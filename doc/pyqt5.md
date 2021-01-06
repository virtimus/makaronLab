
#@refs: https://www.riverbankcomputing.com/static/Docs/PyQt5/designer.html#using-the-generated-code



#@results: failed - to complicated not my current target to build libc from scratch
#Alternative:pyside


#        Python: 3.6+

#       Qt: 6.0+ is recommended

#        libclang: The libclang library, recommended: version 10 for 6.0+. Prebuilt versions of it can be downloaded here.

#        CMake: 3.1+ is needed.



#@refs:https://wiki.qt.io/Qt_for_Python
pip install pyside6
pyside6-uic editor.ui > ui_editor.py
problem - rror: /home/ths/.local/lib/python3.6/site-packages/PySide6/uic: /lib/x86_64-linux-gnu/libc.so.6: version `GLIBC_2.28' not found (required by /home/ths/.local/lib/python3.6/site-packages/PySide6/Qt/lib/libQt6Core.so.6)
sudo ln -s /lib/x86_64-linux-gnu/libc-2.27.so /lib/x86_64-linux-gnu/libc-2.28.so
cd /home/ths/.local/lib/python3.6/site-packages/PySide6/Qt/lib
sudo apt install p7zip-full p7zip-rar #stupid 
wget http://download.qt.io/development_releases/prebuilt/libclang/libclang-release_110-based-linux-Ubuntu18.04-gcc9.3-x86_64.7z

failed - to complicated not my current target to build libc from scratch