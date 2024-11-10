#!/bin/bash

echo "[Desktop Entry]
Name=$2
Comment=Executable jar file
Exec=java -jar $1
Icon=$3
Terminal=false
Type=Application
Categories=$4;
" > /home/agustin/Desktop/"$2".desktop

ln /home/agustin/Desktop/"$2".desktop /home/agustin/.local/share/applications/"$2".desktop
