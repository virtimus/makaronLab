#!/bin/bash
python3 -m pip install --upgrade pip \
 && python3 -m pip install PyQt5 \
 && pyuic5 -o ui_imagedialog.py ../externalTools/spaghetti/libspaghetti/source/ui/editor.ui