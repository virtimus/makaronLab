#@refs: https://dev-docs.kicad.org/contribute/
	https://dev-docs.kicad.org/build/
	https://stackoverflow.com/questions/1056051/how-do-you-call-python-code-from-c-code

cd /src/makaronLab/externalTools && git clone --depth 1 https://gitlab.com/kicad/code/kicad.git

#adddditional preps for ubuntu 18.04 (?(swig3.0)) - libngspice as shared lib)
sudo apt install -y libglew-dev libglm-dev libcairo2-dev autoconf automake libboost-all-dev
sudo apt install -y bison flex libtool swig
cd /src/makaronLab/externalTools/kicad/scripting/build_tools && chmod +x get_libngspice_so.sh && ./get_libngspice_so.sh && sudo ./get_libngspice_so.sh install

sudo apt install build-essential libboost-dev libboost-system-dev libboost-test-dev libboost-filesystem-dev cmake freeglut3-dev libglew-dev libglm-dev liboce-foundation-dev liboce-ocaf-dev python-wxgtk3.0-dev libwxgtk3.0-gtk3-dev swig3.0 doxygen graphviz libcurl4-openssl-dev libcairo-dev libpython3-dev libssl-dev

#Python 3.6
sudo apt install python3.6 
ls -al /usr/bin/py*
sudo ln -sf  /usr/bin/python3.6 /usr/bin/python
sudo ln -sf  /usr/bin/python3.6-config /usr/bin/python-config

sudo apt-get install build-essential 

sudo apt-get install libgtk-3-0 libgtk-3-dev 
#sudo apt-get install python-wxtools
pip install wheel && pip install pygame
pip install -U wxPython

#removing wx30* libs
apt list --installed | grep wx
 
sudo apt remove libwxbase3.0* libwxgtk3.0* python-wxgtk3.0* wx-common wx3.0-headers

#wxwidgets from trunk https://github.com/wxWidgets/wxWidgets
cd /src && git clone --depth 1 https://github.com/wxWidgets/wxWidgets 
cd /src/wxWidgets && mkdir -p build && cd build && git submodule update --init
cd /src/wxWidgets/build && ../configure --with-gtk  
cd /src/wxWidgets/build && make && sudo make install && sudo ldconfig

#@ref: https://dev-docs.kicad.org/build/linux/
cd /src/makaronLab/externalTools/kicad && mkdir -p build/release && mkdir build/debug # Optional for debug build.
cd /src/makaronLab/externalTools/kicad/build/release && cmake -DKICAD_USE_EGL=on -DKICAD_SCRIPTING_PYTHON3=enabled -DKICAD_SCRIPTING_WXPYTHON_PHOENIX=enabled -DCMAKE_BUILD_TYPE=Release ../../ && make  && sudo make install

