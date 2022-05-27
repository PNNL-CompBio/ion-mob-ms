#!/usr/bin/env python3.9

from time import sleep
import tkinter as tk
import tkinter.filedialog
from tkinter.ttk import *
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfile
import tkinter.scrolledtext as scrolledtext
from tkinter import messagebox as msg
from tkinter import font
import os
from turtle import bgcolor, st
import threading
import sv_ttk
from ttkthemes import ThemedTk
import json
import pmw
from utils_mac import *
import sys

"""
Front End for ION Mobility Desktop Application


Users can:

Select their experiment type
Build a Pipeline
Fill in required experimental parameters
Upload required files
Run Experiment

"""

#To do: Create Slide Deck

#Nextflow Note This will not work if main.nf is not in current directory. 
#  When this is executable app, add string substitution to find current directory and/or main.nf

#Notes
#SV Black = #1c1c1c
#Standard Background = #E5E4E2


#Set working directory
cur_dir = os.path.dirname(__file__)
os.chdir(cur_dir)

                      
#Layout

# Initialize application
window = ThemedTk(theme="none")
window.title("PNNL Ion Mobility Application",)
window.config(bg='#0C74BA')
#window.geometry("1500x900")
window.columnconfigure(1)
window.columnconfigure(8)

tabControl = ttk.Notebook(window)
tabControl.grid(row=2, rowspan=10,column=7)

pmw.initialise(window)
window.columnconfigure(0,weight=1)
window.columnconfigure(10,weight=1)
sv_ttk.set_theme("dark")

screen_width = window.winfo_screenwidth()
screen_height = (window.winfo_screenheight()-50)
window_height = 900
window_width = 1500

wf = 1
hf = 1
small_screen = False
if screen_height < window_height or screen_width < window_width:
    wf = window_width/screen_width
    hf = window_height/screen_height
    small_screen = True


