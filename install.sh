#!/bin/bash

sudo apt update
sudo apt install python3-tk python3-pil python3-pil.imagetk tor torsocks obfs4proxy privoxy

echo -n -e '\n>tor is'
if(systemctl is-active tor)
then
systemctl stop tor
echo 'Now Stopped!'
fi

echo -n -e '\n>privoxy is'
if(systemctl is-active privoxy)
then
systemctl stop privoxy
echo 'Now Stopped!'
fi

echo -n -e '\n>tor service is'
if(systemctl is-enabled tor)
then	
systemctl disable tor
echo 'Now Disabled!'
fi

echo -n -e '\n>privoxy service is'
if(systemctl is-enabled privoxy)
then
systemctl disable privoxy
echo 'Now Disabled!'
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

sudo chown root:root $SCRIPTPATH/pytorxy.desktop
sudo chown root:root $SCRIPTPATH/'Python GUI/pytorxy.sh'
sudo chown root:root $SCRIPTPATH/'Python GUI/pytorxy.py'
sudo chmod 7777 $SCRIPTPATH/pytorxy.desktop
sudo chmod 7777 $SCRIPTPATH/'Python GUI/pytorxy.sh'
sudo chmod 7777 $SCRIPTPATH/'Python GUI/pytorxy.py'
sudo cp pytorxy.desktop '/usr/share/applications/'

if [[ -z $(grep '[^[:space:] \n]' "Tor Config/Bridges list") ]] ; then
  > "Tor Config/Bridges list"
fi

if [[ -z $(grep '[^[:space:] \n]' "Tor Config/obfs4 list") ]] ; then
  > "Tor Config/obfs4 list"
fi

echo 'finish installation!'
