# pyTorXy
Python base Tor and Privoxy GUI

This Python App will help new users of Ubuntu to use tor and privoxy easily in a simple way.

# How to install

## Step 1.
clone or download this repository (<a href="https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository">read</a> how to clone or download file in Ubuntu)

If you download it, Extract zip file in /home/$USER/.
#### CAUTION: Do not Extract it other disk partitions!

## Step 2.

Run install.sh file. To run it open terminal and write command below:

    $./install.sh

This bash file will automatically install needed python library, Tor, TorSocks, Obfs4proxy and Privoxy

(For super-new users: $ is not part of command)

## Step 3.

pyTorXy install successfully. Now leave the directory and use pyTorXy easily with shortcut in applications.

In the pyTorXy directory a pytorxy.desktop file is created which is anouther shortcut. You can run it like a shortcut, copy it anywhere you want to access pyTorXy easily.

# How to Use

## Add or Remove Bridge/Obfs4
At first you need to know how to get and add tor bridge or obsf4 transport.

To get bridge send an email to `bridges@torproject.org`. No subject needed, Just write `get bridge` for bridge and `get transport obfs4` to get obfs4 from torproject. Copy full line bridge or obsf4 e.g.:

for obfs4:
    
    obfs4 X.X.X.X:PORT abcdefghijklmn cert=opqrstuvwxyz iat-mode=0

for bridges:

    X.X.X.X:PORT abcdefghijklmn
    
Now open application, Go to Tor Config -> Add/Remove Bridge. Paste obfs4 in "Obfs4" tab and bridge in "Bridge" tab and Add them.

In this window you can see list of bridges and obfs4 transports which can selected to remove.

## Set Tor Bridge/Obsf4 and Config Tor Port
In application, Go to Tor Config -> Tor Configuaration. In this window you can config tor port (from = 1000 to 65535), Tor Exit Node and Bridge. you can select you prefer to use bridge/obfs4 or not.

## Config Privoxy Port
In Application, Go to Privoxy Config -> Privoxy Configuration. You can select port of privoxy easily (from = 1000 to 65535).

#### CAUTION: Do not select Privoxy port same as Tor port

## Use Tor Socks or Privoxy HTTP proxy
Tor make socks5 proxy which could use in Telegram desktop application. HTTP proxy provided by Privoxy could proxy whole device (read it from <a href="https://help.ubuntu.com/stable/ubuntu-help/net-proxy.html.en">here</a> or <a href="https://medium.com/@krish.raghuram/setting-up-proxy-in-ubuntu-95058da0b2d4">here</a>) or applications which could use http proxy. Both proxy addresses are `127.0.0.1`. Port of proxies are as you define in config.
