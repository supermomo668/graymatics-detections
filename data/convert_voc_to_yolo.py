"""
Convert VOC(.xml) labels to YOLO(.txt) 
Usage:
  Require dataset to be in YOLO structure but annotations are in .xml. 
  train
    images
    labels-voc
    (labels) <- to be created
  val 
    ...
"""
import glob, yaml
from pathlib import Path
import xml.etree.ElementTree as ET

from sqlalchemy import exists

DEFAULT_SPLIT_DIRS = ['train', 'val']
DEFAULT_CLASSES = ['0', '1']
# hardcoded , must use this name
DEFAULT_VOC_LABEL_DIRNAME="labels-voc"

HOME = Path.cwd()
DEFAULT_DATASET_PARENT_PATH = HOME / "dataset"

def getImagesInDir(dir_path):
    image_list = []
    for filename in glob.glob(dir_path + '/*.jpg'):
        image_list.append(filename)

    return image_list

def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(source_voc_path, output_path, classes:list):
    in_file, out_file = open(source_voc_path), open(output_path/(source_voc_path.stem + '.txt'), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w, h = int(size.find('width').text), int(size.find('height').text)

    for obj in root.iter('object'):
      difficult = obj.find('difficult').text
      cls = obj.find('name').text
      # if cls not in classes or int(difficult)==1:
      #   print(f"Skipping as class {cls} not in {classes}. To avoid this, comment this block out")
      #   continue
      cls_id = classes.index(cls)
      xmlbox = obj.find('bndbox')
      b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
      bb = convert((w,h), b)
      out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

def get_cls_labels(dataset_path):
  with open(dataset_path/'data.yaml') as f:
    conf = yaml.safe_load(f)
  return conf.get('names')


def main(args):
    """
    args:
      dataset_path
      dirs
      classes
    """
    cls_labels = get_cls_labels(args.dataset_path)
    print("")
    for split in args.splits:
      full_dir_path = args.dataset_path/split
      output_path = full_dir_path/args.output_label_dir

      output_path.mkdir(exist_ok=True, parents=True)
      
      for cts, voc_label_file in enumerate((full_dir_path/args.source_label_dir).iterdir()):
        convert_annotation(voc_label_file, output_path, classes=cls_labels)

      print(f"Finished processing:{split}. Converted {cts} files.")

if __name__=="__main__":
  import argparse
  from pathlib import Path
  ap = argparse.ArgumentParser()
  ap.add_argument(
    '-D', '--dataset_path', type=Path,
    default = DEFAULT_DATASET_PARENT_PATH
  )  
  ap.add_argument(
    '-S','--splits', nargs='+', 
    default=DEFAULT_SPLIT_DIRS
  )

  ap.add_argument(
    '--source_label_dir', type=str, help="",
    default = DEFAULT_VOC_LABEL_DIRNAME
  )
  ap.add_argument(
    '--output_label_dir', type=str, help="",
    default = 'labels'
  )
  args = ap.parse_args()
  main(args)