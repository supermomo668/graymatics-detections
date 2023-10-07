#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Train quick & dirty YOLOv8 model
"""
from pathlib import Path
import torch, supervision as sv

from ultralytics import YOLO
# from autodistill_yolov8 import YOLOv8

HOME = Path.cwd()

torch.cuda.is_available()
torch.cuda.empty_cache() 

DEFAULT_DATA_YAML_PATH = f"{HOME}/data.yaml"
DEFAULT_EPOCHS = 100
DEFAULT_RUN = 1
DEFAULT_TRAINED_MODEL_PATH = f"{HOME}/runs/detect/{DEFAULT_RUN}/weights/best.pt"

def load_dataset(yaml_path):
  yaml_path = Path(yaml_path)
  dataset = sv.DetectionDataset.from_yolo(
    images_directory_path=yaml_path.parent/'frames',
    annotations_directory_path=yaml_path.parent/'annotations',
    data_yaml_path=yaml_path)
  
  return dataset

def main(args):
  if args.chkpt_path is None:
    target_model = YOLO("yolov8m.pt")
  else:
    target_model = YOLO(args.chkpt_path)
  # Training.  
  # target_model.train(
  #   args.data_yaml_file, epochs=args.epochs)

  train_results = target_model.train(
    data=str(args.data_yaml_file),
    epochs=args.epochs,
    batch=48,
    name=args.data_yaml_file.parent.name+'-yolov8'
  )
  print(f"Results:\n{results}")
  val_results = target_model.val()
  print("Finetune completed")

if __name__=="__main__":
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument(
    '--data_yaml_file', type=Path,
    default = DEFAULT_DATA_YAML_PATH
  )
  ap.add_argument(
    '--epochs', type=int,
    default = DEFAULT_EPOCHS
  )
  ap.add_argument(
    '--chkpt_path', 
    default=None
  )
  args = ap.parse_args()
  main(args)