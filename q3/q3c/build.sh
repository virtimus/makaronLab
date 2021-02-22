#!/bin/bash

#ln -sf /src/makaronLab/libmakaron/include /src/makaronLab/q3/q3c/include
ln -sf /src/makaronLab/externalTools /src/makaronLab/q3/q3c/extools

sudo apt-get install libglfw3 libglfw3-dev
sudo apt-get install python3-dev   

#python3 setup.py build
sudo CC=gcc python3 setup.py install