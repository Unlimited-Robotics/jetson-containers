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

RUN source /opt/ros/humble/install/setup.bash && \
    mkdir -p ${ROS_ROOT}/src && \
    cd ${ROS_ROOT} && \
    rosinstall_generator --deps --rosdistro ${ROS_DISTRO} \
            moveit \
            controller_manager_msgs \
            control_toolbox \
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
    apt-get install -y libfcl-dev && \
    rosdep install -y --ignore-src --from-paths src --rosdistro ${ROS_DISTRO} \
        --skip-keys "fastcdr rti-connext-dds-6.0.1 rti-connext-dds-5.3.1 \
        urdfdom_headers libopencv-dev libopencv-contrib-dev \
        libopencv-imgproc-dev python-opencv python3-opencv moveit_ros_benchmarks moveit_msgs pilz_industrial_motion_planner \
        $(ros2 pkg list | tr '\n' ' ')" && \
    rm -r src/moveit src/moveit_msgs && \
    apt-get remove -y libfcl-dev
    
RUN source /opt/ros/humble/install/setup.bash && \
    cd ${ROS_ROOT}/src && \
    git clone https://github.com/Unlimited-Robotics/moveit2 && \
    cd ./moveit2/ && \
    git checkout 6fae6e7bb6db9b1aaaefc779a0ee208f0fd74a8d && \
    cd ${ROS_ROOT}/src && \
    git clone https://github.com/Unlimited-Robotics/moveit_msgs && \
    cd ./moveit_msgs/ && \
    git checkout 693578844ba57b7aa6292fcb9ee190431a7e5fe2 && \
    cd ${ROS_ROOT}/src && \
    git clone https://github.com/Unlimited-Robotics/fcl && \
    cd ./fcl/ && \
    git checkout 519c9a35a9bf72fb9fc6012535e26f8c236524d1 && \
    cd ${ROS_ROOT} && \
    colcon build --merge-install --cmake-args -DCMAKE_BUILD_TYPE=Release \
        -DBUILD_TESTING=OFF -DCMAKE_EXPORT_COMPILE_COMMANDS=ON \
        --ament-cmake-args -DCMAKE_BUILD_TYPE=Release \
        --packages-skip cyclonedds fastcdr fastrtps foonathan_memory_vendor \
        google_benchmark_vendor gmock_vendor gtest_vendor iceoryx_binding_c \
        iceoryx_hoofs iceoryx_posh osrf_testing_tools_cpp urdfdom \
        urdfdom_headers $(ros2 pkg list | tr '\n' ' ') && \
    rm -Rf src build log ${ROS_ROOT}/ros2.${ROS_DISTRO}.ros_base.rosinstall && \
    rm -Rf /var/lib/apt/lists/* && \
    apt-get clean
