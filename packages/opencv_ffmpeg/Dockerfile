#---
# name: opencv_ffmpeg
# group: core
# depends: [cuda, cudnn, python, numpy, ffmpeg]
# postfix: 4.7.0
#---
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

COPY loadsave.cpp /root

RUN apt-get update && \
    apt-get install -y \
        libgtk2.0-dev \
        libeigen3-dev \
        liblapack-dev \
        && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean

RUN mkdir -p /opt/opencv && \
    cd /opt/opencv && \
    cd /opt/opencv && \
    wget -O opencv.zip https://github.com/opencv/opencv/archive/4.7.0.zip && \
    wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.7.0.zip && \
    unzip opencv.zip && \
    unzip opencv_contrib.zip && \
    mv opencv-4.7.0  opencv && \
    mv opencv_contrib-4.7.0 opencv_contrib && \
    rm opencv.zip && \
    rm opencv_contrib.zip && \
    mv /root/loadsave.cpp opencv/modules/imgcodecs/src/loadsave.cpp && \
    mkdir -p /opt/opencv/opencv/build && \ 
    cd /opt/opencv/opencv/build && \
    cmake \
        -D CMAKE_BUILD_TYPE=RELEASE \
        -D CMAKE_INSTALL_PREFIX=/usr \
        -D OPENCV_EXTRA_MODULES_PATH=/opt/opencv/opencv_contrib/modules \
        -D EIGEN_INCLUDE_PATH=/usr/include/eigen3 \
        -D WITH_OPENCL=OFF \
        -D WITH_CUDNN=ON \
        -D WITH_CUBLAS=ON \
        -D ENABLE_FAST_MATH=ON \
        -D WITH_QT=OFF \
        -D WITH_OPENMP=ON \
        -D BUILD_TIFF=ON \
        -D WITH_FFMPEG=ON \
        -D WITH_GSTREAMER=ON \
        -D WITH_TBB=ON \
        -D BUILD_TBB=ON \
        -D BUILD_TESTS=OFF \
        -D WITH_EIGEN=ON \
        -D WITH_V4L=ON \
        -D WITH_LIBV4L=ON \
        -D OPENCV_ENABLE_NONFREE=OFF \
        -D INSTALL_C_EXAMPLES=OFF \
        -D INSTALL_PYTHON_EXAMPLES=OFF \
        -D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
        -D OPENCV_GENERATE_PKGCONFIG=ON \
        -D BUILD_EXAMPLES=OFF \
        -D BUILD_opencv_aruco=ON \
        -D WITH_CUDA=ON \
        -D CUDA_ARCH_BIN=5.3 \
        -D CUDA_ARCH_PTX="" \
        -D CUDA_FAST_MATH=ON \
        -D OPENCV_DNN_CUDA=ON \
        .. && \
    make -j$([[ $CI == "true" ]] && echo $(($(nproc) > 1 ? $(nproc) : 1)) || echo $(((($(nproc)-1)) > 1 ? (($(nproc)-1)) : 1))) && \
    make install && \
    cp python_loader/setup.py /usr/lib/python3/dist-packages/cv2/ && \
    cd /usr/lib/python3/dist-packages/cv2/ && \
    sed -i "s/package_name = 'opencv'/package_name = 'opencv-python'/" setup.py && \
    sed -i "s/packages=setuptools.find_packages(),/packages=['cv2'], package_dir={'cv2':'.'},/" setup.py && \
    python3 -m pip install . && \
    ldconfig && \
    rm -rf /opt/opencv
