cd /src && git  clone --depth 1  https://github.com/llvm/llvm-project.git



cd /src/llvm-project && mkdir -p build 
pref=/home/ths/.local/lib/python3.6/site-packages/PySide6/Qt/lib
cd /src/llvm-project/build && cmake -G Unix Makefiles -DLLVM_ENABLE_PROJECTS='clang;libcxx;libcxxabi;lldb;compiler-rt;lld' -DCMAKE_INSTALL_PREFIX=$pref ../llvm