ALLOWED_EXTENSIONS = ['mp4', 'mov', 'webm', 'ts', 'avi', 'y4m', 'mkv', "flv", "wmv", "mpeg", "mpg"]

def allowed_video_file(filename):
  file_extension = filename.split(".")[-1]
  return file_extension in ALLOWED_EXTENSIONS