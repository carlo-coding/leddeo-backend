from rest_framework.parsers import FileUploadParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from commons.permissions import CustomerHasPlan
from .functions.get_srt_from_video import get_srt_from_video
from .functions.apply_srt_to_video import apply_srt_to_video
from .utils.allowed_video_file import allowed_video_file
from .utils.allowed_srt_file import allowed_srt_file
from .utils.get_temp_folders import get_temp_folders
from .utils.remove_folders import remove_folders
from django.http import HttpResponse
from history.models import History
from .models import SubtitlesRecord, DownloadsRecord
from .serializers import SubtitlesRecordSerializer, DownloadsRecordSerializer
from commons.utils import user_from_request
import string
from uuid import uuid4
from time import time
import os

class VideoUploadView(APIView):
  parser_class = (FileUploadParser,)
  permission_classes=[IsAuthenticated, CustomerHasPlan]

  def post(self, request):
    st = time() 
    model_type="small"
    user = user_from_request(request)
    uploads_folder, outputs_folder = get_temp_folders()

    video_file = request.data["file"]
    filename = video_file.name

    if filename == "":
      return Response(
        { "message": "File name not provided" }, 
        content_type="application/json", 
        status=400
      )
    if not video_file or not allowed_video_file(filename):
      return Response(
        { "message": "File type not allowed, must be a video" }, 
        content_type="application/json", 
        status=415
      )
    filename = f"{uuid4()}-{filename}"

    # Save uploaded file
    file_path = os.path.join(uploads_folder, filename)
    with open(file_path, 'wb') as f:
      f.write(video_file.read())

    data, clip_duration, clip_bytes = get_srt_from_video(
      uploaded_vid=file_path,
      output_dir=outputs_folder,
      model_type=model_type
    )

    text_content = "".join([i["text"] for i in data])
    number_of_words = sum([i.strip(string.punctuation).isalpha() for i in text_content.split()])

    if data == None:
      return Response(
        { "message": "Error trying to access the output directory" }, 
        content_type="application/json", 
        status=500
      )

    response = {
      "message": "Video successfully uploaded",
      "data": data
    }

    remove_folders(uploads_folder, outputs_folder)

    et = time()
    SubtitlesRecord.objects.create(
      user=user,
      audio_duration=clip_bytes,
      audio_size=clip_duration,
      process_duration=et - st,
      whisper_model=model_type,
      number_of_words=number_of_words
    ).save()

    return Response(response, content_type="application/json")



class VideoCaptionView(APIView):
  parser_class = (FileUploadParser,)
  permission_classes=[IsAuthenticated, CustomerHasPlan]

  def post(self, request):
    st = time()
    user = user_from_request(request)
    uploads_folder, outputs_folder = get_temp_folders()

    video_file = request.data["video"]
    srt_file = request.data["srt"]
    try:
      fontsize= float(request.GET.get("size", 20))
      bgcolor= request.GET.get("bgcolor", "transparent")
      color= request.GET["color"]
      font= request.GET["font"]
      posh= request.GET["halign"]
      posv= request.GET["valign"]
    except:
      return Response(
        { "message": "one or more quired query params were not valid" },
        content_type="application/json",
        status=400
      )

    video_filename = video_file.name
    srt_filename = srt_file.name

    original_name = video_file.name

    if video_filename == "" or srt_filename == "":
      return Response(
        { "message": "Filename not provided" }, 
        content_type="application/json", 
        status=400
      )
    if not video_file or not allowed_video_file(video_filename):
      return Response(
        { "message": "File type not allowed, must be a video" }, 
        content_type="application/json", 
        status=415
      )
    if not srt_file or not allowed_srt_file(srt_filename):
      return Response(
        { "message": "File type not allowed, must be an srt file" }, 
        content_type="application/json", 
        status=415
      )
    video_filename = f"{uuid4()}-{video_filename}"
    srt_filename = f"{uuid4()}-{srt_filename}"

    # Save uploaded files
    video_file_path = os.path.join(uploads_folder, video_filename)
    with open(video_file_path, 'wb') as f:
      f.write(video_file.read())
    video_size = os.stat(video_file_path).st_size

    srt_file_path = os.path.join(uploads_folder, srt_filename)
    with open(srt_file_path, 'wb') as f:
      f.write(srt_file.read())

    output_file_dir, output_file_name, video_duration, video_size_compressed = apply_srt_to_video(
      uploaded_vid=video_file_path,
      uploaded_srt=srt_file_path,
      output_dir=outputs_folder,
      font=font,
      fontsize=fontsize,
      color=color,
      bgcolor=bgcolor,
      pos=(posh, posv)
    )

    if output_file_dir == None:
      return Response(
        { "message": "Error trying to access the output directory" }, 
        content_type="application/json", 
        status=500
      )
    
    file = open(output_file_dir, "rb")
    response = HttpResponse(file.read(), content_type='video/mp4', )
    response['Content-Disposition'] = 'attachment; filename="%s"' % output_file_name
    file.close()

    remove_folders(uploads_folder, outputs_folder)

    history = History.objects.create(
      user=user,
      action="VC",
      description=f"applied subtitles to {original_name}"
    )
    history.save()
    et = time()
    DownloadsRecord.objects.create(
      user=user,
      video_duration=video_duration,
      video_size=video_size,
      video_size_compressed=video_size_compressed,
      process_duration=et - st,
    ).save()


    return response


class SubtitlesRecordView(APIView):
  permission_classes=[IsAuthenticated]

  def get(self, request):
    objects = SubtitlesRecord.objects.all()
    data = SubtitlesRecordSerializer(objects, many=True).data
    return Response(data)

class DownloadsRecordView(APIView):

  def get(self, request):
    objects = DownloadsRecord.objects.all()
    data = DownloadsRecordSerializer(objects, many=True).data
    return Response(data)