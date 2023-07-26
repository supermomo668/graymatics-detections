## Introdution
[Repo Sources](https://github.com/Hexmagic/ONNX-yolov5)
[dockerfile] (https://github.com/leimao/ONNX-Runtime-Inference/tree/main)
Deploy ultralytics [Yolov5](https://github.com/ultralytics/yolov5.git) pretained model with C++ language ;

<div align="center">
<img src="assets/output.jpg">
</div>


## Env
1. GCC 7.5
2. Opencv 4.5.4



### Build in docker
(OpenCV C++ installation performed in dockerfile)[https://docs.opencv.org/4.x/d7/d9f/tutorial_linux_install.html]

## Set-up GTK backend connection to be able to visualize from the docker application
### This portion is host machine dependent , since the docker container are unable to produce visualization 
### On Windows:
[Instructions](https://dev.to/darksmile92/run-gui-app-in-linux-docker-container-on-windows-host-4kde)
1. Install Display Host: ```choco install vcxsrv```
2. Open the application ```XLaunch```, proceed through installation instructions and save the final configuration file in ```%userprofile```
3. Run docker with the following commands (powershell):
```
set-variable -name DISPLAY -value [your ipv4 address]:0.0
docker build -f docker\dockerfile -t onnx-yolo5 .
```

## Docker Build
This command is what built the docker and does not need to be repeated.
```
docker build -f docker\dockerfile -t onnx-yolo5 .
```
And now you maybe proceed to infer with the docker
## Infer with Docker
```
docker run -dit --rm -e DISPLAY=$DISPLAY --net host --name yolov5 onnx_yolov5 {path_to_input}
```
