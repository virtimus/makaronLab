#build options	@ref: https://dev-docs.kicad.org/build/getting-started/
KICAD_SCRIPTING (enabled) Scripting Support to enable building the Python scripting support into Pcbnew. This options is enabled by default, and will disable all other KICAD_SCRIPTING_* options when it is disabled.
KICAD_SCRIPTING_PYTHON3 (disabled) used to enable using Python 3 for the scripting support instead of Python 2. This option is disabled by default
KICAD_SCRIPTING_MODULES (enabled) enable building and installing the Python modules supplied by KiCad. This option is enabled by default
KICAD_SCRIPTING_WXPYTHON (enabled) used to enable building the wxPython interface into Pcbnew including the wxPython console. This option is enabled by default,
KICAD_SCRIPTING_WXPYTHON_PHOENIX (disabled) used to enable building the wxPython interface with the new Phoenix binding instead of the legacy one. This option is disabled by default
KICAD_SCRIPTING_ACTION_MENU (enabled) allows Python scripts to be added directly to the Pcbnew menu. This option is enabled by default,
KICAD_SPICE (enabled) used to control if the Spice simulator interface for Eeschema is built. When this option is enabled, it requires [ngspice][] to be available as a shared library. This option is enabled by default.
KICAD_USE_OCE (enabled) used for the 3D viewer plugin to support STEP and IGES 3D models. Build tools and plugins related to OpenCascade Community Edition (OCE) are enabled with this option. When enabled it requires [liboce][] to be available, and the location of the installed OCE library to be passed via the OCE_DIR flag. This option is enabled by default.
KICAD_USE_EGL option switches the OpenGL backend from using X11 bindings to Wayland EGL bindings
KICAD_WIN32_DPI_AWARE option makes the Windows manifest file for KiCad use a DPI aware version, which tells Windows that KiCad wants Per Monitor V2 DPI awareness (requires Windows 10 version 1607 and later).
KICAD_USE_VALGRIND (disabled) option is used to enable Valgrind’s stack annotation feature in the tool framework. This provides the ability for Valgrind to trace memory allocations and accesses in the tool framework and reduce the number of false positives reported. This option is disabled by default.
KICAD_STDLIB_DEBUG and KICAD_STDLIB_LIGHT_DEBUG. Both these options are disabled by default, and only one should be turned on at a time with KICAD_STDLIB_DEBUG taking precedence.
KICAD_SANITIZE option enables Address Sanitizer support to trace memory allocations and accesses to identify problems. This option is disabled by default. The Address Sanitizer contains several runtime options to tailor its behavior that are described in more detail in its documentation.
KICAD_INSTALL_DEMOS option. You can also select where to install them with the KICAD_DEMOS variable. On Linux the demos are installed in $PREFIX/share/kicad/demos by default.


    Build all QA binaries: make qa_all

    Build a specific test: make qa_pcbnew

    Build all unit tests: make qa_all_tests

    Build all test tool binaries: make qa_all_tools
KiCad Build Version
git describe --dirty

KiCad Config Directory
On Linux this is located at ~/.config/kicad
This is set by specifying the KICAD_CONFIG_DIR string at compile time.

delta:KICAD_SCRIPTING_PYTHON3(enabled) KICAD_INSTALL_DEMOS (enabled)

```

cd /src/makaronLab/externalTools && git clone --depth 1 https://gitlab.com/kicad/code/kicad.git
```

#adddditional preps for ubuntu 18.04 (?(swig3.0))
sudo apt install -y libglew-dev libglm-dev libcairo2-dev autoconf automake libboost-all-dev
sudo apt install -y bison flex libtool swig
cd /src/makaronLab/externalTools/kicad/scripting/build_tools && chmod +x get_libngspice_so.sh && ./get_libngspice_so.sh && sudo ./get_libngspice_so.sh install


#OpenCascade Library - trying from libs(? is this ?) (ev. compile from source:https://github.com/tpaviot/oce
sudo apt install -y liboce-ocaf-dev liboce-foundation-dev liboce-ocaf11 liboce-visualization-dev liboce-visualization11


sudo apt-key adv --fetch-keys http://repos.codelite.org/CodeLite.asc
sudo apt-add-repository --remove 'deb http://repos.codelite.org/wx3.1.5/ubuntu/ bionic universe'
sudo apt-add-repository 'deb http://repos.codelite.org/wx3.1/ubuntu/ bionic universe'

libwxbase3.0


#@failed: wxWidgets @ref: http://wxwidgets.org/ - 3.0.2
sudo apt install -y wx-common wx3.0-headers wx3.0-i18n wxsqlite3-3.0-dbg wx3.0-examples wx3.0-doc
sudo apt install -y wxglade python-wxgtk3.0
sudo apt-get install libwxgtk-media3.0-dev gettext

