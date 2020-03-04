import time
import os
import subprocess
import signal
import threading
try:
	import Tkinter as tk
	import ttk
	import tkMessageBox
except:
	import tkinter as tk
	from tkinter import ttk
	from tkinter import messagebox as tkMessageBox
import trace 
import sys
from PIL import ImageTk, Image
try:
	from REF import ref
except:
	from .REF import ref
	

class torconfigwindow:
	
	def __init__(self , win, isopenflag):
		self.win = win;
		self.isopenflag = isopenflag;
		
		if __name__ == "__main__":
			self.filereletivelocation = "../../";
		else:
			self.filereletivelocation = "../";
		
		#Window Config
		self.win.title("Tor Configuration");
		win.resizable(width=False, height=False);
		self.frame = tk.Frame(master=win , width=850 , height=500);
		self.frame.pack();
		
		#Bridge Checkbutton
		self.usebridgecheck = ttk.Checkbutton(master=self.frame , text="Use Bridge");
		self.usebridgecheck.state(['!selected' , '!alternate']);
		self.usebridgecheck.place(x = 10 , y = 10);
		
		#Get Tor Port
		filehandle = open(self.filereletivelocation+"Tor Config/Tor Port" , "r");
		self.torportvalue = filehandle.read();
		filehandle.close();
		
		#Tor Port Spinbox
		self.torportvaluestr = tk.StringVar(win);
		self.torportvaluestr.set(self.torportvalue);
		self.torportspin = tk.Spinbox(master=self.frame , from_=1000 , to=65535 , width=12 , textvariable=self.torportvaluestr);
		self.torportspin.place(x=180 , y= 10);
		self.torportspinlabel = tk.Label(master=self.frame ,text="Tor Port:");
		self.torportspinlabel.place(x=120 , y=10);
		
		#Exit Node Bridge Drop Menu
		filehandle = open(self.filereletivelocation+"Tor Config/Country list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		
		self.countrylist = filecontainer.split("\n");
		del self.countrylist[len(self.countrylist)-1];
		self.countrydropmenu = ttk.Combobox(master=self.frame ,values=self.countrylist ,width=42 ,font=('Courier', 12));
		self.countrydropmenu.set(self.countrylist[0]);
		self.countrydropmenu.place(x=396 , y = 10);
		self.win.option_add('*TCombobox*Listbox.font', ('Courier', 12));
		
		self.exitnodelabel = tk.Label(master=self.frame ,text="Exit Node:");
		self.exitnodelabel.place(x=320 , y=10);
		#Bridge Label Frame
		self.bridgelabelframe = tk.LabelFrame(master = self.frame, width = 400, text="Bridge List" , padx=5 , pady=5);
		self.bridgelabelframe.place(x = 10 , y = 45);
		self.bridgeframe = tk.Frame(master = self.bridgelabelframe, width = 390, height=370, padx=0 , pady=0);
		self.bridgeframe.pack();
		
		#Bridge List Box
		self.bridgelistbox = tk.Listbox(master = self.bridgeframe , selectmode=tk.SINGLE , width = 48 , height = 20);
		filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filelines = filecontainer.split("\n");
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.bridgelistbox.insert(i+1 , tmp[0]);
		self.bridgelistbox.place(x=0 , y=0);
		
		#Obfs4 Label Frame
		self.obfs4labelframe = tk.LabelFrame(master = self.frame, width = 400, text="Obfs4 List" , padx=5 , pady=5);
		self.obfs4labelframe.place(x = 430 , y = 45);
		self.obfs4frame = tk.Frame(master = self.obfs4labelframe, width = 390, height=370, padx=0 , pady=0);
		self.obfs4frame.pack();
		
		#Bridge List Box
		self.obfs4listbox = tk.Listbox(master = self.obfs4frame , selectmode=tk.SINGLE , width = 48 , height = 20);
		filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filelines = filecontainer.split("\n");
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.obfs4listbox.insert(i+1 , tmp[1]);
		self.obfs4listbox.place(x=0 , y=0);
		
		#Set Bridge Button
		self.setbutton = tk.Button(master= self.frame , text="Set" , padx=10 , pady = 10 , width=10, command=self.setcommand);
		self.setbutton.place(x=10 , y=450);
		
		#Cancel Button
		self.cancelbutton = tk.Button(master= self.frame, text="cancel" , padx=10 , pady = 10 , width=10, command=self.on_closing);
		self.cancelbutton.place(x=150 , y=450);
		
		#Window Close Button Config
		win.protocol("WM_DELETE_WINDOW", self.on_closing);
	
	#Window Closing Event
	def on_closing(self):
		self.isopenflag.set(False);
		self.win.destroy();
	
	#Set Command (remake Tor Bridge Config)
	def setcommand(self):
		selectedbridge = self.bridgelistbox.curselection();
		selectedobfs4 = self.obfs4listbox.curselection();
		exitnodecountrystr = self.countrydropmenu.get();
		torport = self.torportspin.get();
		
		if ("selected" in self.usebridgecheck.state()) and not(selectedbridge) and not(selectedobfs4):
			tkMessageBox.showerror("Error", "Select a Bridge or Obsf4!\nIf lists are empty, Add one!" , master=self.frame)
			return;
			
		filecontainer = "UseBridges " + str(int("selected" in self.usebridgecheck.state())) +"\n";
		
		if selectedbridge and ("selected" in self.usebridgecheck.state()):
			filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "r");
			filecontainertmp = filehandle.read();
			filehandle.close();
			filelines = filecontainertmp.split("\n");
			filecontainer += "Bridge " + filelines[selectedbridge[0]] + "\n";
			
		if selectedobfs4 and ("selected" in self.usebridgecheck.state()):
			filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "r");
			filecontainertmp = filehandle.read();
			filehandle.close();
			filelines = filecontainertmp.split("\n");
			filecontainer += "ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy\nBridge " + filelines[selectedobfs4[0]] + "\n";
		
		if "GLOBAL" not in exitnodecountrystr:
			filecontainertmp = exitnodecountrystr.split(" ");
			filecontainer += "ExitNodes " + filecontainertmp[len(filecontainertmp)-1] + "\n";
		
		filecontainer += "SocksListenAddress 127.0.0.1:"+torport+"\nSocksPort "+torport+"\n";
		filehandle = open(self.filereletivelocation+"Tor Config/Bridge" , "w");
		filehandle.write(filecontainer);
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Tor Config/Tor Port" , "w");
		filehandle.write(torport);
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Privoxy Config/Privoxy Port" , "r");
		privoxyport = filehandle.read().rstrip();
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Privoxy Config/PrivoxyConfig" , "w");
		filecontainer = "forward-socks5 / 127.0.0.1:"+torport+" .\nlisten-address  127.0.0.1:"+privoxyport+" .\n";
		filehandle.write(filecontainer);
		filehandle.close();
		self.isopenflag.set(False);
		self.win.destroy();
		
if __name__ == "__main__":
	window = tk.Tk();
	isopenflag = ref(True);
	GUI = torconfigwindow(window , isopenflag);
	window.mainloop();
