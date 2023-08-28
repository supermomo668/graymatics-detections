import os
import shutil
from pathlib import Path

def copy_all_content_to_all_directory(target_directory):
    current_directory = Path.cwd()/target_directory
    call_directory = os.path.join(current_directory, 'all')

    # Create 'call' directory if it doesn't exist
    if not os.path.exists(call_directory):
      os.mkdir(call_directory)

    # Iterate through subdirectories
    for fp in Path(current_directory).glob('**/*'):
      if fp.parent.name =='all': continue
      if os.path.isfile(fp):  # Check if it's a file and not a directory
          fn = Path(fp).parent.name + '_' + Path(fp).name
          destination_path = os.path.join(call_directory, fn)
          shutil.copy(fp, destination_path)
          print(f"copied '{fp}' to 'aall' directory")

if __name__ == "__main__":
  target_directory = 'frames'
  copy_all_content_to_all_directory(target_directory)
