#---
# name: moveit
# group: ros
# depends: [ros:humble-desktop]
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

RUN mkdir -p ${ROS_ROOT}/src && \
    cd ${ROS_ROOT} && \
    rosinstall_generator --deps --rosdistro ${ROS_DISTRO} \
            moveit \
        > ros2.${ROS_DISTRO}.ros_base.rosinstall && \
    vcs import src < ros2.${ROS_DISTRO}.ros_base.rosinstall && \
    apt-get update && \
    rosdep update && \
    rosdep install -y --ignore-src --from-paths src --rosdistro ${ROS_DISTRO} --skip-keys "fastcdr rti-connext-dds-6.0.1 rti-connext-dds-5.3.1 urdfdom_headers libopencv-dev libopencv-contrib-dev libopencv-imgproc-dev python-opencv python3-opencv" && \
    colcon build --merge-install --cmake-args -DCMAKE_BUILD_TYPE=Release -DBUILD_TESTING=OFF -DCMAKE_EXPORT_COMPILE_COMMANDS=ON --ament-cmake-args -DCMAKE_BUILD_TYPE=Release && \
    rm -Rf src build log ${ROS_ROOT}/ros2.${ROS_DISTRO}.ros_base.rosinstall && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get clean
