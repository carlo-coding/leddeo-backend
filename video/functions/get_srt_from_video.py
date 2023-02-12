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
    audio_path = os.path.join(output_dir, output_audio)
    clip = mp.VideoFileClip(uploaded_vid)

    clip.audio.write_audiofile(audio_path)

    clip_duration = clip.audio.duration
    clip.close()

    clip_bytes = os.stat(audio_path).st_size
    model = whisper.load_model(model_type)
    result  = model.transcribe(audio_path)
    
    data = []
    for i in result['segments']:
        data.append({
          "id": uuid.uuid4(),
          "begin": float(i['start']),
          "end": float(i['end']),
          "text": i['text']
        })
    return data, clip_duration, clip_bytes