#---
# name: ffmpeg
# group: core
# depends: [build-essential, cmake]
#---
ARG BASE_IMAGE
FROM ${BASE_IMAGE}

ARG DEBIAN_FRONTEND=noninteractive

#This symbolic link is needed to use the streaming features on Jetson inside a container
RUN ln -sf /usr/lib/aarch64-linux-gnu/tegra/libv4l2.so.0 /usr/lib/aarch64-linux-gnu/libv4l2.so

RUN echo "deb https://repo.download.nvidia.com/jetson/ffmpeg main main" |  sudo tee -a /etc/apt/sources.list.d/ffmpeg_nvidia.list && \
	echo "deb-src https://repo.download.nvidia.com/jetson/ffmpeg main main" |  sudo tee -a /etc/apt/sources.list.d/ffmpeg_nvidia.list && \
	apt purge ffmpeg || true && \
    apt-get update && \
    apt-get build-dep -y ffmpeg &&\
    apt install -y --no-install-recommends \
        libc6 \
        libc6-dev \
        libchromaprint-dev \
        libass-dev \
        libfreetype6-dev \
        libgnutls28-dev \
        libsdl2-dev \
        libtool \
        libva-dev \
        libvdpau-dev \
        libvorbis-dev \
        libxcb1-dev \
        libxcb-shm0-dev \
        libxcb-xfixes0-dev \
        libchromaprint-dev \
        frei0r-plugins-dev \
        zlib1g-dev \
        libgnutls28-dev \
        libunistring-dev \
        libsrt-dev \
        libx264-dev \
        libx265-dev \
        libnuma-dev \
        libvpx-dev \
        libfdk-aac-dev \
        libmp3lame-dev \
        libopus-dev \
        libaom-dev \
        ladspa-sdk \
        liblilv-dev \
        libbluray-dev \
        libiec61883-dev \
        libbs2b-dev \
        libcodec2-dev \
        libcaca-dev \
        libdrm-dev \
        flite1-dev \
        libgme-dev \
        libgsm1-dev \
        libmysofa-dev \
        libopenmpt-dev \
        librabbitmq-dev \
        librsvg2-dev \
        librubberband-dev \
        libshine-dev \
        libsnappy-dev \
        libsoxr-dev \
        libssh-dev \
        libspeex-dev \
        libtwolame-dev \
        libvidstab-dev \
        libxvidcore-dev \
        libzvbi-dev \
        libopenal-dev \
        ocl-icd-opencl-dev \
        libomxil-bellagio-dev \
        libpocketsphinx-dev \
        libjack-dev \
        libcdio-dev \
        libtheora-dev \
        libwebp-dev \
        libdc1394-22-dev \
        libopenjp2-7-dev \
        libv4l-dev \
        libwavpack-dev \
        libzmq3-dev \
        && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get clean 

RUN mkdir -p /opt/ffmpeg_build && \
    cd /opt/ffmpeg_build && \
    git clone https://git.videolan.org/git/ffmpeg/nv-codec-headers.git && \
    cd nv-codec-headers && make install && cd .. && \
    wget -O ffmpeg.tar.bz2 https://ffmpeg.org/releases/ffmpeg-5.1.tar.bz2 && \
    tar -xvf ffmpeg.tar.bz2 && \
    cd ./ffmpeg-5.1 && \
    ./configure \
        --enable-gpl \
        --enable-nonfree \
        --enable-cuda-nvcc \
        --enable-ladspa \
        --enable-libaom \
        --enable-libass \
        --enable-libbs2b \
        --enable-libcaca \
        --enable-libcodec2 \
        --enable-libflite \
        --enable-libfontconfig \
        --enable-libfreetype \
        --enable-libfribidi \
        --enable-libgme \
        --enable-libgsm \
        --enable-libjack \
        --enable-libmp3lame \
        --enable-libmysofa \
        --enable-libopenmpt \
        --enable-libopus \
        --enable-libpulse \
        --enable-librubberband \
        --enable-libshine \
        --enable-libsnappy \
        --enable-libsoxr \
        --enable-libspeex \
        --enable-libsrt \
        --enable-libssh \
        --enable-libtheora \
        --enable-libtwolame \
        --enable-libvidstab \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libwebp \
        --enable-libx265 \
        --enable-libxvid \
        --enable-libzvbi \
        --enable-lv2 \
        --enable-omx \
        --enable-openal \
        --enable-opencl \
        --enable-opengl \
        --enable-sdl2 \
        --enable-librsvg \
        --enable-libdrm \
        --enable-chromaprint \
        --enable-frei0r \
        --enable-libx264 \
        --extra-cflags=-I/usr/local/cuda/include \
        --extra-ldflags=-L/usr/local/cuda/lib64 \
        --disable-static \
        --enable-shared && \
    make -j8 && \
    make install && \
    ldconfig && \
    rm -rf /opt/ffmpeg_build