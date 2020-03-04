import time
import os
import subprocess
import signal
try:
	import Tkinter as tk
	import ttk
except:
	import tkinter as tk
	from tkinter import ttk
import trace 
import sys
from PIL import ImageTk, Image
try:
	from REF import ref
except:
	from .REF import ref

class privoxyconfigwindow:
	
	def __init__(self , win, isopenflag):
		self.win = win;
		self.isopenflag = isopenflag;
		
		if __name__ == "__main__":
			self.filereletivelocation = "../../";
		else:
			self.filereletivelocation = "../";
		
		
		#Window Config
		self.win.title("Privoxy Configuration");
		win.resizable(width=False, height=False);
		self.frame = tk.Frame(master = win , width = 220 , height = 100);
		self.frame.pack();
		
		#Get Tor Port
		filehandle = open(self.filereletivelocation+"Privoxy Config/Privoxy Port" , "r");
		self.privoxyportvalue = filehandle.read();
		filehandle.close();
		
		#Privoxy Port Spinbox
		self.privoxyportvaluestr = tk.StringVar(win);
		self.privoxyportvaluestr.set(self.privoxyportvalue);
		self.privoxyportspin = tk.Spinbox(master=self.frame , from_=1000 , to=65535 , width=12 , textvariable=self.privoxyportvaluestr);
		self.privoxyportspin.place(x=100 , y= 10);
		self.privoxyportspinlabel = tk.Label(master=self.frame ,text="Privoxy Port:");
		self.privoxyportspinlabel.place(x=10 , y=10);
		
		#Set Bridge Button
		self.setbutton = tk.Button(master= self.frame , text="Set" , padx=10 , pady = 10 , width=9, command=self.setcommand);
		self.setbutton.place(x=10 , y=50);
		
		#Cancel Button
		self.cancelbutton = tk.Button(master= self.frame, text="cancel" , padx=10 , pady = 10 , width=9, command=self.on_closing);
		self.cancelbutton.place(x=115 , y=50);
		
		#Window Close Button Config
		win.protocol("WM_DELETE_WINDOW", self.on_closing)
	
	#Window Closing Event
	def on_closing(self):
		self.isopenflag.set(False);
		self.win.destroy();
	
	#Set Command (remake Tor Bridge Config)
	def setcommand(self):
		privoxyport = self.privoxyportspin.get();
		filehandle = open(self.filereletivelocation+"Tor Config/Tor Port" , "r");
		torport = filehandle.read().rstrip();
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Privoxy Config/PrivoxyConfig" , "w");
		filecontainer = "forward-socks5 / 127.0.0.1:"+torport+" .\nlisten-address  127.0.0.1:"+privoxyport+" .\n";
		filehandle.write(filecontainer);
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Privoxy Config/Privoxy Port" , "w");
		filehandle.write(privoxyport);
		filehandle.close();
		self.isopenflag.set(False);
		self.win.destroy();
if __name__ == "__main__":
	window = tk.Tk();
	isopenflag = ref(True);
	GUI = privoxyconfigwindow(window , isopenflag);
	window.mainloop();
