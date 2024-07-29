#---
# name: gary
# group: base
# depends: [pytorch, torchvision, torchaudio, torch2trt, opencv_ffmpeg, pycuda, realsense, zed, ros:humble-desktop, nav2, rtabmap, moveit]
# postfix: 3.7.22.dev
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

RUN source /opt/ros/humble/install/setup.bash && \
    mkdir -p ${ROS_ROOT}/src && \
    cd ${ROS_ROOT} && \
    rosinstall_generator --deps --rosdistro ${ROS_DISTRO} \
            ros2_control \
            rplidar_ros \
            imu_filter_madgwick \
            robot_localization \
            tf_transformations \
            ros2_controllers \
        > packages_to_install.rosinstall && \
    ros2 pkg list > installed_packages.list && \
    /filter_ros_packages.py && \
    echo "" && \
    echo "--- ROS INSTALL GENERATOR FILTERED ---" && \
    echo "PACKAGES TO INSTALL:" && \
    cat packages_to_install.filtered.rosinstall && \
    echo "" && \
    vcs import src < packages_to_install.filtered.rosinstall && \
    apt-get update && \
    rosdep update && \
    rosdep install -y --ignore-src --from-paths src --rosdistro ${ROS_DISTRO} \
        --skip-keys "fastcdr rti-connext-dds-6.0.1 rti-connext-dds-5.3.1 \
        urdfdom_headers libopencv-dev libopencv-contrib-dev \
        libopencv-imgproc-dev python-opencv python3-opencv moveit_msgs gripper_controllers \
        $(ros2 pkg list | tr '\n' ' ')" && \
    colcon build --merge-install --cmake-args -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_TESTING=OFF -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
        --ament-cmake-args -DCMAKE_BUILD_TYPE=Release \
        --packages-skip cyclonedds fastcdr fastrtps foonathan_memory_vendor \
        google_benchmark_vendor gmock_vendor gtest_vendor iceoryx_binding_c \
        iceoryx_hoofs iceoryx_posh osrf_testing_tools_cpp urdfdom \
        urdfdom_headers $(ros2 pkg list | tr '\n' ' ') && \
    rm -Rf src build log && \
    rm -Rf ${ROS_ROOT}/installed_packages.list && \
    rm -Rf ${ROS_ROOT}/packages_to_install.rosinstall && \
    rm -Rf ${ROS_ROOT}/packages_to_install.filtered.rosinstall && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get clean

RUN mkdir -p /opt/raya_os/tools/ && \
    cd /opt/raya_os/tools/ && \
    git clone https://github.com/BehaviorTree/Groot.git && \
    cd Groot && \
    git submodule update --init --recursive && \
    mkdir build && \
    cd build && \
    cmake .. && \
    make

# Install YDLidar-SDK
# https://github.com/YDLIDAR/YDLidar-SDK
RUN cd /opt && \
    git clone https://github.com/YDLIDAR/YDLidar-SDK.git && \
    cd YDLidar-SDK && \
    mkdir build && cd build && cmake .. &&\
    make && make install && \
    cd ../.. && rm -r YDLidar-SDK/

# Install YDLidar-ros2-driver
# https://github.com/YDLIDAR/YDLidar-SDK
# humble branch Jan 5 2024: aa9a97b070a1c700f95e5de9244c15c0f7028d76
RUN mkdir -p ${ROS_ROOT}/src && cd ${ROS_ROOT}/src && \
    git clone https://github.com/YDLIDAR/ydlidar_ros2_driver.git && \
    cd ydlidar_ros2_driver && \
    git checkout aa9a97b070a1c700f95e5de9244c15c0f7028d76 && \
    cd ${ROS_ROOT} && \
    source ${ROS_ROOT}/install/setup.bash && \
    colcon build --merge-install && \
    rm -rf src build log

# Realsense calibration tool
RUN UBUNTU_BASE=$(grep -oP '(?<=UBUNTU_CODENAME=)[^\s"]+' /etc/os-release) && \
    sudo add-apt-repository "deb https://librealsense.intel.com/Debian/apt-repo ${UBUNTU_BASE} main" && \
    sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE || sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-key F6E65AC044F831AC80A06380C8B3A55A6F3EFCDE && \
    sudo apt-get update && \
    sudo apt-get install -y freeglut3 librscalibrationtool && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

# Install C++ GPIO Port
# https://github.com/pjueon/JetsonGPIO
RUN cd /opt/raya_os/tools/ && \
    git clone -b v1.2.5 https://github.com/pjueon/JetsonGPIO.git && \
    cd JetsonGPIO && \
    echo JEISON && \
    mkdir build && cd build && cmake .. && \
    make && make install

COPY ros_entrypoint.sh /ros_entrypoint.sh
