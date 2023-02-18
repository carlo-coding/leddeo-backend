def predict_download(duration, size):
  return duration * 6.96571632e-01 + size * 8.80247327e-07 - 3.9184691319678393

def predict_transcription(duration, size):
  return  duration * -2.49418411e+00 + size* 1.61425249e-04  + 39.40729092426871

def predict_translation(words):
  return words * 0.02850206 + 8.332316943782583