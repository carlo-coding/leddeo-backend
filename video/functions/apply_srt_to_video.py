from __future__ import unicode_literals
from moviepy.editor import VideoFileClip
from moviepy.editor import *
import os
import cv2
import uuid
from .SubtitleClips import SubtitlesClip
from .compress import compress_video

def apply_srt_to_video( 
  uploaded_vid,
  uploaded_srt, 
  output_dir,
  font="Georgia-Regular",
  fontsize=24,
  color="white",
  bgcolor="rgb(102,102,102)",
  pos=('center','bottom'),
):
    output_video_name = f"{uuid.uuid4()}.mp4"
    output_video_dir = os.path.join(output_dir,output_video_name)

    output_compressed_video_name = f"{uuid.uuid4()}.mp4"
    output_compressed_video_dir = os.path.join(output_dir,output_compressed_video_name)
    compress_video(uploaded_vid, output_compressed_video_dir)
    video_size_compressed = os.stat(output_compressed_video_dir).st_size
    video_to_process = output_compressed_video_dir


    vidcap = cv2.VideoCapture(video_to_process)
    _,image = vidcap.read()
    height = len(image)
    width = len(image[0])

    alignments = {
      "center": "center",
      "right": "East",
      "left": "West"
    }

    generator = lambda txt: TextClip(
      txt, 
      font=font, 
      fontsize=fontsize/0.375, 
      color=color,
      bg_color=bgcolor,
      size = (width, None), 
      method='caption',
      align=alignments[pos[0]]
    )
    subtitles = SubtitlesClip(uploaded_srt, generator, "utf-8")
    video = VideoFileClip(video_to_process)
    video_duration = video.duration
    final = CompositeVideoClip([video, subtitles.set_pos(pos)])
    final.write_videofile(
      output_video_dir, 
      fps=video.fps, 
      remove_temp=True, 
      codec="libx264", 
      audio_codec="aac",
    )
    final.close()

    return output_video_dir, output_video_name, video_duration, video_size_compressed