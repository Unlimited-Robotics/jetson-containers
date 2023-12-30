#---
# name: gary
# group: base
# depends: [pytorch, torchvision, torchaudio, torch2trt, opencv_ffmpeg, pycuda, realsense, zed, ros:humble-desktop, nav2, rtabmap, moveit]
# postfix: 3.7.0.dev
#---
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG ROS_PACKAGE=ros_base
ARG ROS_VERSION=humble

ENV ROS_DISTRO=${ROS_VERSION}
ENV ROS_ROOT=/opt/ros/${ROS_DISTRO}
ENV ROS_PYTHON_VERSION=3

ENV DEBIAN_FRONTEND=noninteractive
ENV SHELL /bin/bash
SHELL ["/bin/bash", "-c"] 

ENV LANG=en_US.UTF-8
ENV PYTHONIOENCODING=utf-8
ENV LD_PRELOAD=$LD_PRELOAD:'/usr/lib/aarch64-linux-gnu/libgomp.so.1'

COPY ros_entrypoint.sh /ros_entrypoint.sh
