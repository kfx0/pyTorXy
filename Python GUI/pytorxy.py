import time
import os
import subprocess
import signal
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

from classes.REF import ref
from classes.NewThreading import thread_with_trace
from classes.AddBridgeWindow import addbridgewindow
from classes.TorConfigWindow import torconfigwindow
from classes.PrivoxyConfigWindow import privoxyconfigwindow

class mainwindow:
	
	def __init__(self , win):
		self.win = win;
		self.addbridgeopenflag = ref(False);
		self.torconfigopenflag = ref(False);
		self.privoxyconfigopenflag = ref(False);
		
		#Window Config
		self.win.title("Tor Proxy");
		win.resizable(width=False, height=False);
		self.frame = tk.Frame(master = win , width = 850 , height = 110);
		self.frame.pack();
		
		#Create Menu bar
		self.menubar = tk.Menu(self.win);
		self.toolbar = tk.Frame(self.win, bd=1, relief=tk.RAISED);
		self.toolbar.pack(side=tk.TOP, fill=tk.X);
		self.win.config(menu=self.menubar)
		
		#Create File Menu
		self.fileMenu = tk.Menu(self.win, tearoff=0);
		self.menubar.add_cascade(label="File", menu=self.fileMenu);
		
		#Create Tor Confige Menu
		self.torconfigMenu = tk.Menu(self.win, tearoff=0);
		self.menubar.add_cascade(label="Tor Menu", menu=self.torconfigMenu);
		
		#Create Privoxy Confige Menu
		self.privoxyconfigMenu = tk.Menu(self.win, tearoff=0);
		self.menubar.add_cascade(label="Privoxy Menu", menu=self.privoxyconfigMenu);
		
		#Create Help Menu
		self.helpMenu = tk.Menu(self.win, tearoff=0);
		self.menubar.add_cascade(label="Help", menu=self.helpMenu);
		
		#Add (Exit) to File Menu
		self.fileMenu.add_command(label="Exit", command=self.on_closing);
		
		#Add (Add Bridge) to Tor Config Menu
		self.torconfigMenu.add_command(label="Add/Remove Bridge", command=self.TorAddBridge);
		
		#Add (Tor Configuration) to Tor Config Menu
		self.torconfigMenu.add_command(label="Tor Configuration", command=self.TorConfig);
		
		#Add (Privoxy Configuration) to Privoxy Config Menu
		self.privoxyconfigMenu.add_command(label="Privoxy Configuration", command=self.PrivoxyConfig);
		
		#Add (About) and (Help) to Help Menu
		self.helpMenu.add_command(label="About", 
								  command=lambda: tkMessageBox.showinfo("About", 
								  "pyToxy\nBy kfx0 (github)\nVersion: 1.0.0",
								  master=self.win)
								 );
		self.helpMenu.add_command(label="Help", 
								  command=lambda: tkMessageBox.showinfo("Help" ,
								  "SOCKS5\nhost:127.0.0.1\nport: read from tor config\n\nHTTP/HTTPS\nhost:127.0.0.1\nport: read from privoxy config",
								  master=self.win)
								 );
		
		#Create Tor Start Button
		self.startbuttontext = tk.StringVar();
		self.startbuttontext.set("Start Tor");
		
		#Create Privoxy Start Button
		self.startprivoxytext = tk.StringVar();
		self.startprivoxytext.set("Start Privoxy");
		
		#Add Tor Logo
		img = ImageTk.PhotoImage(Image.open("logo_tor.png").resize((50, 50), Image.ANTIALIAS));
		self.logo = tk.Label(self.frame , image = img, borderwidth=0);
		self.logo.image = img;
		self.logo.place(x = 0 , y = 5);
		
		#Add Privoxy Logo
		img1 = ImageTk.PhotoImage(Image.open("logo_privoxy.png").resize((50, 50), Image.ANTIALIAS));
		self.logo1 = tk.Label(self.frame , image = img1, borderwidth=0);
		self.logo1.image = img1;
		self.logo1.place(x = 800 , y = 5);
		
		#Tor and Privoxy State Flag (on / off flag)
		self.ssflag = 0;
		self.spflag = 0;
		
		#Tor Button Event and Position Setting
		self.ss_button = tk.Button(self.frame, textvariable=self.startbuttontext, command=self.ss, height = 2 , width = 43)
		self.ss_button.place(x = 52 , y = 5);
		
		#Privoxy Button Event and Postion Setting
		self.sp_button = tk.Button(self.frame, textvariable=self.startprivoxytext, command=self.sp, height = 2 , width = 43)
		self.sp_button.place(x = 426 , y = 5);
		
		#Feedback Text Creation for Tor Condition
		self.cm = tk.StringVar();
		self.cm.set("Tor Proxy is ready...");
		self.label = tk.Label(self.frame , textvariable=self.cm , wraplength = 750 , justify = tk.LEFT);
		self.label.place(x = 0 , y = 60);
		
		#Terminal Clear 
		os.system("clear");
		
		#Kill Tor if its running
		stdout , stderr = subprocess.Popen('pidof tor |wc -w' , shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setsid).communicate();
		if (int(stdout) == 1):
			stdout1 , stderr1 = subprocess.Popen('pidof tor' , shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setsid).communicate();
			os.kill(int(stdout1), signal.SIGTERM)
			
		#Application Close Button Config
		win.protocol("WM_DELETE_WINDOW", self.on_closing)
	
	
	#Tor Start and Stop Button with Terminal Feedback
	def ss(self):
		if self.ssflag == 0:
			self.startbuttontext.set("Stop Tor");
			#Tor Thread flag control
			self.stflag = 0;
			self.process = subprocess.Popen("tor --defaults-torrc torrc -f \"../Tor Config/Bridge\"", shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setsid);
			self.t1 = thread_with_trace(target=self.TorThread);
			self.t1.start();
			self.ssflag = 1;
		else:
			self.startbuttontext.set("Start Tor");
			os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
			self.stflag = 1;
			self.t1.kill();
			self.t1.join();
			self.ssflag = 0;
			self.cm.set("Process Stopped!");
			self.win.update();
	
	#Privoxy Start and Stop Button 
	def sp(self):
		if self.spflag == 0:
			self.startprivoxytext.set("Stop Privoxy");
			self.processprivoxy = subprocess.Popen("privoxy --no-daemon \"../Privoxy Config/PrivoxyConfig\"", shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=os.setsid);
			self.spflag = 1;
		else:
			self.startprivoxytext.set("Start Privoxy");
			os.killpg(os.getpgid(self.processprivoxy.pid), signal.SIGTERM)
			self.spflag = 0;
			self.win.update();
	
	#Tor Thread 
	def TorThread(self):
		lineIT = iter(self.process.stdout.readline , b'');
		line = "";
		while self.stflag == 0 and next(lineIT) is not None:
			try:
				line = next(lineIT);
			except:
				self.win.update();
				break;
			self.cm.set(line);
			self.win.update();
	
	#Define on closing event callback
	def on_closing(self):
		try:
			os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
			os.killpg(os.getpgid(self.processprivoxy.pid), signal.SIGTERM)
			self.t1.kill();
			self.t1.join();
			os.system("clear");
		except: 
			os.system("clear");
		try:
			self.TorAddBridgewin.destroy();
		except:
			os.system("clear");
		try:
			self.TorConfigwin.destroy();
		except:
			os.system("clear");
		try:
			self.PrivoxyConfigwin.destroy();
		except:
			os.system("clear");	
		self.win.destroy()
	
	#Define Tor Add Bridge Window
	def TorAddBridge(self):
		if not(self.addbridgeopenflag.get()):
			self.addbridgeopenflag.set(True);
			self.TorAddBridgewin = tk.Tk();
			self.TorAddBridgeGUI = addbridgewindow(self.TorAddBridgewin , self.addbridgeopenflag);
			self.TorAddBridgewin.mainloop();
		else:
			self.TorAddBridgewin.lift();
			self.TorAddBridgewin.after(1, lambda: self.TorAddBridgewin.focus_force())
		
	#Define Tor Configuration Window	
	def TorConfig(self):
		if not(self.torconfigopenflag.get()):
			self.torconfigopenflag.set(True);
			self.TorConfigwin = tk.Tk();
			self.TorConfigGUI = torconfigwindow(self.TorConfigwin , self.torconfigopenflag);
			self.TorConfigwin.mainloop();
		else:
			self.TorConfigwin.lift();
			self.TorConfigwin.after(1, lambda: self.TorConfigwin.focus_force())
	
	#Define Pirvoxy Configuration window
	def PrivoxyConfig(self):
		if not(self.privoxyconfigopenflag.get()):
			self.privoxyconfigopenflag.set(True);
			self.PrivoxyConfigwin = tk.Tk();
			self.PrivoxyConfigGUI = privoxyconfigwindow(self.PrivoxyConfigwin , self.privoxyconfigopenflag);
			self.PrivoxyConfigwin.mainloop();
		else:
			self.PrivoxyConfigwin.lift();
			self.PrivoxyConfigwin.after(1, lambda: self.PrivoxyConfigwin.focus_force())

#Run Application
if __name__ == "__main__":
	os.system("clear");
	window = tk.Tk();
	window.tk.call('wm', 'iconphoto', window._w, ImageTk.PhotoImage(file='logo.png'))
	GUI = mainwindow(window);
	window.mainloop();
