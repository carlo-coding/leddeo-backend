import os
from uuid import uuid4
from tempfile import gettempdir

def get_temp_folders():
  temp_dir = gettempdir()
  uploads_folder = os.path.join(temp_dir, f"temp_uploads_{uuid4()}")
  outputs_folder = os.path.join(temp_dir, f"temp_outputs_{uuid4()}")

  if not os.path.exists(uploads_folder):
    os.mkdir(uploads_folder)
  if not os.path.exists(outputs_folder):
    os.mkdir(outputs_folder)
  
  return uploads_folder, outputs_folder