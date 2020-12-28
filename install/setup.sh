#!/bin/bash
set -e
mkdir -p /src/makaronLab/build/editor
if [ -e mLabEditor ]; then
	mv mLabEditor /src/makaronLab/build/editor/
fi
if [ ! -e ~/Desktop ]; then
	mkdir -p ~/Desktop  
fi
cp makaronLab.desktop ~/Desktop
if [ -e plugins ]; then
	mv plugins /src/makaronLab/build/plugins
fi
if [ -e lib ]; then
	mv lib /src/makaronLab/build/lib
fi
if [ -e packages ]; then
	mv packages /src/makaronLab/packages
fi
ln -sf /src/makaronLab/packages /src/packages 
cd /src/makaronLab/build/editor && ./mLabEditor

