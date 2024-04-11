#---
# name: rtabmap
# group: ros
# depends: [ ros:humble-desktop, nav2, zed, realsense ]
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
        nav2_msgs \
        pcl_conversions \
        octomap_msgs \
        octomap \
        pcl_ros \
        pcl_conversions \
        octomap_msgs \
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

WORKDIR /root/

# PDAL
RUN apt-get update && apt-get install -y libpdal-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/

#commit Aug 6 2020
RUN git clone https://github.com/laurentkneip/opengv.git && \
    cd opengv && \
    git checkout 91f4b19c73450833a40e463ad3648aae80b3a7f3 && \
    wget https://gist.githubusercontent.com/matlabbe/a412cf7c4627253874f81a00745a7fbb/raw/accc3acf465d1ffd0304a46b17741f62d4d354ef/opengv_disable_march_native.patch && \
    git apply opengv_disable_march_native.patch && \
    mkdir build && \
    cd build && \
    cmake -DCMAKE_BUILD_TYPE=Release .. && \
    make -j$(nproc) && \
    make install && \
    cd && \
    rm -r opengv

RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# ros2 seems not sourcing by default its multi-arch folders
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/ros/humble/lib/x86_64-linux-gnu:/opt/ros/humble/lib/aarch64-linux-gnu

# gtsam v4.2.0
RUN mkdir -p /opt/raya_os/repos/gtsam && \
    cd /opt/raya_os/repos/gtsam && \
    git init && \
    git remote add origin https://github.com/borglab/gtsam && \
    git fetch --depth 1 --verbose --progress origin 4f66a491ffc83cf092d0d818b11dc35135521612 && \
    git checkout FETCH_HEAD && \
    cd /opt/raya_os/repos/gtsam && \
    mkdir build && cd build && \
    cmake -DGTSAM_BUILD_WITH_MARCH_NATIVE=ON -DGTSAM_USE_SYSTEM_EIGEN=ON .. && \
    make -j$([[ $CI == "true" ]] && echo $(($(nproc) > 1 ? $(nproc) : 1)) || echo $(((($(nproc)-1)) > 1 ? (($(nproc)-1)) : 1))) && \
    make install && \
    rm -r /opt/raya_os/repos/

# libnabo v1.0.7
RUN mkdir -p /opt/raya_os/repos/libnabo && \
    cd /opt/raya_os/repos/libnabo && \
    git init && \
    git remote add origin https://github.com/ethz-asl/libnabo && \
    git fetch --depth 1 --verbose --progress origin d4f45e2b2f9b811344cd5002346b9fb52ac2520e && \
    git checkout FETCH_HEAD && \
    cd /opt/raya_os/repos/libnabo && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$([[ $CI == "true" ]] && echo $(($(nproc) > 1 ? $(nproc) : 1)) || echo $(((($(nproc)-1)) > 1 ? (($(nproc)-1)) : 1))) && \
    make install && \
    rm -r /opt/raya_os/repos/

# libpointmatcher v1.3.1
RUN mkdir -p /opt/raya_os/repos/libpointmatcher && \
    cd /opt/raya_os/repos/libpointmatcher && \
    git init && \
    git remote add origin https://github.com/ethz-asl/libpointmatcher && \
    git fetch --depth 1 --verbose --progress origin eaece708ceda032501568563a91eeb3d71a5ca8d && \
    git checkout FETCH_HEAD && \
    cd /opt/raya_os/repos/libpointmatcher && \
    mkdir build && cd build && \
    cmake .. && \
    make -j$([[ $CI == "true" ]] && echo $(($(nproc) > 1 ? $(nproc) : 1)) || echo $(((($(nproc)-1)) > 1 ? (($(nproc)-1)) : 1))) && \
    make install && \
    rm -r /opt/raya_os/repos/

# g2o v20201223_git
RUN mkdir -p /opt/raya_os/repos/g2o && \
    cd /opt/raya_os/repos/g2o && \
    git init && \
    git remote add origin https://github.com/RainerKuemmerle/g2o && \
    git fetch --depth 1 --verbose --progress origin b1ba729aa569267e179fa2e237db0b3ad5169e2e && \
    git checkout FETCH_HEAD && \
    cd /opt/raya_os/repos/g2o && \
    mkdir build && cd build && \
    cmake -DBUILD_WITH_MARCH_NATIVE=OFF -DG2O_BUILD_APPS=OFF -DG2O_BUILD_EXAMPLES=OFF -DG2O_USE_OPENGL=OFF .. && \
    make -j$([[ $CI == "true" ]] && echo $(($(nproc) > 1 ? $(nproc) : 1)) || echo $(((($(nproc)-1)) > 1 ? (($(nproc)-1)) : 1))) && \
    make install && \
    rm -r /opt/raya_os/repos/

# RTABMAP (UR VERSION)
## gary branch 18 Jan 2024: 9362f744f683e2998b814b1247135a8f322e4dca
RUN source /ros_entrypoint.sh && \
    cd /root && \
    git clone https://github.com/unlimited-robotics/rtabmap && \
    cd rtabmap/ && \
    git checkout 9362f744f683e2998b814b1247135a8f322e4dca && \
    cd build/ && \
    cmake -DWITH_OPENGV=ON .. && \
    make -j$([[ $CI == "true" ]] && echo $(($(nproc) > 1 ? $(nproc) : 1)) || echo $(((($(nproc)-1)) > 1 ? (($(nproc)-1)) : 1))) && \
    make install && \
    cd ../.. && \
    rm -rf rtabmap && \
    ldconfig

# RTABMAP_ROS (UR VERSION)
## 3.7.9.dev: cd22989d3db9aca76316884a3fbf68040e450806
# Perception PCL:
## 2.4.1:  2b82545af3fda19eaa9bbed2a0f5d517bf23103f
RUN apt-get update && mkdir -p ${ROS_ROOT}/src && cd ${ROS_ROOT}/src && \
    git clone https://github.com/unlimited-robotics/rtabmap_ros && cd rtabmap_ros && git checkout 1291afba4c6c20dd6dfb5bc218402da30f8fa90d && cd .. && \
    git clone https://github.com/ros-perception/perception_pcl && cd perception_pcl && git checkout 2b82545af3fda19eaa9bbed2a0f5d517bf23103f && cd .. &&\
    source ${ROS_ROOT}/install/setup.bash && \
    cd ${ROS_ROOT} && \
    colcon build --parallel-workers 1 --event-handlers console_direct+ --merge-install --cmake-args -DRTABMAP_SYNC_MULTI_RGBD=ON -DCMAKE_BUILD_TYPE=Release && \
    rm -Rf src build log ros2.humble.ros_base.rosinstall && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean
