

import os
from pathlib import Path

SOURCE_ANNOT_DIRNAME='annotations'
SOURCE_FRAMES_DIRNAME='frames'
HOME=Path.getcwd()
def main(args):
  xml_files = []
  for file in Path(
    args.data_voc_dir/SOURCE_ANNOT_DIRNAME
    ).glob("*.xml"):
    print(file )
    
    
  return xml_files
  
if __name__=="__main__":
  import argparse, json

  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--data_voc_dir", type=str, default=HOME/'argrosuper', required=True)
  parser.add_argument(
    "--output_dir", type=str, default=HOME/'agrosuper-yolo' , required=True)
  parser.add_argument(
    "--splits", type=json.loads, default='{"train":0.8, "val":0.2}')
  args = parser.parse_args()
  Path(args.output_dir).mkdir(exist_ok=True, parents=True)
  main(args)