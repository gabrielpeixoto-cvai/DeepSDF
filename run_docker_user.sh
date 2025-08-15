#!/bin/bash
container_name="$1"
image_name="$2"
use_gpu="$3"

echo "Running with parameters:"
echo "Container name: $container_name"
echo "Image name: $image_name"
echo "use GPU: $use_gpu"

if [ ! "$(docker ps -q -f name=$container_name)" ]; then
  if [ "$(docker ps -aq -f status=exited -f name=$container_name)" ]; then
    echo "Container already exists attaching to it: $container_name"
    # cleanup
    docker start $container_name
    docker attach $container_name
  else
    echo "Building container from image $image_name"
    xhost +local:
    docker run -it --net=host \
      --gpus all \
      --privileged \
      --user=$(id -u) \
      -e DISPLAY=$DISPLAY \
      -e QT_GRAPHICSSYSTEM=native \
      -e CONTAINER_NAME=$container_name \
      -e USER=$USER \
      --workdir=/home/$USER \
      -v "/tmp/.X11-unix:/tmp/.X11-unix" \
      -v "/etc/group:/etc/group:ro" \
      -v "/etc/passwd:/etc/passwd:ro" \
      -v "/etc/shadow:/etc/shadow:ro" \
      -v "/etc/sudoers.d:/etc/sudoers.d:ro" \
      -v "/etc/sudoers:/etc/sudoers" \
      -v "/home/$USER/:/home/$USER/" \
      -v "/dev:/dev" \
      -v "/var/run/udev:/var/run/udev" \
      -v "/data:/data" \
      -v "/var/log/cr:/var/log/cr" \
      --name=$container_name \
      $image_name
  fi
fi
