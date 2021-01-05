#!/bin/bash
set -e
echo "[mLab] Installing toolchain ..."
sudo apt update -y && sudo apt install -y curl libcurl4-openssl-dev libssl-dev build-essential manpages-dev software-properties-common
sudo add-apt-repository -y ppa:ubuntu-toolchain-r/test && sudo apt install -y gcc-7 g++-7 gcc-8 g++-8 
sudo apt-get install -y cmake qtbase5-dev qtdeclarative5-dev qtcreator

echo "[mLab] Installing sources /external tools(MLAB_BS_SKIP_SRC=$MLAB_BS_SKIP_SRC) ..."
if [[ -z "${MLAB_BS_SKIP_SRC}" ]]; then
if [ -e /src/makaronLab ]; then
	cd 	/src/makaronLab && git pull
else 
	mkdir -p /src && cd /src && git clone http://github.com/virtimus/makaronLab 
fi	
if [ ! -e /src/tinyemu-2019-12-21 ]; then
	cd /src && wget https://bellard.org/tinyemu/tinyemu-2019-12-21.tar.gz && tar -xvf tinyemu-2019-12-21.tar.gz
fi
cd /src/makaronLab/externalTools/tinyEMU && echo '#define MAX_XLEN 32' > riscv_cpu32.c && cat riscv_cpu.c >> riscv_cpu32.c && echo '#define MAX_XLEN 64' > riscv_cpu64.c && cat riscv_cpu.c >> riscv_cpu64.c && echo '#define MAX_XLEN 128' > riscv_cpu128.c && cat riscv_cpu.c >> riscv_cpu128.c
cd /src/makaronLab && git submodule update --init --recursive && cd externalTools/spaghetti &&  git pull origin master
cp /src/makaronLab/res/CMakeLists.txt  /src/makaronLab/externalTools/spaghetti/plugins/CMakeLists.txt 
cd /src/makaronLab/externalTools/spaghetti/plugins && ln -sf /src/makaronLab/components components
#path to packages fixed by now
ln -sf /src/makaronLab/packages /src/packages
cd /src/makaronLab/externalTools/spaghetti/vendor &&  ln -sf /src/makaronLab/externalTools/chips chips 
clear && cd /src/makaronLab && mkdir -p build && cd build && cmake .. && make

echo "[mLab] Starting mLabEditor ..."
cd /src/makaronLab && mkdir -p packages && cd build/editor && ./mLabEditor
fi #MLAB_BS_SKIP_SRC