#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Train quick & dirty YOLOv8 model
"""
from pathlib import Path
import torch

from autodistill_yolov8 import YOLOv8

HOME = Path.cwd()

torch.cuda.is_available()
torch.cuda.empty_cache() 

INPUT_VIDEO_PATH = f"{HOME}/data/project-1_omni-processed/"
DEFAULT_DATA_YAML_PATH = f"{HOME}/data.yaml"
# OUTPUT_VIDEO_PATH = f"{DATA_HOME}/output-{name}"
DEFAULT_RUN = 1
DEFAULT_TRAINED_MODEL_PATH = f"{HOME}/runs/detect/{DEFAULT_RUN}/weights/best.pt"

def main(args):
  if args.chkpt_path is None:
    target_model = YOLOv8("yolov8n.pt")
    target_model.train(args.data_yaml_file, epochs=70)
  print("Finetune completed")

if __name__=="__main__":
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument(
    '--chkpt_path', 
    default=f"{HOME}/runs/detect/1/weights/best.pt"
  )
  ap.add_argument(
    '--data_yaml_file', 
    default = DEFAULT_DATA_YAML_PATH
  )
  args = ap.parse_args()