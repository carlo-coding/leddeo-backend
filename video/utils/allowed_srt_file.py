ALLOWED_EXTENSIONS = ["srt", "txt"]

def allowed_srt_file(filename):
  file_extension = filename.split(".")[-1]
  return file_extension in ALLOWED_EXTENSIONS