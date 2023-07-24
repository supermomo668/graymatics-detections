ARG OPENCV_VERSION 4.5.2
# sources: https://viking-drone.com/wiki/installing-opencv-4-5-2/

FROM nvcr.io/nvidia/cuda:11.6.2-cudnn8-devel-ubuntu20.04 AS builder-opencv-base

ARG ONNXRUNTIME_VERSION=1.12.0

ENV DEBIAN_FRONTEND noninteractive
ARG OPENCV_VERSION

RUN apt update && apt upgrade -y && apt install -y build-essential cmake git unzip pkg-config \
  libjpeg-dev libpng-dev libtiff-dev wget \
  libavcodec-dev libavformat-dev libswscale-dev \
  libgtk2.0-dev libcanberra-gtk* \
  python3-dev python3-numpy python3-pip \
  libxvidcore-dev libx264-dev libgtk-3-dev \
  libtbb2 libtbb-dev libdc1394-22-dev \
  libv4l-dev v4l-utils \
  libavresample-dev libvorbis-dev libxine2-dev \
  libfaac-dev libmp3lame-dev libtheora-dev \
  libopencore-amrnb-dev libopencore-amrwb-dev \
  libopenblas-dev libatlas-base-dev libblas-dev  \
  liblapack-dev libeigen3-dev gfortran  \
  libhdf5-dev protobuf-compiler  \
  libprotobuf-dev libgoogle-glog-dev libgflags-dev 

RUN cd ~ && wget -O opencv.zip https://github.com/opencv/opencv/archive/$OPENCV_VERSION.zip && unzip opencv.zipp && mv opencv-$OPENCV_VERSION opencv && rm opencv.zip

FROM builder-opencv-base as builder-opencv-build

RUN cd ~/opencv && mkdir build && cd build && \
  cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_C_COMPILER=/usr/bin/gcc-6 -D CMAKE_INSTALL_PREFIX=/usr/local -D INSTALL_PYTHON_EXAMPLES=ON -D INSTALL_C_EXAMPLES=OFF -D WITH_TBB=ON -D WITH_CUDA=ON -D BUILD_opencv_cudacodec=OFF -D ENABLE_FAST_MATH=1 -D CUDA_FAST_MATH=1 -D WITH_CUBLAS=1 -D WITH_V4L=ON -D WITH_QT=OFF -D WITH_OPENGL=ON -D WITH_GSTREAMER=ON -D OPENCV_GENERATE_PKGCONFIG=ON -D OPENCV_PC_FILE_NAME=opencv.pc -D OPENCV_ENABLE_NONFREE=ON -D OPENCV_PYTHON3_INSTALL_PATH=~/.virtualenvs/cv/lib/python3.8/site-packages -D OPENCV_EXTRA_MODULES_PATH=~/downloads/opencv/opencv_contrib-4.5.2/modules -D PYTHON_EXECUTABLE=~/.virtualenvs/cv/bin/python -D BUILD_EXAMPLES=ON -D BUILD_SHARED_LIBS=OFF ..
  
RUN make -j$(nproc) && make install && ldconfig && make clean && rm -rf ~/opencv

FROM builder-opencv-build AS builder-onnx

# Install package dependencies
RUN apt update && apt install -y --no-install-recommends \
      build-essential \
      software-properties-common \
      autoconf \
      automake \
      libtool \
      pkg-config \
      ca-certificates \
      wget \
      git \
      curl \
      libjpeg-dev \
      libpng-dev \
      language-pack-en \
      locales \
      locales-all \
      python3 \
      python3-py \
      python3-dev \
      python3-pip \
      python3-numpy \
      python3-pytest \
      python3-setuptools \
      libprotobuf-dev \
      protobuf-compiler \
      zlib1g-dev \
      swig \
      vim \
      gdb \
      valgrind \
      libsm6 \
      libxext6 \
      libxrender-dev \
      cmake \
      unzip && \
    apt-get clean

RUN cd /usr/local/bin && \
    ln -s /usr/bin/python3 python && \
    ln -s /usr/bin/pip3 pip && \
    pip install --upgrade pip setuptools wheel

FROM builder-onnx AS runner
# System locale
# Important for UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN pip install Pillow==9.4.0 onnx==${ONNXRUNTIME_VERSION} onnxruntime-gpu==${ONNXRUNTIME_VERSION}

WORKDIR /ONNX-yolov5
COPY / /ONNX-yolov5

RUN mkdir build && cd build && cmake .. && make -j4

# COPY ..yolov5/yolov5.onnx /

ENTRYPOINT ./build/main yolov5n.onnx 