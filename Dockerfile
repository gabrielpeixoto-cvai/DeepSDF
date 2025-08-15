FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04


# setup timezone
RUN echo 'Etc/UTC' > /etc/timezone && \
    ln -s /usr/share/zoneinfo/Etc/UTC /etc/localtime && \
    apt-get update && \
    apt-get install -q -y --no-install-recommends tzdata && \
    rm -rf /var/lib/apt/lists/*

# install packages
RUN apt-get update && apt-get install -q -y --no-install-recommends \
    dirmngr \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*

# setup environment
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

# install dependencies
RUN apt-get update -q && \
    apt-get dist-upgrade -q -y && \
    apt-get install -y \
    build-essential cmake \
    libgtest-dev \
    libeigen3-dev \
    ninja-build \
    libcli11-dev && \
    rm -rf /var/lib/apt/lists/*


#install pytorch
RUN apt-get update -q && \
    apt-get dist-upgrade -q -y && \
    apt-get install -y python3-pip wget git && \
    rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
RUN python3 -m pip install matplotlib open3d pyopengl trimesh scikit-image plyfile

RUN echo Installing deps
# install pangolin

ADD install_pangolin.sh .
RUN bash install_pangolin.sh

# install nanoflann
ADD install_nanoflann.sh .
RUN bash install_nanoflann.sh
