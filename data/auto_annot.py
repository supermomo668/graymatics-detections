#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created
@author Matthew info@ezout.store
This script is used to preprocess the data.
Perform unsupervised annotation using foundation models
"""

from pathlib import Path
import cv2
import supervision as sv
from autodistill.detection import CaptionOntology

from typing import List, Tuple, Optional
import matplotlib.pyplot as plt
import random
"""
# Required modules to install depending of model used
%pip3 install autodistill-owl-vit
%pip3 install autodistill-fastsam
%pip install autodistill-grounding-dino
%pip install autodistill-grounded-sam
"""

HOME = Path.cwd()
# print(f"Home path:{HOME}")

DEFAULT_DATA_HOME = HOME
DEFAULT_IMAGE_DIR_PATH = DEFAULT_DATA_HOME/"frames"
DEFAULT_OUTPUT_DATASET_PATH = DEFAULT_DATA_HOME/"dataset-sam-processd"
print(DEFAULT_IMAGE_DIR_PATH, DEFAULT_OUTPUT_DATASET_PATH, sep='\n')
DEFAULT_ONTOLOGY_FILE = DEFAULT_DATA_HOME/'labels.txt'

def setup_imports(model):
  """
  Import time of these models are long, conditional imports
  """
  models = dict()
  match model:
    case "grounded-sam":
      from autodistill_grounded_sam import GroundedSAM
      models.update({model: GroundedSAM})
    case "owl-vit":
      from autodistill_owl_vit import OWLViT
      models.update({model: OWLViT})
    case "fast-sam":
      from autodistill_fastsam import FastSAM
      models.update({model: FastSAM})
    case "grounding-dino":
      from autodistill_grounding_dino import GroundingDINO
      models.update({model: GroundingDINO})
  return models

def plot_images_grid(
    images: List[np.ndarray],
    grid_size: Tuple[int, int],
    titles: Optional[List[str]] = None,
    size: Tuple[int, int] = (12, 12),
    cmap: Optional[str] = "gray",
) -> None:
    """
    Plots images in a grid using matplotlib.
        import cv2
        import supervision as sv
    """
    nrows, ncols = grid_size
    if len(images) > nrows * ncols:
        raise ValueError(
            "The number of images exceeds the grid size. Please increase the grid size"
            " or reduce the number of images."
        )

    fig, axes = plt.subplots(
      nrows=nrows, ncols=ncols, figsize=size)
    for idx, ax in enumerate(axes.flat):
        if idx < len(images):
            if images[idx].ndim == 2:
                ax.imshow(images[idx], cmap=cmap)
            else:
                ax.imshow(cv2.cvtColor(images[idx], cv2.COLOR_BGR2RGB))

            if titles is not None and idx < len(titles):
                ax.set_title(titles[idx])

        ax.axis("off")
    return fig
    
def visualize_dataset(
  dataset, 
  SAMPLE_SIZE = 16, SAMPLE_GRID_SIZE = (4, 4), SAMPLE_PLOT_SIZE = (24, 18)):
  """visualize dataset at random"""
  image_names = list(dataset.images.keys())
  image_names = [image_names[i] for i in random.choices(range(len(image_names)), k=SAMPLE_SIZE)]

  mask_annotator = sv.MaskAnnotator()
  box_annotator = sv.BoxAnnotator()

  images = []
  for image_name in image_names:
      image = dataset.images[image_name]
      annotations = dataset.annotations[image_name]
      labels = [
          dataset.classes[class_id]
          for class_id
          in annotations.class_id]
      annotates_image = mask_annotator.annotate(
          scene=image.copy(),
          detections=annotations)
      annotates_image = box_annotator.annotate(
          scene=annotates_image,
          detections=annotations,
          labels=labels)
      images.append(annotates_image)

  return plot_images_grid(
    images=images,
    titles=image_names,
    grid_size=SAMPLE_GRID_SIZE,
    size=SAMPLE_PLOT_SIZE
  )

def form_ontology(input_file):
  ontology = dict()
  with open(input_file,'r') as f:
    for line in f:
      label, search_ontology = line.strip("\n").split('\t')[:2]
      ontology.update({label:search_ontology})
  return CaptionOntology(ontology)

def main(args):
  models = setup_imports(args.model)
  base_model = models[args.model](
    ontology=form_ontology(args.ontology_file))
  # Label the dataset
  dataset = base_model.label(
    input_folder=args.input_image_dir,
    # extension=args.ext,
    output_folder=args.output_dir
  )
  # Optional visualization
  figure = visualize_dataset(dataset)
  figure.savefig(args.output_dir)
  print("process completed.")
  # return xml_files
  
if __name__=="__main__":
  import argparse, json

  parser = argparse.ArgumentParser()
  parser.add_argument(
    "--model", type=str, 
    choices=["grounded-sam", "owl-vit", "grounding-dino", "fast-sam"],
    default="grounded-sam")
  parser.add_argument(
    "--ontology_file", help="file that contain class labels and optionally description", 
    type=str, default=DEFAULT_ONTOLOGY_FILE)
  parser.add_argument(
    "--input_image_dir", type=str, default=DEFAULT_IMAGE_DIR_PATH)
  parser.add_argument(
    "--output_dir", type=str, default=DEFAULT_OUTPUT_DATASET_PATH)
  parser.add_argument(
    "--splits", type=json.loads, default='{"train":0.8, "val":0.2}')
  args = parser.parse_args()
  Path(args.output_dir).mkdir(exist_ok=True, parents=True)
  main(args)