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
import threading
try:
	from REF import ref
except:
	from .REF import ref

class addbridgewindow:
	
	def __init__(self , win, isopenflag):
		self.win = win;
		self.isopenflag = isopenflag;
		
		if __name__ == "__main__":
			self.filereletivelocation = "../../";
		else:
			self.filereletivelocation = "../";
			
		#Window Config
		self.win.title("Add/Remove Bridge");
		win.resizable(width=False, height=False);
		self.frame = tk.Frame(master = win , width = 850 , height = 610);
		self.frame.pack();
		
		########################## Add Bridge and Obfs4 Frame #######################################
		self.addbridgeobfs4frame = tk.LabelFrame(master = self.frame , width = 830, text="Add Bridge and Obfs4" , padx=5 , pady = 5);
		self.addbridgeobfs4frame.place(x = 8 , y = 10);
		
		#Bridge and Obfs4 Notebook
		self.addbridgeobfs4tabbox = ttk.Notebook(master = self.addbridgeobfs4frame , width=820 , height=90);
		
		#Make Tab Bridge and Obfs4
		self.addbridgetab = ttk.Frame(self.addbridgeobfs4tabbox);
		self.addobfs4tab = ttk.Frame(self.addbridgeobfs4tabbox);
		
		#Add Bridge and Obfs4 Tabs to Add Bridge Tab box
		self.addbridgeobfs4tabbox.add(self.addbridgetab , text="Bridge");
		self.addbridgeobfs4tabbox.add(self.addobfs4tab , text="Obfs4");
		
		######## Make Tab Bridge ###########
		##Add text box
		self.addbridgetextbox = tk.Text(master = self.addbridgetab , width=100 , height=2);
		self.addbridgetextbox.place(x=5 , y=5);
		
		##Add Submit Button
		self.addbridgebutton = tk.Button(master = self.addbridgetab , text="Add Bridge" , command=self.addbridgecommand);
		self.addbridgebutton.place(x=5 , y = 50);
		####################################
		
		########## Make Tab Obfs4 ##########
		##Add text box
		self.addobfs4textbox = tk.Text(master = self.addobfs4tab , width=100 , height=2);
		self.addobfs4textbox.place(x=5 , y=5);
		
		##Add Submit Button
		self.addobfs4button = tk.Button(master = self.addobfs4tab , text="Add Obfs4" , command=self.addobfs4command);
		self.addobfs4button.place(x=5 , y = 50);
		####################################
		
		#Packing Tab Box
		self.addbridgeobfs4tabbox.pack(fill = tk.X , side = tk.TOP);
		
		########################## Remove Bridge and Obfs4 Frame #######################################
		self.removebridgeobfs4labelframe = tk.LabelFrame(master=self.frame , width = 830, text="Remove Bridge and Obfs4" , padx=5 , pady=5);
		self.removebridgeobfs4labelframe.place(x = 8 , y = 165);
		self.removebridgeobfs4frame = tk.Frame(master=self.removebridgeobfs4labelframe, width=820 , height=400 , padx=0 , pady=0);
		self.removebridgeobfs4frame.pack();
		
		#Bridge Label Frame
		self.removebridgelabelframe = tk.LabelFrame(master = self.removebridgeobfs4frame, width = 400, text="Bridge List" , padx=5 , pady=5);
		self.removebridgelabelframe.place(x = 0 , y = 0);
		self.removebridgeframe = tk.Frame(master = self.removebridgelabelframe, width = 390, height=370, padx=0 , pady=0);
		self.removebridgeframe.pack();
		
		#Bridge List Box
		self.bridgelistbox = tk.Listbox(master = self.removebridgeframe , selectmode=tk.SINGLE , width = 48 , height = 18);
		filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filelines = filecontainer.split("\n");
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.bridgelistbox.insert(i+1 , tmp[0]);
		self.bridgelistbox.place(x=0 , y=0);
		
		#Bridge Remove Buttom
		self.bridgeremovebotton = tk.Button(master = self.removebridgeframe, width = 45 ,text="Remove Bridge", command=self.removebridgecommand);
		self.bridgeremovebotton.place(x=0 , y=340);
		
		
		#Obfs4 Label Frame
		self.removeobfs4labelframe = tk.LabelFrame(master = self.removebridgeobfs4frame , width = 830, text="Obfs4 List" , padx=5 , pady = 5);
		self.removeobfs4labelframe.place(x = 415 , y = 0);
		self.removeobfs4frame = tk.Frame(master = self.removeobfs4labelframe, width = 390, height=370, padx=0 , pady=0);
		self.removeobfs4frame.pack();
		
		#Obfs4 List Box
		self.obfs4listbox = tk.Listbox(master = self.removeobfs4frame , selectmode=tk.SINGLE , width = 48 , height = 18);
		filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filelines = filecontainer.split("\n");
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.obfs4listbox.insert(i+1 , tmp[1]);
		self.obfs4listbox.place(x=0 , y=0);
		
		#Obfsd=4 Remove Buttom
		self.obfs4removebotton = tk.Button(master = self.removeobfs4frame, width = 45 ,text="Remove obfs4", command=self.removeobfs4command);
		self.obfs4removebotton.place(x=0 , y=340);
		
		#Window Close Button Config
		win.protocol("WM_DELETE_WINDOW", self.on_closing);
	
	#Window Closing Event
	def on_closing(self):
		self.isopenflag.set(False);
		self.win.destroy();	
		
	#Add Bridge Command
	def addbridgecommand(self):
		filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "a");
		bridge = self.addbridgetextbox.get("1.0" , "end");
		filehandle.write(bridge);
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filelines = filecontainer.split("\n");
		self.bridgelistbox.delete(0,self.bridgelistbox.size())
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.bridgelistbox.insert(i+1 , tmp[0]);
		self.addbridgetextbox.delete('1.0', "end");
		
	#Add Obfs4 Command
	def addobfs4command(self):
		filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "a");
		obfs4 = self.addobfs4textbox.get("1.0" , "end");
		filehandle.write(obfs4);
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filelines = filecontainer.split("\n");
		self.obfs4listbox.delete(0,self.obfs4listbox.size())
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.obfs4listbox.insert(i+1 , tmp[1]);
		self.addobfs4textbox.delete('1.0', "end");
	
	#Remove Bridge Command	
	def removebridgecommand(self):
		filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Tor Config/Bridges list" , "w");
		filelines = filecontainer.split("\n");
		x = self.bridgelistbox.curselection();
		x = x[0];
		del filelines[x];
		self.bridgelistbox.delete(0,self.bridgelistbox.size())
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.bridgelistbox.insert(i+1 , tmp[0]);
			filehandle.write(filelines[i]);
			if not(i == len(filelines)-1):
				filehandle.write("\n");
		filehandle.close();
		
	#Remove Obfs4 Command
	def removeobfs4command(self):
		filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "r");
		filecontainer = filehandle.read();
		filehandle.close();
		filehandle = open(self.filereletivelocation+"Tor Config/obfs4 list" , "w");
		filelines = filecontainer.split("\n");
		x = self.obfs4listbox.curselection();
		x = x[0];
		del filelines[x];
		self.obfs4listbox.delete(0,self.obfs4listbox.size())
		for i in range(len(filelines)-1):
			tmp = filelines[i].split(" ");
			self.obfs4listbox.insert(i+1 , tmp[1]);
			filehandle.write(filelines[i]);
			if not(i == len(filelines)-1):
				filehandle.write("\n");
		filehandle.close();

if __name__ == "__main__":
	window = tk.Tk();
	isopenflag = ref(True);
	GUI = addbridgewindow(window , isopenflag);
	window.mainloop();
