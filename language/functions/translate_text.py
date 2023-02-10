import argostranslate.package
import argostranslate.translate

def translate_text(text, codes):
  try:

    if (len(codes) == 2):
      return argostranslate.translate.translate(text, codes[0], codes[1])
    elif (len(codes) == 3):
      intermediate_text = argostranslate.translate.translate(text, codes[0], codes[1])
      return argostranslate.translate.translate(intermediate_text, codes[1], codes[2])
    else:
      return text

  except:
    print("Error on translation")
    return text