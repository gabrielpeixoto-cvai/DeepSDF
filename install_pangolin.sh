#!/bin/bash
git clone --recursive https://github.com/stevenlovegrove/Pangolin.git -b v0.6
cd Pangolin

# Install dependencies (as described above, or your preferred method)
#./scripts/install_prerequisites.sh recommended

apt update
apt install -y libgl1-mesa-dev libwayland-dev libxkbcommon-dev wayland-protocols
apt install -y libegl1-mesa-dev libc++-dev libepoxy-dev libglew-dev libeigen3-dev cmake g++
apt install -y ninja-build libjpeg-dev libpng-dev catch2
apt install -y libavcodec-dev libavutil-dev libavformat-dev libswscale-dev libavdevice-dev
apt install -ylibdc1394-dev libraw1394-dev libopenni-dev python3-dev

# Configure and build
cmake -B build
cmake --build build

# GIVEME THE PYTHON STUFF!!!! (Check the output to verify selected python version)
cmake --build build -t pypangolin_pip_install

cmake --install build
