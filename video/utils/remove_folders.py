import os
import shutil

def remove_folders(*args):
  for folder in args:
    try:
      if os.path.exists(folder):
          shutil.rmtree(folder)
          print(f"{folder} ha sido borrado.")
      else:
          print(f"{folder} no existe.")
    except:
      print(f"No se pudo borrar el directorio temporal {folder}")