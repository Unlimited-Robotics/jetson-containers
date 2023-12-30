#---
# name: ffmpeg_4_2
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

RUN mkdir -p /root/ffmpeg_build && \
    cd /root/ffmpeg_build && \
    wget https://repo.download.nvidia.com/jetson/ffmpeg/pool/main/f/ffmpeg/ffmpeg_4.2.7-nvidia.tar.xz && \
    tar -xvf ffmpeg_4.2.7-nvidia.tar.xz && \
    chmod 775 -R /root/ffmpeg_build && \
    cd ./ffmpeg && \
    ./configure \
        --prefix=/usr \
        --enable-nvv4l2dec \
        --enable-libv4l2 \
        --enable-shared \
        --extra-libs='-L/usr/lib/aarch64-linux-gnu/tegra -lnvbufsurface -lnvbufsurftransform' \
        --extra-cflags='-I/usr/src/jetson_multimedia_api/include/ -I/usr/local/cuda/include' \
        --extra-ldflags=-L/usr/local/cuda/lib64 \
        --extra-version=1ubuntu0.1 \
        --toolchain=hardened \
        --libdir=/usr/lib/aarch64-linux-gnu \
        --incdir=/usr/include/aarch64-linux-gnu \
        --enable-gpl \
        --disable-stripping \
        --disable-filter=resample \
        --enable-avisynth \
        --enable-gnutls \
        --enable-ladspa \
        --enable-libaom \
        --enable-libass \
        --enable-libbluray \
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
        --enable-libopenjpeg \
        --enable-libopenmpt \
        --enable-libopus \
        --enable-libpulse \
        --enable-librsvg \
        --enable-librubberband \
        --enable-libshine \
        --enable-libsnappy \
        --enable-libsoxr \
        --enable-libspeex \
        --enable-libssh \
        --enable-libsrt \
        --enable-libtheora \
        --enable-libtwolame \
        --enable-libvidstab \
        --enable-libvorbis \
        --enable-libvpx \
        --enable-libwavpack \
        --enable-libwebp \
        --enable-libx265 \
        --enable-libxml2 \
        --enable-libxvid \
        --enable-libzmq \
        --enable-libzvbi \
        --enable-lv2 \
        --enable-omx \
        --enable-openal \
        --enable-opencl \
        --enable-opengl \
        --enable-sdl2 \
        --enable-libdc1394 \
        --enable-libdrm \
        --enable-chromaprint \
        --enable-frei0r \
        --enable-libx264 \
        --enable-shared \
    && \
    make -j8 && \
    make install && \
    ldconfig && \
    rm -rf /opt/ffmpeg_build