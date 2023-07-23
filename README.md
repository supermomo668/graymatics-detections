# graymatics-yolo-detection

# Instructions
## Create application
Run ```run.sh``` with no argument to deploy application ready for inference. Change variable ARG  ```MODELNAME``` to not use the default ```yolov5n``` model

## Inference 
use running container by passing commands as follows:
```
docker exec -it {PATH to INPUT VIDEO}
```
and optionally pass a run name as a subdirectory:
```--name {NAME}```
and it will display real-time detected results as well as saving a result video under ```/graymatics/{NAME}```