#@ref:https://wiki.codelite.org/pmwiki.php/Main/WxWidgets30Binaries#toc2	
sudo apt-key adv --fetch-keys http://repos.codelite.org/CodeLite.asc
sudo apt-add-repository 'deb http://repos.codelite.org/wx3.0.5/ubuntu/ bionic universe'
sudo add-apt-repository --remove 'deb http://repos.codelite.org/wx3.0.5/ubuntu/ bionic universe'
#sudo apt-add-repository 'deb http://repos.codelite.org/wx3.0.2/ubuntu/ bionic release'
sudo apt-get update
sudo apt-get install libwxbase3.0-0-unofficial libwxbase3.1-dev libwxgtk3.1-0-unofficial libwxgtk3.1-dev wx3.1-headers wx-common libwxbase3.1-dbg libwxgtk3.1-dbg wx3.1-i18n wx3.1-examples wx3.1-doc 

sudo apt-get install -y libwxgtk-media3.1-dev libwxbase3.1unofficial3-dev libwxgtk3.1-dev 
 
 sudo apt-get update
#@failed-end above failed - from source

 
#Python 3.6
sudo apt install python3.6 
ls -al /usr/bin/py*
sudo ln -sf  /usr/bin/python3.6 /usr/bin/python
sudo ln -sf  /usr/bin/python3.6-config /usr/bin/python-config

sudo apt-get install build-essential libgtk-3 libgtk-3-dev 
sudo apt-get install python-wxtools
pip install wheel && pip install pygame
pip install -U wxPython

sudo apt install python-pip
python2.7 -m pip install wxpython
sudo ln -sf  /usr/bin/python2.7 /usr/bin/python
sudo ln -sf  /usr/bin/python2.7-config /usr/bin/python-config


#@ref: https://github.com/wxWidgets/wxWidgets/releases/tag/v3.0.2
#@failed: libgtkd-3-dev
sudo apt install -y libgtk2.0 libgtk2.0-dev
sudo apt-get remove libgtk2.0  libgtk2.0-dev
sudo apt-get install libgtkd-3 libgtkd-3-dev
cd /src && wget https://github.com/wxWidgets/wxWidgets/archive/v3.0.2.tar.gz 
cd /src && tar -xvf  v3.0.2.tar.gz #-C wxWidgets3.0.2
cd /src/wxWidgets-3.0.2 && mkdir -p buildgtk && cd buildgtk && ../configure -with-gtk
cd /src/wxWidgets-3.0.2/buildgtk && make && sudo make install && sudo ldconfig
wx-config --list
failed!
#@failed-end


sudo apt-get install libgtkd-3-0 libgtkd-3-dev
sudo apt-get remove libgtkd-3-0 libgtkd-3-dev
sudo apt install -y libgtk2.0 libgtk2.0-dev 
sudo wx-config --selected-config
sudo  update-alternatives --config wx-config
sudo wx-config --selected-config


cd /src && git clone --depth 1 https://gitlab.com/kicad/code/wxWidgets
cd /src/wxWidgets && mkdir -p build && cd build && ../configure --with-gtk #(2! 3 is failed!)
cd /src/wxWidgets/build && make && sudo make install && sudo ldconfig

 sudo apt-get install python-setuptools
 pip install wxpython
 
#problem with wxPython classic - get from source 
cd /src && wget https://deac-ams.dl.sourceforge.net/project/wxpython/wxPython/3.0.2.0/wxPython-src-3.0.2.0.tar.bz2
cd /src && tar -xvf wxPython-src-3.0.2.0.tar.bz2 
cd /src/wxPython-src-3.0.2.0 && ./configure && make && sudo make install

 
#@ref: https://dev-docs.kicad.org/build/linux/
```
cd /src/makaronLab/externalTools/kicad && mkdir -p build/release && mkdir build/debug # Optional for debug build.
cd /src/makaronLab/externalTools/kicad/build/release && cmake -DKICAD_SCRIPTING_WXPYTHON_PHOENIX=enabled -DCMAKE_BUILD_TYPE=Release ../../ && make  && sudo make install
```
cd /src/makaronLab/externalTools/kicad/build/release && rm CMakeCache.txt && cmake   -DCMAKE_BUILD_TYPE=Release -DKICAD_SCRIPTING_PYTHON3=enabled ../../ && make  && sudo make install

cd /src/makaronLab/externalTools/kicad/build/release && rm CMakeCache.txt && cmake

-DwxWidgets_CONFIG_OPTIONS=--toolkit=3.0.2.0/gtk3
KICAD_SCRIPTING_PYTHON3
KICAD_SCRIPTING_WXPYTHON_PHOENIX



KICAD_SCRIPTING_PYTHON3
====================================
=====================================