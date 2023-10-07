#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Quick & Dirty way of splitting annotation (GT) and ANY number of additional source directories into splits bins
"""
import os
import random
import shutil
from pathlib import Path

HOME = Path.cwd()
# Source directories and target directory
DEFAULT_SOURCE_ANNOT_DIR = Path("data/annotations")
DEFAULT_OUTPUT_DIR = Path("data/splitted-dataset")
DEFAULT_ALL_SOURCE_DIRS = {
    "annotations": ".xml",
    "frames": ".jpg",
}

# Define the proportion for each subdirectory under the target directory
# The keys are subdirectory names, and values are proportions (between 0 and 1)
DEFAULT_SPLITS = {
    "train": 0.8,
    "valid": 0.2,
    # "subdir3": 0.2,
}

# Function to move files based on the specified proportions
def move_files(
  source_annot_dir, 
  all_source_dirs,
  target_dir, 
  split_dict
  ):
  """
  parameter:
    source_annot_dir (Path): 
      full path of the annotation directory
    all_source_dirs (dict):
      all dir names of source directories in the same parent directory as `source_annot_dir) : and their file extension
      
  """
  # Defined source directory
  source_dir = source_annot_dir.parent
  cts, create_dest_dirs = 0, False
  for source_file in source_annot_dir.iterdir():
    if source_file.is_file():
      # Check if the file has a same link/different extension in all source dirs
      same_name_diff_ext = [
          (source_dir/other_dir/(source_file.stem + ext)).exists()
          for (other_dir, ext) in all_source_dirs.items()
      ]
      # check that same file present across source directory
      if all(same_name_diff_ext):
        print(f"File-name qualified and transferred:{source_file.stem}")
        cts += 1
        # Randomly select the target subdirectory
        target_subdir = random.choices(
            list(split_dict.keys()),
            weights=list(split_dict.values()),
        )[0]
        # Construct the target path
        target_path = target_dir / target_subdir
        target_path.parent.mkdir(
          parents=True, exist_ok=True)
        # Move the sources files to the target directory
        for source_name, ext in all_source_dirs.items():
          (target_path/source_name).mkdir(parents=True, exist_ok=True)
          shutil.copy(
            source_dir/source_name/ (source_file.stem + ext),
            target_path/source_name/ (source_file.stem + ext)
          )
  print(f"Process completed. Number of entity transferred:{cts}")

def main(args):
  print(f"Arugments:{args}")
  # Call the function to move files
  move_files(args.annot_dir, args.all_source_dirs, args.output_dir, args.splits)

if __name__ == "__main__":
    import argparse, json

    parser = argparse.ArgumentParser()
    parser.add_argument("-A", "--annot_dir", type=Path, default=DEFAULT_SOURCE_ANNOT_DIR)
    parser.add_argument(
      "-S", "--all_source_dirs",
      type=json.loads,
      help="list of folder in the same directory to split with the annotation gt",
      default=json.dumps(DEFAULT_ALL_SOURCE_DIRS),
    )
    parser.add_argument(
      "-T", "--output_dir", 
      type=Path, default=DEFAULT_OUTPUT_DIR
    )
    parser.add_argument(
      "--splits", type=json.loads, default=json.dumps(DEFAULT_SPLITS)
    )
    args = parser.parse_args()
    print("Created split directory")
    Path(args.output_dir).mkdir(
      exist_ok=True, parents=True)
    main(args)
