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
yolo predict model="{TRAINED_MODEL_PATH}" source="{INPUT_VIDEO_PATH}" conf=0.8
```

## Example
1. You may first extract frames from directory of videos
