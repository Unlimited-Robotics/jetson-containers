#---
# name: nav2
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

COPY ./filter_ros_packages.py /

RUN source /opt/ros/humble/install/setup.bash && \
    mkdir -p ${ROS_ROOT}/src && \
    cd ${ROS_ROOT} && \
    rosinstall_generator --deps --rosdistro ${ROS_DISTRO} \
            angles \
            apriltag \
            behaviortree_cpp_v3 \
            bondcpp \
            camera_calibration_parsers \
            camera_info_manager \
            compressed_image_transport \
            compressed_depth_image_transport \
            cv_bridge \
            demo_nodes_cpp \
            demo_nodes_py \
            diagnostic_updater \
            example_interfaces \
            image_geometry \
            image_pipeline \
            image_transport \
            image_transport_plugins \
            launch_xml \
            launch_yaml \
            launch_testing \
            launch_testing_ament_cmake \
            nav2_msgs \
            ompl \
            resource_retriever \
            rqt_image_view \
            rviz2 \
            sensor_msgs \
            slam_toolbox \
            v4l2_camera \
            vision_opencv \
            vision_msgs \
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
        libopencv-imgproc-dev python-opencv python3-opencv \
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

# Install nav2
# navigation2   gary    be1ad35f188a205dfc7ec7a6f2c1a432e4bae3ba
# BehaviorTree  3.8.5   2fb11758ea4b1ab1f9501fe1032e7c28684fe3f6
RUN apt-get update && mkdir -p ${ROS_ROOT}/src && cd ${ROS_ROOT}/src && \
    git clone https://github.com/Unlimited-Robotics/navigation2.git && \
    cd navigation2 && git checkout 1ec05bc67ff335464d89ece2aafeeaaaa7b79dd9 && \
    cd .. && \
    git clone https://github.com/BehaviorTree/BehaviorTree.CPP.git && \
    cd BehaviorTree.CPP && git checkout 2fb11758ea4b1ab1f9501fe1032e7c28684fe3f6 && \
    cd .. && \
    source ${ROS_ROOT}/install/setup.bash && cd ${ROS_ROOT} && \
    rosdep install -y -r --ignore-src --from-paths src --rosdistro ${ROS_DISTRO} && \
    colcon build --merge-install --cmake-args -DCMAKE_BUILD_TYPE=RelWithDebInfo \
        --packages-up-to-regex nav2* \
        --packages-ignore nav2_system_tests nav2_mppi_controller && \
    rm -Rf src build log && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