#Global Labels
l1=Label(window,text="  PNNL Ion Mobility Application  ", font=("default", int(30//wf)),borderwidth=1, relief="solid", width = int(45//wf)).grid(row=0, column = 7, ipady=(10), sticky="EW")
l2=Label(window,text="Experiment", font=("default", int(20//wf), "bold"),borderwidth=0, relief="solid", height=2).grid(row=1,column=7, ipadx=(0), pady=(5,0), sticky="EW")
sep = tk.Frame(window, bg="black", height=2, bd=0).grid(row=1, column=7, sticky="EWS", ipadx=(0), padx=(8,8))

#tabs
tab1 = ttk.Frame(tabControl)


tabControl.add(tab1, text = "Single Field")
tab1.columnconfigure((1,2,3,4,5,6,7,8,9), minsize=int(140//wf))
tab1.columnconfigure((0), minsize=int(20//wf))
tab1.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=int(25//hf))
tab1.rowconfigure((4), minsize=int(90//hf))

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text = "SLIM")
tab2.columnconfigure((0,1,2,3,4,5,6,7,8,9), minsize=int(140//wf))
tab2.columnconfigure((0), minsize=int(20//wf))
tab2.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=int(25//wf))
tab2.rowconfigure((4), minsize=int(90//wf))

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text = "Stepped Field")
tab3.columnconfigure((0,1,2,3,4,5,6,7,8,9), minsize=int(140//wf))
tab3.columnconfigure((0), minsize=int(20//wf))
tab3.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=int(25//wf))
tab3.rowconfigure((4), minsize=int(90//wf))


##################################################################
                ##### Single Field Tab #####
##################################################################

t1_l3=Label(tab1,text="     Build Your Pipeline   ", font=("Helvetica Neue", int(18//wf), "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "nw", justify = "left").grid(row=1, rowspan=4, column=0, columnspan=10, pady=(5,0), sticky="NEWS")
t1_l11=Label(tab1,text="     Hover over the tools or click \"Show Documentation\" for a description of usage.  ", font=("Helvetica Neue", int(14//wf), "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "center", justify = "left").grid(row=1, rowspan=1, column=3, columnspan=8, pady=(5,0), sticky="NEWS")

#initialize tool design frames
t1_tool_1 = tk.Frame(tab1)
t1_tool_2 = tk.Frame(tab1)
t1_tool_3 = tk.Frame(tab1)
t1_tool_4 = tk.Frame(tab1)
t1_generate_pipeline = tk.Frame(tab1)

t1_canvas1 = tk.Canvas(t1_tool_1 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t1_canvas2 = tk.Canvas(t1_tool_2 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t1_canvas3 = tk.Canvas(t1_tool_3 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t1_canvas4 = tk.Canvas(t1_tool_4 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t1_canvas5 = tk.Canvas(t1_generate_pipeline, height=int(101//hf), width=int(116//wf), bg ="grey", highlightthickness=0)

t1_canvas1.pack()
t1_canvas2.pack()
t1_canvas3.pack()
t1_canvas4.pack()
t1_canvas5.pack()

t1_tool_1.grid(row=2,column=1, columnspan=3,sticky = "W")
t1_tool_2.grid(row=2,column=3, columnspan=3,sticky = "W")
t1_tool_3.grid(row=2,column=5, columnspan=3,sticky = "W")
t1_tool_4.grid(row=2,column=7, columnspan=3,sticky = "W")
t1_generate_pipeline.grid(row=2,column=9, columnspan=2,sticky = "W")


#PNNL PreProcessor - labels, buttons, design
round_rectangle(t1_canvas1, 0, 0, int(200//wf), int(100//hf), 25, fill="#FE994A")
round_rectangle(t1_canvas1, 5, 5, int(195//wf), int(95//hf), 25, fill="#FEA95E")
round_rectangle(t1_canvas1, 20, 20, int(180//wf), int(80//hf), 25, fill="#FFCD91")
t1_canvas1.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(12//wf), "bold"), text="PNNL PreProcessor")

t1_canvas1_help = pmw.Balloon(window)
t1_canvas1_help.bind(t1_canvas1, "PNNL PreProcessor\nProcess raw data to reduce noise and highlight features.\n\nInput: Raw Data\nOutput: Processed data & metadata\nFilter out low count signals with \"minIntensity\".\nPerform smoothing to improve signal of low intensity peaks with \"driftkernel\".\nSum all frames into one by setting \"lcKernel\" to 0.")
t1_canvas1_lbl = t1_canvas1_help.component("label")
t1_canvas1_lbl.config(background="black", foreground="white")

t1_l3=Label(tab1,text="Filter data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=1, columnspan=2,sticky="w")
t1_l4=Label(tab1,text="Smooth data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=1, columnspan=2,sticky="w")

PP_check_1_single = BooleanVar(False)
PP_button_1_single = Checkbutton(tab1, variable=PP_check_1_single, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PP_button_1_single.grid(row=3, column=2, sticky = "W")

PP_check_2_single = BooleanVar(False)
PP_button_2_single = Checkbutton(tab1, variable=PP_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PP_button_2_single.grid(row=4, column=2, sticky = "W")


#ProteoWizard -  labels, buttons, design
round_rectangle(t1_canvas2, 0, 0, int(200//wf), int(100//hf), 25, fill="#bd1c1f")
round_rectangle(t1_canvas2, 5, 5, int(195//wf), int(95//hf), 25, fill="#f11b23")
round_rectangle(t1_canvas2, 20, 20, int(180//wf), int(80//hf), 25, fill="#fd6861")
t1_canvas2.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="ProteoWizard")

t1_canvas2_help = pmw.Balloon(window) 
t1_canvas2_help.bind(t1_canvas2, "ProteoWizard\nThis tool is capable of converting proprietary data (raw or preprocessed) into (gz compressed) mzML files.\nmzML format is universal file type that is required for many open source tools.\n\nInput: Raw or Preprocessed data\nOutput: mzML Files ")
t1_canvas2_lbl = t1_canvas2_help.component("label")
t1_canvas2_lbl.config(background="black", foreground="white")

t1_l5=Label(tab1,text= "  Convert to mzML", font=("default, 14"),borderwidth=0, relief="solid", height=2, bg="grey").grid(row=3, rowspan =1, column=3, columnspan=1, sticky = "w")

PW_check_1_single = BooleanVar(False)
PW_button_1_single = Checkbutton(tab1, variable=PW_check_1_single, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PW_button_1_single.grid(row=3, column=4, sticky = "W")


#DEIMoS -  labels, buttons, design
round_rectangle(t1_canvas3, 0, 0, int(200//wf), int(100//hf), 25, fill="#FFD300")
round_rectangle(t1_canvas3, 5, 5, int(195//wf), int(95//hf), 25, fill="#FFE54C")
round_rectangle(t1_canvas3, 20, 20, int(180//wf), int(80//hf), 25, fill="#FFFFBF")
t1_canvas3.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="DEIMoS")

t1_canvas3_help = pmw.Balloon(window)
t1_canvas3_help.bind(t1_canvas3, "DEIMoS\nThis tool has many capabilities including feature detection and CCS calculation.\n\nInput: mzML files, metadata, target list, calibrant data, configuration file (hidden) \nOutput: Feature files and/or CCS results")
t1_canvas3_lbl = t1_canvas3_help.component("label")
t1_canvas3_lbl.config(background="black", foreground="white")

t1_l6=Label(tab1,text="  Feature Detection", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=5, columnspan=1)
t1_l7=Label(tab1,text="Calculate CCS", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=5, columnspan=1)

DS_check_1_single = BooleanVar(False)
DS_button_1_single = Checkbutton(tab1, variable=DS_check_1_single, onvalue=True, offvalue=False, bg="grey", fg ="blue")
DS_button_1_single.grid(row=3, column=6, sticky = "W")

DS_check_2_single = BooleanVar(False)
DS_button_2_single = Checkbutton(tab1, variable=DS_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
DS_button_2_single.grid(row=4, column=6, sticky = "W")


#AutoCCS - labels, buttons, design
round_rectangle(t1_canvas4, 0, 0, int(200//wf), int(100//hf), 25, fill="#5CB6F2")
round_rectangle(t1_canvas4, 5, 5, int(195//wf), int(95//hf), 25, fill="#7EC4EF")
round_rectangle(t1_canvas4, 20, 20, int(180//wf), int(80//hf), 25, fill="#BEDFF1")
t1_canvas4.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="AutoCCS")

t1_canvas4_help = pmw.Balloon(window)
t1_canvas4_help.bind(t1_canvas4, "AutoCCS\nThis tool offers two methods of CCS calculations.\nThe \"standard\" method is comparable to DEIMoS.\nThe \"enhanced\" method takes into account the temperature and pressure of the instrument across runs.\n\nInput: Feature files, calibration data, target list, configuration file (hidden) \nOutput: CCS results\n")
t1_canvas4_lbl = t1_canvas4_help.component("label")
t1_canvas4_lbl.config(background="black", foreground="white")


t1_l8=Label(tab1,text="Calculate CCS (Standard)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=7, columnspan=1)
t1_l9=Label(tab1,text="Calculate CCS (Enhanced)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=7, columnspan=1)

AC_check_1_single = BooleanVar(False)
AC_button_1_single = Checkbutton(tab1, variable=AC_check_1_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
AC_button_1_single.grid(row=3, column=8, sticky = "W")

AC_check_2_single = BooleanVar(False)
AC_button_2_single = Checkbutton(tab1, variable=AC_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
AC_button_2_single.grid(row=4, column=8, sticky = "W")

#Generate Pipeline Button -  labels, buttons, design
t1_tag0 = round_rectangle(t1_canvas5, 0, 0, int(115//wf), int(100//hf), 25, fill="black")
t1_tag1 = round_rectangle(t1_canvas5, 5, 5, int(110//wf), int(95//hf), 25, fill="#72cc50")
t1_tag2 = t1_canvas5.create_text(int(57//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="Generate\nNew\nPipeline", justify="center")
t1_tag3 = t1_canvas5.create_rectangle(0, 0, 0, 0, fill="grey", width=0)

t1_canvas5.tag_bind(t1_tag0, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab1, window, hf, wf,small_screen, PP_check_1_single.get(),PP_check_2_single.get(),PW_check_1_single.get(),DS_check_1_single.get(),DS_check_2_single.get(),AC_check_1_single.get(),AC_check_2_single.get()))
t1_canvas5.tag_bind(t1_tag1, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab1, window, hf, wf,small_screen, PP_check_1_single.get(),PP_check_2_single.get(),PW_check_1_single.get(),DS_check_1_single.get(),DS_check_2_single.get(),AC_check_1_single.get(),AC_check_2_single.get()))
t1_canvas5.tag_bind(t1_tag2, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab1, window, hf, wf,small_screen, PP_check_1_single.get(),PP_check_2_single.get(),PW_check_1_single.get(),DS_check_1_single.get(),DS_check_2_single.get(),AC_check_1_single.get(),AC_check_2_single.get()))

t1_canvas5.tag_bind(t1_tag0, "<Enter>", lambda event: t1_canvas5.config(bg="yellow"))
t1_canvas5.tag_bind(t1_tag1, "<Enter>", lambda event: t1_canvas5.config(bg="yellow"))
t1_canvas5.tag_bind(t1_tag2, "<Enter>", lambda event: t1_canvas5.config(bg="yellow"))
t1_canvas5.tag_bind(t1_tag0, "<Leave>", lambda event: t1_canvas5.config(bg="grey"))
t1_canvas5.tag_bind(t1_tag1, "<Leave>", lambda event: t1_canvas5.config(bg="grey"))
t1_canvas5.tag_bind(t1_tag2, "<Leave>", lambda event: t1_canvas5.config(bg="grey"))

t1_canvas5_help = pmw.Balloon(window)
t1_canvas5_help.bind(t1_canvas5, "Note: Generating new pipeline will\nclear all existing pipelines and results.")
t1_canvas5_lbl = t1_canvas5_help.component("label")
t1_canvas5_lbl.config(background="black", foreground="white")

#Show Documentation Button
Help_button_slim = tk.Button(tab1,text="Show\nDocumentation", command=lambda:show_help_single(window), height=3, width=int(14//hf), bg = "silver", fg= "green")
Help_button_slim.grid(row=4, column=9, columnspan=2, sticky = "NWE")


##################################################################
                #### SLIM Tab ####
##################################################################

t2_l3=Label(tab2,text="     Build Your Pipeline", font=("Helvetica Neue", 18, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "nw", justify = "left").grid(row=1, rowspan=4, column=0, columnspan=10, pady=(5,0), sticky="NEWS")
t2_l11=Label(tab2,text="     Hover over the tools or click \"Show Documentation\" for a description of usage.  ", font=("Helvetica Neue", 14, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "center", justify = "left").grid(row=1, rowspan=1, column=3, columnspan=8
, pady=(5,0), sticky="NEWS")

#initialize tool design frames
t2_tool_1 = tk.Frame(tab2)
t2_tool_2 = tk.Frame(tab2)
t2_tool_3 = tk.Frame(tab2)
t2_tool_4 = tk.Frame(tab2)
t2_generate_pipeline = tk.Frame(tab2)

t2_canvas1 = tk.Canvas(t2_tool_1 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t2_canvas2 = tk.Canvas(t2_tool_2 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t2_canvas3 = tk.Canvas(t2_tool_3 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t2_canvas4 = tk.Canvas(t2_tool_4 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t2_canvas5 = tk.Canvas(t2_generate_pipeline, height=int(101//hf), width=int(116//wf), bg ="grey", highlightthickness=0)


t2_canvas1.pack()
t2_canvas2.pack()
t2_canvas3.pack()
t2_canvas4.pack()
t2_canvas5.pack()

t2_tool_1.grid(row=2,column=1, columnspan=2,sticky = "W")
t2_tool_2.grid(row=2,column=3, columnspan=2,sticky = "W")
t2_tool_3.grid(row=2,column=5, columnspan=2,sticky = "W")
t2_tool_4.grid(row=2,column=7, columnspan=2,sticky = "W")
t2_generate_pipeline.grid(row=2,column=9, columnspan=2,sticky = "W")


#PNNL PreProcessor -  labels, buttons, design
round_rectangle(t2_canvas1, 0, 0, int(200//wf), int(100//hf), 25, fill="#FE994A")
round_rectangle(t2_canvas1, 5, 5, int(195//wf), int(95//hf), 25, fill="#FEA95E")
round_rectangle(t2_canvas1, 20, 20, int(180//wf), int(80//hf), 25, fill="#FFCD91")
t2_canvas1.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(12//wf), "bold"), text="PNNL PreProcessor")


t2_canvas1_help = pmw.Balloon(window)
t2_canvas1_help.bind(t2_canvas1, "PNNL PreProcessor\nProcess raw data to reduce noise and highlight features.\n\nInput: Raw Data\nOutput: Processed data & metadata\nFilter out low count signals with \"minIntensity\".\nPerform smoothing to improve signal of low intensity peaks with \"driftkernel\".\nSum all frames into one by setting \"lcKernel\" to 0.")
t2_canvas1_lbl = t2_canvas1_help.component("label")
t2_canvas1_lbl.config(background="black", foreground="white")

t2_l3=Label(tab2,text="Filter data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=1, columnspan=1)
t2_l4=Label(tab2,text="Smooth data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=1, columnspan=1)

PP_check_1_slim = BooleanVar(False)
PP_button_1_slim = Checkbutton(tab2, variable=PP_check_1_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PP_button_1_slim.grid(row=3, column=2, sticky = "W")

PP_check_2_slim = BooleanVar(False)
PP_button_2_slim = Checkbutton(tab2, variable=PP_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PP_button_2_slim.grid(row=4, column=2, sticky = "W")


#ProteoWizard -  labels, buttons, design
round_rectangle(t2_canvas2, 0, 0, int(200//wf), int(100//hf), 25, fill="#bd1c1f")
round_rectangle(t2_canvas2, 5, 5, int(195//wf), int(95//hf), 25, fill="#f11b23")
round_rectangle(t2_canvas2, 20, 20, int(180//wf), int(80//hf), 25, fill="#fd6861")
t2_canvas2.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="ProteoWizard")

t2_canvas2_help = pmw.Balloon(window) 
t2_canvas2_help.bind(t2_canvas2, "ProteoWizard\nThis tool is capable of converting proprietary data (raw or preprocessed) into (gz compressed) mzML files.\nmzML format is universal file type that is required for many open source tools.\n\nInput: Raw or Preprocessed data\nOutput: mzML Files ")
t2_canvas2_lbl = t2_canvas2_help.component("label")
t2_canvas2_lbl.config(background="black", foreground="white")

t2_l5=Label(tab2,text= "  Convert to mzML", font=("default, 14"),borderwidth=0, relief="solid", height=2, bg="grey").grid(row=3, rowspan =1, column=3, columnspan=1, sticky = "w")

PW_check_1_slim = BooleanVar(False)
PW_button_1_slim = Checkbutton(tab2, variable=PW_check_1_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PW_button_1_slim.grid(row=3, column=4, sticky = "W")


#DEIMoS -  labels, buttons, design
round_rectangle(t2_canvas3, 0, 0, int(200//wf), int(100//hf), 25, fill="#FFD300")
round_rectangle(t2_canvas3, 5, 5, int(195//wf), int(95//hf), 25, fill="#FFE54C")
round_rectangle(t2_canvas3, 20, 20, int(180//wf), int(80//hf), 25, fill="#FFFFBF")
t2_canvas3.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="DEIMoS")

t2_canvas3_help = pmw.Balloon(window)
t2_canvas3_help.bind(t2_canvas3, "DEIMoS\nThis tool has many capabilities including feature detection and CCS calculation.\n\nInput: mzML files, metadata, target list, calibrant data, configuration file (hidden) \nOutput: Feature files and/or CCS results")
t2_canvas3_lbl = t2_canvas3_help.component("label")
t2_canvas3_lbl.config(background="black", foreground="white")

t2_l6=Label(tab2,text="  Feature Detection", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=5, columnspan=1)
t2_l7=Label(tab2,text="Calculate CCS", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=5, columnspan=1)

DS_check_1_slim = BooleanVar(False)
DS_button_1_slim = Checkbutton(tab2, variable=DS_check_1_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue")
DS_button_1_slim.grid(row=3, column=6, sticky = "W")

DS_check_2_slim = BooleanVar(False)
DS_button_2_slim = Checkbutton(tab2, variable=DS_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
DS_button_2_slim.grid(row=4, column=6, sticky = "W")


#AutoCCS -  labels, buttons, design
round_rectangle(t2_canvas4, 0, 0, int(200//wf), int(100//hf), 25, fill="#5CB6F2")
round_rectangle(t2_canvas4, 5, 5, int(195//wf), int(95//hf), 25, fill="#7EC4EF")
round_rectangle(t2_canvas4, 20, 20, int(180//wf), int(80//hf), 25, fill="#BEDFF1")
t2_canvas4.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="AutoCCS")

t2_canvas4_help = pmw.Balloon(window)
t2_canvas4_help.bind(t2_canvas4, "AutoCCS\nThis tool offers two methods of CCS calculations.\nThe \"standard\" method is comparable to DEIMoS.\nThe \"enhanced\" method takes into account the temperature and pressure of the instrument across runs.\n\nInput: Feature files, calibration data, target list, configuration file (hidden) \nOutput: CCS results\n")
t2_canvas4_lbl = t2_canvas4_help.component("label")
t2_canvas4_lbl.config(background="black", foreground="white")

t2_l8=Label(tab2,text="Calculate CCS (Standard)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=7, columnspan=1)
t2_l9=Label(tab2,text="Calculate CCS (Enhanced)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=7, columnspan=1)

AC_check_1_slim = BooleanVar(False)
AC_button_1_slim = Checkbutton(tab2, variable=AC_check_1_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
AC_button_1_slim.grid(row=3, column=8, sticky = "W")

AC_check_2_slim = BooleanVar(False)
AC_button_2_slim = Checkbutton(tab2, variable=AC_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
AC_button_2_slim.grid(row=4, column=8, sticky = "W")

#Generate Pipeline Button -  labels, buttons, design
t2_tag0 = round_rectangle(t2_canvas5, 0, 0, int(115//wf), int(100//hf), 25, fill="black")
t2_tag1 = round_rectangle(t2_canvas5, 5, 5, int(110//wf), int(95//hf), 25, fill="#72cc50")
t2_tag2 = t2_canvas5.create_text(int(57//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="Generate\nNew\nPipeline", justify="center")
t2_tag3 = t2_canvas5.create_rectangle(0, 0, 0, 0, fill="grey", width=0)

t2_canvas5.tag_bind(t2_tag0, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab2, window, hf, wf,small_screen, PP_check_1_slim.get(),PP_check_2_slim.get(),PW_check_1_slim.get(),DS_check_1_slim.get(),DS_check_2_slim.get(),AC_check_1_slim.get(),AC_check_2_slim.get()))
t2_canvas5.tag_bind(t2_tag1, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab2, window, hf, wf,small_screen, PP_check_1_slim.get(),PP_check_2_slim.get(),PW_check_1_slim.get(),DS_check_1_slim.get(),DS_check_2_slim.get(),AC_check_1_slim.get(),AC_check_2_slim.get()))
t2_canvas5.tag_bind(t2_tag2, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab2, window, hf, wf,small_screen, PP_check_1_slim.get(),PP_check_2_slim.get(),PW_check_1_slim.get(),DS_check_1_slim.get(),DS_check_2_slim.get(),AC_check_1_slim.get(),AC_check_2_slim.get()))

t2_canvas5.tag_bind(t2_tag0, "<Enter>", lambda event: t2_canvas5.config(bg="yellow"))
t2_canvas5.tag_bind(t2_tag1, "<Enter>", lambda event: t2_canvas5.config(bg="yellow"))
t2_canvas5.tag_bind(t2_tag2, "<Enter>", lambda event: t2_canvas5.config(bg="yellow"))
t2_canvas5.tag_bind(t2_tag0, "<Leave>", lambda event: t2_canvas5.config(bg="grey"))
t2_canvas5.tag_bind(t2_tag1, "<Leave>", lambda event: t2_canvas5.config(bg="grey"))
t2_canvas5.tag_bind(t2_tag2, "<Leave>", lambda event: t2_canvas5.config(bg="grey"))

t2_canvas5_help = pmw.Balloon(window)
t2_canvas5_help.bind(t2_canvas5, "Note: Generating new pipeline will\nclear all existing pipelines and results.")
t2_canvas5_lbl = t2_canvas5_help.component("label")
t2_canvas5_lbl.config(background="black", foreground="white")

#Show Documentation Button
Help_button_slim = tk.Button(tab2,text="Show\nDocumentation", command=lambda:show_help_single(window), height=3, width=14, bg="silver", fg= "green")
Help_button_slim.grid(row=4, column=9, columnspan=2, sticky ="NWE")


##################################################################
                #### Stepped Field Tab #### 
##################################################################

t3_l3=Label(tab3,text="     Build Your Pipeline", font=("Helvetica Neue", 18, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "nw", justify = "left").grid(row=1, rowspan=4, column=0, columnspan=10, pady=(5,0), sticky="NEWS")
t3_l11=Label(tab3,text="     Hover over the tools or click \"Show Documentation\" for a description of usage.  ", font=("Helvetica Neue", 14, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "center", justify = "left").grid(row=1, rowspan=1, column=3, columnspan=8, pady=(5,0), sticky="NEWS")

#initialize tool design frames
t3_tool_1 = tk.Frame(tab3)
t3_tool_2 = tk.Frame(tab3)
t3_tool_3 = tk.Frame(tab3)
t3_tool_4 = tk.Frame(tab3)
t3_generate_pipeline = tk.Frame(tab3)

t3_canvas1 = tk.Canvas(t3_tool_1 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t3_canvas2 = tk.Canvas(t3_tool_2 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t3_canvas3 = tk.Canvas(t3_tool_3 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t3_canvas4 = tk.Canvas(t3_tool_4 , height=int(100//hf), width=int(200//wf), bg ="grey", highlightthickness=0)
t3_canvas5 = tk.Canvas(t3_generate_pipeline, height=int(101//hf), width=int(116//wf), bg ="grey", highlightthickness=0)

t3_canvas1.pack()
t3_canvas2.pack()
t3_canvas3.pack()
t3_canvas4.pack()
t3_canvas5.pack()

t3_tool_1.grid(row=2,column=1, columnspan=2,sticky = "W")
t3_tool_2.grid(row=2,column=3, columnspan=2,sticky = "W")
t3_tool_3.grid(row=2,column=5, columnspan=2,sticky = "W")
t3_tool_4.grid(row=2,column=7, columnspan=2,sticky = "W")
t3_generate_pipeline.grid(row=2,column=9, columnspan=2,sticky = "W")


#PNNL PreProcessor -  labels, buttons, design
round_rectangle(t3_canvas1, 0, 0, int(200//wf), int(100//hf), 25, fill="#FE994A")
round_rectangle(t3_canvas1, 5, 5, int(195//wf), int(95//hf), 25, fill="#FEA95E")
round_rectangle(t3_canvas1, 20, 20, int(180//wf), int(80//hf), 25, fill="#FFCD91")
t3_canvas1.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(12//wf), "bold"), text="PNNL PreProcessor")

t3_canvas1_help = pmw.Balloon(window)
t3_canvas1_help.bind(t3_canvas1, "PNNL PreProcessor\nProcess raw data to reduce noise and highlight features.\n\nInput: Raw Data\nOutput: Processed data & metadata\nFilter out low count signals with \"minIntensity\".\nPerform smoothing to improve signal of low intensity peaks with \"driftkernel\".\nSum all frames into one by setting \"lcKernel\" to 0.")
t3_canvas1_lbl = t3_canvas1_help.component("label")
t3_canvas1_lbl.config(background="black", foreground="white")

t3_l3=Label(tab3,text="Filter data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=1, columnspan=1)
t3_l4=Label(tab3,text="Smooth data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=1, columnspan=1)

PP_check_1_step = BooleanVar(False)
PP_button_1_step = Checkbutton(tab3, variable=PP_check_1_step, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PP_button_1_step.grid(row=3, column=2, sticky = "W")

PP_check_2_step = BooleanVar(False)
PP_button_2_step = Checkbutton(tab3, variable=PP_check_2_step, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PP_button_2_step.grid(row=4, column=2, sticky = "W")


#ProteoWizard -  labels, buttons, design
round_rectangle(t3_canvas2, 0, 0, int(200//wf), int(100//hf), 25, fill="#bd1c1f")
round_rectangle(t3_canvas2, 5, 5, int(195//wf), int(95//hf), 25, fill="#f11b23")
round_rectangle(t3_canvas2, 20, 20, int(180//wf), int(80//hf), 25, fill="#fd6861")
t3_canvas2.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="ProteoWizard")

t3_canvas2_help = pmw.Balloon(window) 
t3_canvas2_help.bind(t3_canvas2, "ProteoWizard\nThis tool is capable of converting proprietary data (raw or preprocessed) into (gz compressed) mzML files.\nmzML format is universal file type that is required for many open source tools.\n\nInput: Raw or Preprocessed data\nOutput: mzML Files ")
t3_canvas2_lbl = t3_canvas2_help.component("label")
t3_canvas2_lbl.config(background="black", foreground="white")

t3_l5=Label(tab3,text= "  Convert to mzML", font=("default, 14"),borderwidth=0, relief="solid", height=2, bg="grey").grid(row=3, rowspan =1, column=3, columnspan=1, sticky = "w")

PW_check_1_step = BooleanVar(False)
PW_button_1_step = Checkbutton(tab3, variable=PW_check_1_step, onvalue=True, offvalue=False, bg="grey", fg ="blue")
PW_button_1_step.grid(row=3, column=4, sticky = "W")


#MZMine -  labels, buttons, design
round_rectangle(t3_canvas3, 0, 0, int(200//wf), int(100//hf), 25, fill="#8800C7")
round_rectangle(t3_canvas3, 5, 5, int(195//wf), int(95//hf), 25, fill="#A44CD3")
round_rectangle(t3_canvas3, 20, 20, int(180//wf), int(80//hf), 25, fill="#E090EF")
t3_canvas3.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="Mzmine")

t3_canvas3_help = pmw.Balloon(window)
t3_canvas3_help.bind(t3_canvas3, "MZmine\nThis open source tool has feature detection capabilities.\n\nInput: mzML files & metadata\nOutput: Feature files")
t3_canvas3_lbl = t3_canvas3_help.component("label")
t3_canvas3_lbl.config(background="black", foreground="white")

t3_l6=Label(tab3,text="  Feature Detection", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=5, columnspan=1)
MM_check_1_step = BooleanVar(False)
MM_button_1_step = Checkbutton(tab3, variable=MM_check_1_step, onvalue=True, offvalue=False, bg="grey", fg ="blue")
MM_button_1_step.grid(row=3, column=6, sticky = "W")


#AutoCCS -  labels, buttons, design
round_rectangle(t3_canvas4, 0, 0, int(200//wf), int(100//hf), 25, fill="#5CB6F2")
round_rectangle(t3_canvas4, 5, 5, int(195//wf), int(95//hf), 25, fill="#7EC4EF")
round_rectangle(t3_canvas4, 20, 20, int(180//wf), int(80//hf), 25, fill="#BEDFF1")
t3_canvas4.create_text(int(100//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="AutoCCS")

t3_canvas4_help = pmw.Balloon(window)
t3_canvas4_help.bind(t3_canvas4, "AutoCCS\nThis tool offers two methods of CCS calculations.\nThe \"standard\" method is comparable to DEIMoS.\nThe \"enhanced\" method takes into account the temperature and pressure of the instrument across runs.\n\nInput: Feature files, target list, configuration file (hidden) \nOutput: CCS results\n")
t3_canvas4_lbl = t3_canvas4_help.component("label")
t3_canvas4_lbl.config(background="black", foreground="white")


t3_l8=Label(tab3,text="Calculate CCS (Enhanced)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=7, columnspan=1)

AC_check_1_step = BooleanVar(False)
AC_button_1_step = Checkbutton(tab3, variable=AC_check_1_step, onvalue=True, offvalue=False, bg="grey", fg ="blue")
AC_button_1_step.grid(row=3, column=8, sticky = "W")


#Generate Pipeline Button -  labels, buttons, design
t3_tag0 = round_rectangle(t3_canvas5, 0, 0, int(115//wf), int(100//hf), 25, fill="black")
t3_tag1 = round_rectangle(t3_canvas5, 5, 5, int(110//wf), int(95//hf), 25, fill="#72cc50")
t3_tag2 = t3_canvas5.create_text(int(57//wf),int(50//hf),fill="black",font=("Helvetica Neue", int(15//wf), "bold"), text="Generate\nNew\nPipeline", justify="center")
t3_tag3 = t3_canvas5.create_rectangle(0, 0, 0, 0, fill="grey", width=0)

t3_canvas5.tag_bind(t3_tag0, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab3, window, hf, wf,small_screen, PP_check_1_step.get(),PP_check_2_step.get(),PW_check_1_step.get(),MM_check_1_step.get(),AC_check_1_step.get()))
t3_canvas5.tag_bind(t3_tag1, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab3, window, hf, wf,small_screen, PP_check_1_step.get(),PP_check_2_step.get(),PW_check_1_step.get(),MM_check_1_step.get(),AC_check_1_step.get()))
t3_canvas5.tag_bind(t3_tag2, "<ButtonPress-1>", lambda event: Generate_pipeline(tabControl.index(tabControl.select()),tab3, window, hf, wf,small_screen, PP_check_1_step.get(),PP_check_2_step.get(),PW_check_1_step.get(),MM_check_1_step.get(),AC_check_1_step.get()))

t3_canvas5.tag_bind(t3_tag0, "<Enter>", lambda event: t3_canvas5.config(bg="yellow"))
t3_canvas5.tag_bind(t3_tag1, "<Enter>", lambda event: t3_canvas5.config(bg="yellow"))
t3_canvas5.tag_bind(t3_tag2, "<Enter>", lambda event: t3_canvas5.config(bg="yellow"))
t3_canvas5.tag_bind(t3_tag0, "<Leave>", lambda event: t3_canvas5.config(bg="grey"))
t3_canvas5.tag_bind(t3_tag1, "<Leave>", lambda event: t3_canvas5.config(bg="grey"))
t3_canvas5.tag_bind(t3_tag2, "<Leave>", lambda event: t3_canvas5.config(bg="grey"))

t3_canvas5_help = pmw.Balloon(window)
t3_canvas5_help.bind(t3_canvas5, "Note: Generating new pipeline will\nclear all existing pipelines and results.")
t3_canvas5_lbl = t3_canvas5_help.component("label")
t3_canvas5_lbl.config(background="black", foreground="white")

#Show Documentation Button
Help_button_step = tk.Button(tab3,text="Show\nDocumentation", command=lambda:show_help_step(window), height=3, width=14, bg= "silver", fg= "green")
Help_button_step.grid(row=4, column=9, columnspan=2, sticky ="NWE")




#Creating Radio Buttons for choosing CCS detection type
#This method was used over tk radio button in order to keep visual style consistent.
#Single
def single_switcher():
    global AC_check_1_single, AC_button_1_single, AC_button_2_single,AC_check_2_single, DS_button_2_single, DS_check_2_single, A, B, C, previous_true
    A = AC_check_1_single.get()
    B = AC_check_2_single.get()
    C = DS_check_2_single.get()
    if "C" in previous_true and C == True:
        print("C")
        AC_button_2_single.destroy()
        AC_check_2_single = BooleanVar(False)
        AC_button_2_single = Checkbutton(tab1, variable=AC_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
        AC_button_2_single.grid(row=4, column=8, sticky = "W")
        AC_button_1_single.destroy()
        AC_check_1_single = BooleanVar(False)
        AC_button_1_single = Checkbutton(tab1, variable=AC_check_1_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
        AC_button_1_single.grid(row=3, column=8, sticky = "W")
        previous_true = ["A","B"]

    elif "B" in previous_true and B == True:
        print("B")
        AC_button_1_single.destroy()
        AC_check_1_single = BooleanVar(False)
        AC_button_1_single = Checkbutton(tab1, variable=AC_check_1_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
        AC_button_1_single.grid(row=3, column=8, sticky = "W")
        DS_button_2_single.destroy()
        DS_check_2_single = BooleanVar(False)
        DS_button_2_single = Checkbutton(tab1, variable=DS_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
        DS_button_2_single.grid(row=4, column=6, sticky = "W")
        previous_true = ["A","C"]

    elif "A" in previous_true and A == True:
        print("A")
        AC_button_2_single.destroy()
        AC_check_2_single = BooleanVar(False)
        AC_button_2_single = Checkbutton(tab1, variable=AC_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
        AC_button_2_single.grid(row=4, column=8, sticky = "W")
        DS_button_2_single.destroy()
        DS_check_2_single = BooleanVar(False)
        DS_button_2_single = Checkbutton(tab1, variable=DS_check_2_single, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: single_switcher())
        DS_button_2_single.grid(row=4, column=6, sticky = "W")
        previous_true = ["B","C"]
#Slim
def slim_switcher():
    global AC_check_1_slim, AC_button_1_slim, AC_button_2_slim,AC_check_2_slim, DS_button_2_slim, DS_check_2_slim, A, B, C, previous_true
    A = AC_check_1_slim.get()
    B = AC_check_2_slim.get()
    C = DS_check_2_slim.get()
    if "C" in previous_true and C == True:
        print("C")
        AC_button_2_slim.destroy()
        AC_check_2_slim = BooleanVar(False)
        AC_button_2_slim = Checkbutton(tab2, variable=AC_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
        AC_button_2_slim.grid(row=4, column=8, sticky = "W")
        AC_button_1_slim.destroy()
        AC_check_1_slim = BooleanVar(False)
        AC_button_1_slim = Checkbutton(tab2, variable=AC_check_1_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
        AC_button_1_slim.grid(row=3, column=8, sticky = "W")
        previous_true = ["A","B"]

    elif "B" in previous_true and B == True:
        print("B")
        AC_button_1_slim.destroy()
        AC_check_1_slim = BooleanVar(False)
        AC_button_1_slim = Checkbutton(tab2, variable=AC_check_1_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
        AC_button_1_slim.grid(row=3, column=8, sticky = "W")
        DS_button_2_slim.destroy()
        DS_check_2_slim = BooleanVar(False)
        DS_button_2_slim = Checkbutton(tab2, variable=DS_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
        DS_button_2_slim.grid(row=4, column=6, sticky = "W")
        previous_true = ["A","C"]

    elif "A" in previous_true and A == True:
        print("A")
        AC_button_2_slim.destroy()
        AC_check_2_slim = BooleanVar(False)
        AC_button_2_slim = Checkbutton(tab2, variable=AC_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
        AC_button_2_slim.grid(row=4, column=8, sticky = "W")
        DS_button_2_slim.destroy()
        DS_check_2_slim = BooleanVar(False)
        DS_button_2_slim = Checkbutton(tab2, variable=DS_check_2_slim, onvalue=True, offvalue=False, bg="grey", fg ="blue", command=lambda: slim_switcher())
        DS_button_2_slim.grid(row=4, column=6, sticky = "W")
        previous_true = ["B","C"]

window.mainloop()


