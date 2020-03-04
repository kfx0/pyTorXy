#!/bin/bash

sudo apt update
sudo apt install python-tk python3-tk python-pil python3-pil tor torsocks obfs4proxy privoxy

echo -n -e '\n>tor is'
if(systemctl is-active tor)
then
systemctl stop tor
fi

echo -n -e '\n>privoxy is'
if(systemctl is-active privoxy)
then
systemctl stop privoxy
fi

echo -n -e '\n>tor service is'
if(systemctl is-enabled tor)
then	
systemctl disable tor
fi

echo -n -e '\n>privoxy service is'
if(systemctl is-enabled privoxy)
then
systemctl disable privoxy
fi

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

echo  "[Desktop Entry]
Version=1.0.0
Type=Application
Terminal=false
Name= pyTorXy
Comment=Python base Tor and Privoxy GUI
Exec= bash '"$SCRIPTPATH"/Python GUI/pytorxy.sh'
Icon= "$SCRIPTPATH"/Python GUI/logo.png
Categories=Network" >> pytorxy.desktop

chmod +x $SCRIPTPATH/pytorxy.desktop
chmod +x $SCRIPTPATH/'Python GUI/pytorxy.sh'
chmod +x $SCRIPTPATH/'Python GUI/pytorxy.py'
cp pytorxy.desktop '/home/'$USER'/.local/share/applications/'
clear
echo 'install successfully!'
