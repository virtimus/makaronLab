#!bin/bash
set -e
mkdir -p /src/makaronLab/build/editor
mv mLabEditor /src/makaronLab/build/editor/
if [ -e ~/Desktop/ ]; then
    mv makaronLab.desktop ~/Desktop/
fi
mv plugins /src/makaronLab/build/plugins
mv lib /src/makaronLab/build/lib
mv packages /src/makaronLab/packages
ln -sf /src/makaronLab/packages /src/packages 
cd /src/makaronLab/build/editor && ./mLabEditor

