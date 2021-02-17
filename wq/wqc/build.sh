#!/bin/bash

#ln -sf /src/makaronLab/libmakaron/include /src/makaronLab/wq/wqc/include
ln -sf /src/makaronLab/externalTools /src/makaronLab/wq/wqc/extools

sudo apt-get install libglfw3 libglfw3-dev
sudo apt-get install python3-dev   

#python3 setup.py build
sudo python3 setup.py install