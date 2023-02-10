import whisper
import moviepy.editor as mp
from moviepy.editor import *
import os
import uuid

def get_srt_from_video( 
  uploaded_vid, 
  output_dir, 
  output_audio="audio.mp3",
  model_type="tiny",
):
    video_path = os.path.join(output_dir, output_audio)
    my_clip = mp.VideoFileClip(uploaded_vid)
    my_clip.audio.write_audiofile(video_path)
    my_clip.close()
    model = whisper.load_model(model_type)
    result  = model.transcribe(video_path)
    
    data = []
    for i in result['segments']:
        data.append({
          "id": uuid.uuid4(),
          "begin": float(i['start']),
          "end": float(i['end']),
          "text": i['text']
        })
    return data