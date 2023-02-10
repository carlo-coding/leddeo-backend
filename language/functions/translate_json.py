from .translate_text import translate_text
from .download_packages import download_packages

def translate_json(json, from_code, to_code):
  if from_code == to_code:
    return json
  codes = download_packages(from_code, to_code)
  translated_json = []
  for item in json:
    translated_json.append({
      "id": item["id"],
      "begin": item["begin"],
      "end": item["end"],
      "text": translate_text(item["text"], codes)
    })
  return translated_json