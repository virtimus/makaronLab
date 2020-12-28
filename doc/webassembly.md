
#@refs: https://gist.github.com/WesThorburn/00c47b267a0e8c8431e06b14997778e4

cd /src && git clone https://github.com/emscripten-core/emsdk.git
cd /src/emsdk && ./emsdk install latest && ./emsdk activate latest && source ./emsdk_env.sh

echo 'source "/src/emsdk/emsdk_env.sh"' >> ~/.bash_profile

export PATH=$PATH:/src/emsdk && echo 'export PATH=$PATH:/src/emsdk' >> ~/.bash_profile


CMAKE_TOOLCHAIN_FILE=/src/emsdk/upstream/emscripten/cmake/Modules/Platform/Emscripten.cmake


Compile to WASM (default)

cd build  
emcmake cmake ..  
make

Compile to JS

cd build  
emcmake cmake .. -DJS_ONLY=ON  
make

After Editing Files

make

After Adding/Removing Files

emcmake cmake ..  
make
