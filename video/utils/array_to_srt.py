from .float_to_srt_time import float_to_srt_time

def array_to_srt(array):
  srt = ""
  for i, d in enumerate(array):
    begin = float_to_srt_time(float(d["begin"]))
    end = float_to_srt_time(float(d["end"]))
    srt += f"{i+1}\n{begin} --> {end}\n{d['text'].strip()}\n\n"
  return srt