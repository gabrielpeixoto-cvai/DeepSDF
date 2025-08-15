#!/bin/bash
git clone https://github.com/jlblancoc/nanoflann.git
cd nanoflann
mkdir build && cd build && cmake ..
make && make test
make install
