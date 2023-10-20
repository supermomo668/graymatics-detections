## Crown-plaza
### Pre-reqs
- Video datasets 

  Video Datasets can be feteched via:
  ```
  bash fetchdata.sh
  ```
- Labelling
  and labeled in LabelStudio by using a containerizezd instance
  ```
  bash labelstudio.sh
  ```
- model artifact (inference)
  use ```git lfs pull``` to get the model. 

## Instructions
* Usage: Frame Extractor

Extract frames at interval from a directory of video footages for annotation
```
usage: extract_frames.py [-h] [-D INPUT_DIRECTORY] [-O OUTPUT_DIRECTORY]
                         [-F FRAME_INTERVAL]

options:
  -h, --help            show this help message and exit
  -D INPUT_DIRECTORY, --input_directory INPUT_DIRECTORY
                        folder of videos
  -O OUTPUT_DIRECTORY, --output_directory OUTPUT_DIRECTORY
                        folder of videos
  -F FRAME_INTERVAL, --frame_interval FRAME_INTERVAL
                        Frame interval for extraction
```

* Usage: Inferece

run inference directly on target
```
run_name="train"
INPUT_VIDEO_PATH = f"{DATA_HOME}/video-processed/"
TRAINED_MODEL_PATH = f"{HOME}/runs/detect/{run_name}/weights/best.pt"
!yolo predict model="{TRAINED_MODEL_PATH}" source="{INPUT_VIDEO_PATH}" conf=0.8
```
which is equivalent as running in bash
```bash
yolo predict model=$PROJECT/crown-plaza/runs/detect/train/weights/best.py
```

## Example Training Workflow
1. You may first extract frames from directory of videos via 
```
extract_frames.py -D ${video_direcory} -O "{output_directory}"
```

2. Proceed to annotation in labelimg or label-studio
3. Train on dataset via [the training notebook](notebooks/run_train.ipynb) and follow the instructions within