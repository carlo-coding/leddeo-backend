def float_to_srt_time(seconds):
  hours = int(seconds // 3600)
  minutes = int((seconds % 3600) // 60)
  seconds = int(seconds % 60)
  miliseconds = int((seconds - int(seconds)) * 1000)
  hours = str(hours).zfill(2)
  minutes = str(minutes).zfill(2)
  seconds = str(seconds).zfill(2)
  return f"{hours}:{minutes}:{seconds},{miliseconds}"