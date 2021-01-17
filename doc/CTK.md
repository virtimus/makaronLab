 #@refs: https://github.com/commontk/CTK

sudo apt-get install -y libqt4-dev libqt4-dev-bin libqt4-opengl-dev libqtwebkit-dev qt4-linguist-tools qt4-qmake 
 
 
cd /src/makaronLab/externalTools  && git clone --depth 1 https://github.com/commontk/CTK
cd /src/makaronLab/externalTools/CTK && mkdir -p build && cd build && cmake .. && make