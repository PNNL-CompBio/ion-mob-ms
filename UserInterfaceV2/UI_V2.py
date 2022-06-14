#!/usr/bin/env python3.9

from email.utils import encode_rfc2231
from fcntl import F_GETFD
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
import threading
import sv_ttk
from ttkthemes import ThemedTk
import json
import pmw
import sys
import tkButton
import platform
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import Pipeline
from matplotlib.lines import Line2D
from tkPDFViewer import tkPDFViewer as pdf







#Set working directory
cur_dir = os.path.dirname(__file__)
os.chdir(cur_dir)
                      
# Initialize application
window = ThemedTk(theme="none")
window.title("IMMS Workflow Automation Dashboard",)
window.config(bg='#0C74BA')
#window.geometry("1500x900")

# tabControl = ttk.Notebook(window)
# tabControl.grid(row=2, rowspan=10,column=7)

# pmw.initialise(window)
# sv_ttk.set_theme("dark")

#Set down-scaling variables based on screen size
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



freeze_run = False
global_file_dictionary = {}
ExpName = ""
DriftKernel = ""
LCKernel = ""
MinIntensity = ""
ExpType = ""
ToolType = ""

def open_file(file_variable,global_files,value_for_entry):
    """ 
    Raw Data Folder - Choose a folder

    All others - Choose a file
    """
    if file_variable in ["Raw Data Folder","IMS Metadata Folder","Feature Data Folder"]:
        file = tkinter.filedialog.askdirectory(parent=window,title='Select a file directory')
        
        # value_for_entry.append(str(os.path.abspath(file)))
        if file != "":
            if file_variable == "Raw Data Folder":
                global_files["Raw Data Folder"]=os.path.abspath(file)

            elif file_variable == "IMS Metadata Folder":
                if platform.system().upper() == "DARWIN":
                    global_files["IMS Metadata Folder"]=(os.path.abspath(file) + "/*.txt")
                elif platform.system().upper() == "WINDOWS":
                    global_files["IMS Metadata Folder"]=(os.path.abspath(file) + "\*.txt")

            elif file_variable == "Feature Data Folder":
                if platform.system().upper() == "DARWIN":
                    global_files["Feature Data Folder"]= (os.path.abspath(file) + "/*.csv")
                elif platform.system().upper() == "WINDOWS":
                    global_files["Feature Data Folder"]= (os.path.abspath(file) + "\*.csv")
            value_for_entry.set(str(os.path.abspath(file)))
    else:
        file = askopenfile(parent=window, mode = 'rb',title = "Select a file")
        if file != None:
            value_for_entry.set(str(os.path.abspath(file.name)))
            if file_variable == "mzML Data Folder":
                global_files["mzML Data Folder"] = os.path.abspath(file.name)

            elif file_variable == "Metadata File":
                global_files["Metadata File"]= os.path.abspath(file.name)

            elif file_variable == "calibrant_curves":
                global_files["calibrant_curves"] = os.path.abspath(file.name)

            elif file_variable == "Calibrant File":
                global_files["Calibrant File"] = os.path.abspath(file.name)

            elif file_variable == "Target List File":
                global_files["Target List File"] = os.path.abspath(file.name)
    return




last_tool=""
tool_check = ""
def change_tool_color(button):
    global last_tool,tool_check
    button.configurebg(bg="#FBB80F")
    if last_tool != "" and last_tool != button:
        last_tool.configurebg(bg="white")
    last_tool = button
    tool_check = button
    


last_mode=""
def change_mode_color(button):
    global last_mode
    button.configurebg(bg="#FBB80F")
    if last_mode != "" and last_mode != button:
        last_mode.configurebg(bg="white")
    last_mode = button


def hide_tools():
    global PP,PW,DM,MZ,AC, last_tool,tool_check
    try:
        last_tool = ""
        tool_check = ""
        for arg in [PP,PW,DM,MZ,AC]:
            arg.grid_forget()
    except:
        pass

def hide_modes():
    for arg in [Single_tool_button,Single_field_button,Stepped_field_button,SLIM_button]:
        arg.grid_forget()


def create_tool_instructions():
    global Tool_instruction_frame,freeze_run
    if freeze_run ==False: 
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    Tool_instruction_frame = LabelFrame(Data_Frame)
    Tool_instruction_frame.grid(row=2,column=0,columnspan=10,rowspan=9,sticky = "NEWS")
    Tool_instruction_frame.columnconfigure((1,2,3,4,5,6,7,8,9,10), minsize=int(40))
    Tool_instruction_frame.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17), minsize=int(20))

    l7=Label(Tool_instruction_frame,text="Tool Descriptions", font=("default", 18, "bold"),borderwidth=0, relief="solid",anchor="w")
    l7.grid(row=1, column = 3, columnspan=10, rowspan=1, sticky="NEWS")
    
    l8=Label(Tool_instruction_frame,text="PNNL PreProcessor", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
    l8.grid(row=3, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l9=Label(Tool_instruction_frame,text="Sum frames and smooth raw data.", font=("default", 14),borderwidth=0, relief="solid",anchor="w")
    l9.grid(row=4, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l10=Label(Tool_instruction_frame,text="ProteoWizard", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
    l10.grid(row=6, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l11=Label(Tool_instruction_frame,text="Convert smoothed or raw data to mzML format.", font=("default", 14),borderwidth=0, relief="solid",anchor="w")
    l11.grid(row=7, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l12=Label(Tool_instruction_frame,text="MZmine", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
    l12.grid(row=9, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l13=Label(Tool_instruction_frame,text="Detect features from mzML files.", font=("default", 14),borderwidth=0, relief="solid",anchor="w")
    l13.grid(row=10, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l14=Label(Tool_instruction_frame,text="DEIMoS", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
    l14.grid(row=12, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l15=Label(Tool_instruction_frame,text="Detect features and calculate collision cross-section values.", font=("default", 14),borderwidth=0, relief="solid",anchor="w")
    l15.grid(row=13, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l16=Label(Tool_instruction_frame,text="AutoCCS", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
    l16.grid(row=15, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

    l17=Label(Tool_instruction_frame,text='Calculate collision cross-section values from feature files \nusing "standard" or "enhanced" methods.', font=("default", 14),borderwidth=0, relief="solid",anchor="w", justify="left")
    l17.grid(row=16, column = 3, columnspan=10, rowspan=1, sticky="NEWS")



def hide_tool_instructions():
    global Tool_instruction_frame
    Tool_instruction_frame.grid_remove()


def PP_create():
    global l18,l19,l20,l21,l22,l23,l24,l25,e1,e2,e3,e4,e5,b1,ExpName, DriftKernel, LCKernel, MinIntensity,global_file_dictionary,ExpType,ToolType, freeze_run
    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    global_file_dictionary = {}
    ExpType = "Any"
    ToolType = "PP"
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    l18=Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w")
    l18.grid(row=1, column = 0, columnspan=5, rowspan=1, sticky="NWS")

    l19=Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w")
    l19.grid(row=3, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l20=Label(Data_Frame,text="Raw Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l20.grid(row=4, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e1_v = tk.StringVar()
    e1 = ttk.Entry(Data_Frame,textvariable = e1_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e1.grid(row=4, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b1 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Raw Data Folder",global_file_dictionary,e1_v))
    b1.grid(row=4,column=7)

    l21=Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w")
    l21.grid(row=6, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l22=Label(Data_Frame,text="Experiment Name", font=("default", 14),borderwidth=0, relief="solid",justify="left", anchor="w")
    l22.grid(row=7, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    ExpName = tk.StringVar()
    e2 = ttk.Entry(Data_Frame, textvariable=ExpName)
    e2.grid(row=7, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    l23=Label(Data_Frame,text="Drift Kernel", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor="w")
    l23.grid(row=9, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    DriftKernel = tk.StringVar()
    e3 = ttk.Entry(Data_Frame, textvariable=DriftKernel)
    e3.grid(row=9, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    l24=Label(Data_Frame,text="LC Kernel", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor="w")
    l24.grid(row=10, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    LCKernel = tk.StringVar()
    e4 = ttk.Entry(Data_Frame, textvariable=LCKernel)
    e4.grid(row=10, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    l25=Label(Data_Frame,text="Minimum Intensity", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor="w")
    l25.grid(row=11, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    MinIntensity = tk.StringVar()
    e5 = ttk.Entry(Data_Frame, textvariable=MinIntensity)
    e5.grid(row=11, column = 2, columnspan=3, rowspan=1, sticky="NEWS")


def PP_hide():
    global l18,l19,l20,l21,l22,l23,l24,l25,e1,e2,e3,e4,e5,b1,ExpName,MinIntensity,LCKernel,DriftKernel
    try:
        for arg in [l18,l19,l20,l21,l22,l23,l24,l25,e5,e1,e2,e3,e4,e5,b1]:
            arg.grid_remove()
    except:
        pass
    try:
        ExpName = ""
        MinIntensity = ""
        LCKernel = ""
        DriftKernel = ""
    except:
        pass

def PW_create():
    global l26,l27,l28,l29,l30,e6,e7,b2,ExpName, global_file_dictionary,ExpType,ToolType,freeze_run

    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    global_file_dictionary = {}
    ExpType = "Any"
    ToolType = "PW"
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    l26=Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w")
    l26.grid(row=1, column = 0, columnspan=5, rowspan=1, sticky="NWS")

    l27=Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w")
    l27.grid(row=3, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l28=Label(Data_Frame,text="Raw Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l28.grid(row=4, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e6_v = tk.StringVar()
    e6 = ttk.Entry(Data_Frame,textvariable=e6_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e6.grid(row=4, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b2 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Raw Data Folder",global_file_dictionary,e6_v))
    b2.grid(row=4,column=7)

    l29=Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w")
    l29.grid(row=6, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l30=Label(Data_Frame,text="Experiment Name", font=("default", 14),borderwidth=0, relief="solid",justify="left", anchor="w")
    l30.grid(row=7, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    ExpName = tk.StringVar()
    e7 = ttk.Entry(Data_Frame, textvariable=ExpName)
    e7.grid(row=7, column = 2, columnspan=3, rowspan=1, sticky="NEWS")


def PW_hide():
    global l26,l27,l28,l29,l30,e6,e7,b2,ExpName
    try:
        for arg in [l26,l27,l28,l29,l30,e6,e7,b2]:
            arg.grid_remove()
    except:
        pass
    try:
        for param in [ExpName]:
            param = tk.StringVar()
    except:
        pass


def AC_create():
    global l36,AC_single_button,AC_stepped_button,AC_slim_button,tool_check,freeze_run
    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    tool_check = ""
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(40))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(40))
    l36=Label(Data_Frame,text="Select Experiment Type", font=("default", 16, "bold"),borderwidth=0, relief="solid", justify="center", anchor="center")
    l36.grid(row=1, column = 0, columnspan=7, rowspan=1, sticky="NWES")
    AC_single_button= Button(Data_Frame, height = 1, width = 8, text = "Single Field", bg = "white", command = lambda: AC_single_create())
    AC_single_button.grid(row=3, column = 1, sticky="NEWS")
    AC_stepped_button= Button(Data_Frame, height = 1, width = 8, text = "Stepped Field", bg = "white", command = lambda: AC_stepped_create())
    AC_stepped_button.grid(row=3, column = 3, sticky="NEWS")
    AC_slim_button= Button(Data_Frame, height = 1, width = 8, text = "SLIM", bg = "red", state = DISABLED)
    AC_slim_button.grid(row=3, column = 5, sticky="NEWS")

def AC_hide():
    global l36,AC_single_button,AC_stepped_button,AC_slim_button
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    try:
        for arg in [l36,AC_single_button,AC_stepped_button,AC_slim_button]:
            arg.grid_remove()
    except:
        pass


def AC_single_create():
    global l31,l32,l33,l34,l35,l36,l37,l38,l39,e8,e9,e10,e11,e12,b3,b4,b5,b6,ExpName,global_file_dictionary,ExpType,ToolType,tool_check,freeze_run
    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    global_file_dictionary = {}
    ExpType = "Single"
    ToolType = "AC"
    tool_check = True
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    l31=Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w")
    l31.grid(row=1, column = 0, columnspan=5, rowspan=1, sticky="NWS")

    l32=Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w")
    l32.grid(row=3, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l33=Label(Data_Frame,text="Feature Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l33.grid(row=4, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e12_v = tk.StringVar()
    e12 = ttk.Entry(Data_Frame,textvariable=e12_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e12.grid(row=4, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b3= Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Feature Data Folder",global_file_dictionary,e12_v))
    b3.grid(row=4,column=7)

    l37=Label(Data_Frame,text="Metadata File", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l37.grid(row=5, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e8_v = tk.StringVar()
    e8 = ttk.Entry(Data_Frame, textvariable=e8_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e8.grid(row=5, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b4 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Metadata File",global_file_dictionary,e8_v))
    b4.grid(row=5,column=7)

    l38=Label(Data_Frame,text="Calibrant File", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l38.grid(row=6, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e9_v = tk.StringVar()
    e9 = ttk.Entry(Data_Frame,textvariable=e9_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e9.grid(row=6, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b5 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Calibrant File",global_file_dictionary,e9_v))
    b5.grid(row=6,column=7)

    l39=Label(Data_Frame,text="IMS Metadata Folder (optional)", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l39.grid(row=7, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e10_v = tk.StringVar()
    e10 = ttk.Entry(Data_Frame,textvariable=e10_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e10.grid(row=7, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b6 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("IMS Metadata Folder",global_file_dictionary,e10_v))
    b6.grid(row=7,column=7)

    l34=Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w")
    l34.grid(row=8, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l35=Label(Data_Frame,text="Experiment Name", font=("default", 14),borderwidth=0, relief="solid",justify="left", anchor="w")
    l35.grid(row=9, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    ExpName = tk.StringVar()
    e11 = ttk.Entry(Data_Frame, textvariable=ExpName)
    e11.grid(row=9, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

def AC_single_hide():
    global l31,l32,l33,l34,l35,l36,l37,l38,l39,e8,e9,e10,e11,e12,ExpName,b3,b4,b5,b6
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    Data_Frame.columnconfigure((0,1,2,3,4,5), minsize=int(0))
    try:
        for arg in [l31,l32,l33,l34,l35,l36,l37,l38,l39,e8,e9,e10,e11,e12,b3,b4,b5,b6]:
            arg.grid_remove()
            
    except:
        pass
    try:
        for param in [ExpName]:
            param = tk.StringVar()
    except:
        pass

def AC_stepped_create():
    global l40,l41,l42,l43,l44,l45,l46,e13,e14,e15,e16,b7,b8,b9,ExpName,global_file_dictionary,ExpType, ToolType,tool_check,freeze_run
    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    ExpType = "Stepped"
    ToolType = "AC"
    tool_check = True
    global_file_dictionary ={}
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    l40=Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w")
    l40.grid(row=1, column = 0, columnspan=5, rowspan=1, sticky="NWS")

    l41=Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w")
    l41.grid(row=3, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l42=Label(Data_Frame,text="IMS Metadata Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l42.grid(row=4, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e13_v = tk.StringVar()
    e13 = ttk.Entry(Data_Frame,textvariable=e13_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e13.grid(row=4, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b7 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("IMS Metadata Folder",global_file_dictionary,e13_v))
    b7.grid(row=4,column=7)

    l43=Label(Data_Frame,text="Feature Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l43.grid(row=5, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e14_v = tk.StringVar()
    e14= ttk.Entry(Data_Frame,textvariable=e14_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e14.grid(row=5, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b8 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Feature Data Folder",global_file_dictionary,e14_v))
    b8.grid(row=5,column=7)    

    l44=Label(Data_Frame,text="Target List File", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l44.grid(row=6, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e15_v = tk.StringVar()
    e15 = ttk.Entry(Data_Frame,textvariable=e15_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e15.grid(row=6, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b9 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Target List File",global_file_dictionary,e15_v))
    b9.grid(row=6,column=7)

    l45=Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w")
    l45.grid(row=8, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l46=Label(Data_Frame,text="Experiment Name", font=("default", 14),borderwidth=0, relief="solid",justify="left", anchor="w")
    l46.grid(row=9, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    ExpName = tk.StringVar()
    e16 = ttk.Entry(Data_Frame, textvariable=ExpName)
    e16.grid(row=9, column = 2, columnspan=3, rowspan=1, sticky="NEWS")



def AC_stepped_hide():
    global l40,l41,l42,l43,l44,l45,l46,e13,e14,e15,e16,ExpName,b7,b8,b9
    Data_Frame.rowconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    try:
        for arg in [l40,l41,l42,l43,l44,l45,l46,e13,e14,e15,e16,b7,b8,b9]:
            arg.grid_remove()
    except:
        pass
    try:
        for param in [ExpName]:
            param = tk.StringVar("")
    except:
        pass


def collect_parameters():
    global ExpType, ToolType,ExpName, DriftKernel, LCKernel, MinIntensity
    p_dict ={}
    try:
        p_dict = {"ExpName":ExpName.get(),"ExpType": ExpType,"ToolType":ToolType}
        p_dict = {"ExpName": ExpName.get(),"ExpType": ExpType,"ToolType":ToolType,"DriftKernel":DriftKernel.get(),"LCKernel":LCKernel.get(),"MinIntensity":MinIntensity.get()}
    except:
        pass
    return p_dict


def create_tools(PP_state,PW_state,MZ_state,DM_state,AC_state,PP_color="grey",PW_color="grey",MZ_color="grey",DM_color="grey",AC_color="grey"):
    global PP,PW,MZ,DM,AC,freeze_run
    try:
        hide_tools()
        hide_tool_instructions()
        hide_empty_data()
        PP_hide()
        PW_hide()
        AC_hide()
        AC_single_hide()
        AC_stepped_hide()
        if freeze_run ==False:
            hide_run()
        hide_single_workflow()
        hide_stepped_workflow()
    except:
        pass
    if PP_state =="active":
        PP = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "PNNL PreProcessor\n ˢᵘᵐ ᶠʳᵃᵐᵉˢ ᵃⁿᵈ ˢᵐᵒᵒᵗʰ ʳᵃʷ ᵈᵃᵗᵃ​",bordersize=1, command = lambda: [change_tool_color(PP),PP_create(),PP_create()])
    if PP_state == "disabled":
        PP = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "PNNL PreProcessor\n ˢᵘᵐ ᶠʳᵃᵐᵉˢ ᵃⁿᵈ ˢᵐᵒᵒᵗʰ ʳᵃʷ ᵈᵃᵗᵃ​",bordersize=1,bg=PP_color)
    PP.grid(row=1, column = 0, sticky="NEWS")
    if PW_state == "active":
        PW = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "ProteoWizard", bordersize=1,command = lambda: [change_tool_color(PW),PW_create()])
    if PW_state == "disabled":
        PW = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "ProteoWizard", bordersize=1,bg=PW_color)
    PW.grid(row=2, column = 0, sticky="NEWS")
    if MZ_state == "active":
        MZ = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "MZmine", bordersize=1,command = lambda: [change_tool_color(MZ)])
    if MZ_state == "disabled":
         MZ = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "MZmine", bordersize=1,bg=MZ_color)
    MZ.grid(row=3, column = 0, sticky="NEWS")
    if DM_state=="active":
        DM = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "DEIMoS", bordersize=1,command = lambda: change_tool_color(DM))
    if DM_state =="disabled":
        DM = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "DEIMoS", bordersize=1,bg=DM_color)
    DM.grid(row=4, column = 0, sticky="NEWS")
    if AC_state == "active":
        AC = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "AutoCCS", bordersize=1,command = lambda: [change_tool_color(AC),AC_create()])
    if AC_state == "disabled":
        AC = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "AutoCCS", bordersize=1,bg=AC_color)
    AC.grid(row=5, column = 0, sticky="NEWS")
    Mode_buttons = tkButton.Button(Mode_Frame, text = "Workflow", height = 40, width = 120, bordersize=1,bg='lightgrey', command=lambda: [create_modes(),create_tools("disabled","active","disabled","disabled","active"),Hide_instructions()])
    Mode_buttons.grid(row=0, column = 0, sticky="NEWS")
    create_tool_instructions()
    
 

def create_single_field(Single_field_button):
    change_mode_color(Single_field_button)
    hide_tools()
    create_tools("disabled","disabled","disabled","disabled","disabled","grey","#FBB80F","grey","grey","#FBB80F")
    create_single_workflow()


def create_stepped_field(Stepped_field_button):
    change_mode_color(Stepped_field_button)
    hide_tools()
    create_tools("disabled","disabled","disabled","disabled","disabled","grey","#FBB80F","grey","grey","#FBB80F")
    create_stepped_workflow()



mode_create_switch = True
def create_modes(*args):
    global Single_tool_button,Single_field_button, Stepped_field_button,SLIM_button, mode_create_switch
    if mode_create_switch == True:
        Single_tool_button = tkButton.Button(Mode_Frame, height = 50, width = 100, text = "Single Tools", bordersize=1, command = lambda: [hide_tools(),create_tools("disabled","active","disabled","disabled","active"),change_mode_color(Single_tool_button)])
        Single_tool_button.grid(row=1, column = 0, sticky="NEWS")
        Single_field_button = tkButton.Button(Mode_Frame, height = 50, width = 100, text = "Single Field", bordersize=1, command = lambda: create_single_field(Single_field_button))
        Single_field_button.grid(row=2, column = 0, sticky="NEWS")
        Stepped_field_button = tkButton.Button(Mode_Frame, height = 50, width = 100, text = "Stepped Field", bordersize=1, command = lambda:create_stepped_field(Stepped_field_button))
        Stepped_field_button.grid(row=3, column = 0, sticky="NEWS")
        SLIM_button= tkButton.Button(Mode_Frame, height = 50, width = 100, text = "SLIM", bordersize=1, bg = "grey")
        SLIM_button.grid(row=4, column = 0, sticky="NEWS")
        mode_create_switch = False
    


def create_single_workflow():
    global l49,l50,l51,l52,l53,l54,l55,l56,l57,e17,e18,e19,e20,e21,e22,b10,b11,b12,b13,b14,ExpName, global_file_dictionary,ExpType,ToolType,tool_check, freeze_run
    hide_tool_instructions()
    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    global_file_dictionary = {}
    ExpType = "Single"
    ToolType = ["PW","AC"]  # Edit code for this...
    tool_check = True
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    l49=Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w")
    l49.grid(row=1, column = 0, columnspan=5, rowspan=1, sticky="NWS")

    l50=Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w")
    l50.grid(row=3, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l51=Label(Data_Frame,text="Raw Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l51.grid(row=4, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e17_v = tk.StringVar()
    e17 = ttk.Entry(Data_Frame,textvariable=e17_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e17.grid(row=4, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b10 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Raw Data Folder",global_file_dictionary,e17_v))
    b10.grid(row=4,column=7)

    l52=Label(Data_Frame,text="Feature Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l52.grid(row=5, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e18_v = tk.StringVar()
    e18 = ttk.Entry(Data_Frame,textvariable=e18_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e18.grid(row=5, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b11= Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Feature Data Folder",global_file_dictionary,e18_v))
    b11.grid(row=5,column=7)

    l53=Label(Data_Frame,text="Metadata File", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l53.grid(row=6, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e19_v = tk.StringVar()
    e19 = ttk.Entry(Data_Frame, textvariable=e19_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e19.grid(row=6, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b12 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Metadata File",global_file_dictionary,e19_v))
    b12.grid(row=6,column=7)

    l54=Label(Data_Frame,text="Calibrant File", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l54.grid(row=7, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e20_v = tk.StringVar()
    e20 = ttk.Entry(Data_Frame,textvariable=e20_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e20.grid(row=7, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b13 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Calibrant File",global_file_dictionary,e20_v))
    b13.grid(row=7,column=7)

    l55=Label(Data_Frame,text="IMS Metadata Folder (optional)", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l55.grid(row=8, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e21_v = tk.StringVar()
    e21 = ttk.Entry(Data_Frame,textvariable=e21_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e21.grid(row=8, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b14 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("IMS Metadata Folder",global_file_dictionary,e21_v))
    b14.grid(row=8,column=7)

    l56=Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w")
    l56.grid(row=9, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l57=Label(Data_Frame,text="Experiment Name", font=("default", 14),borderwidth=0, relief="solid",justify="left", anchor="w")
    l57.grid(row=10, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    ExpName = tk.StringVar()
    e22 = ttk.Entry(Data_Frame, textvariable=ExpName)
    e22.grid(row=10, column = 2, columnspan=3, rowspan=1, sticky="NEWS")




def hide_single_workflow():
    global l49,l50,l51,l52,l53,l54,l55,l56,l57,e17,e18,e19,e20,e21,e22,b10,b11,b12,b13,b14,ExpName,ExpType,ToolType
    try:
        for arg in [l49,l50,l51,l52,l53,l54,l55,l56,l57,e17,e18,e19,e20,e21,e22,b10,b11,b12,b13,b14]:
            arg.grid_remove()
    except:
        pass


def create_stepped_workflow():
    global l58,l59,l60,l61,l62,l63,l64,l65,e23,e24,e25,e26,e27,b15,b16,b17,b18,ExpName,global_file_dictionary,ExpType,ToolType,tool_check,freeze_run
    hide_tool_instructions()
    hide_empty_data()
    PP_hide()
    PW_hide()
    AC_hide()
    AC_single_hide()
    AC_stepped_hide()
    if freeze_run ==False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    global_file_dictionary = {"Raw Data Folder":"","Feature Data Folder":"","IMS Metadata Folder":"","IMS Metadata Folder":"","Target List File":""}
    ExpType = "Stepped"
    ToolType = ["PW","AC"]  # Edit code for this...
    tool_check = True
    Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
    Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
    l58=Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w")
    l58.grid(row=1, column = 0, columnspan=5, rowspan=1, sticky="NWS")

    l59=Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w")
    l59.grid(row=3, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l60=Label(Data_Frame,text="Raw Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l60.grid(row=4, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e23_v = tk.StringVar()
    e23 = ttk.Entry(Data_Frame,textvariable=e23_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e23.grid(row=4, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b15 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Raw Data Folder",global_file_dictionary,e23_v))
    b15.grid(row=4,column=7)

    l61=Label(Data_Frame,text="Feature Data Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l61.grid(row=5, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e24_v = tk.StringVar()
    e24 = ttk.Entry(Data_Frame,textvariable=e24_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e24.grid(row=5, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b16= Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Feature Data Folder",global_file_dictionary,e24_v))
    b16.grid(row=5,column=7)

    l62=Label(Data_Frame,text="IMS Metadata Folder", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l62.grid(row=6, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e25_v = tk.StringVar()
    e25 = ttk.Entry(Data_Frame, textvariable=e25_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e25.grid(row=6, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b17 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("IMS Metadata Folder",global_file_dictionary,e25_v))
    b17.grid(row=6,column=7)

    l63=Label(Data_Frame,text="Target List File", font=("default", 14),borderwidth=1, justify="left", anchor="w")
    l63.grid(row=7, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    e26_v = tk.StringVar()
    e26 = ttk.Entry(Data_Frame,textvariable=e26_v,state = DISABLED,width=50, font=("default",10,"bold"))
    e26.grid(row=7, column = 2, columnspan=3, rowspan=1, sticky="NEWS")

    b18 = Button(Data_Frame, height=1, width =6, text="Browse", command = lambda: open_file("Target List File",global_file_dictionary,e26_v))
    b18.grid(row=7,column=7)


    l64=Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w")
    l64.grid(row=9, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    l65=Label(Data_Frame,text="Experiment Name", font=("default", 14),borderwidth=0, relief="solid",justify="left", anchor="w")
    l65.grid(row=10, column = 0, columnspan=1, rowspan=1, sticky="NWS")

    ExpName = tk.StringVar()
    e27 = ttk.Entry(Data_Frame, textvariable=ExpName)
    e27.grid(row=10, column = 2, columnspan=3, rowspan=1, sticky="NEWS")


def hide_stepped_workflow():
    global l58,l59,l60,l61,l62,l63,l64,l65,e23,e24,e25,e26,e27,b15,b16,b17,b18
    try:
        for arg in [l58,l59,l60,l61,l62,l63,l64,l65,e23,e24,e25,e26,e27,b15,b16,b17,b18]:
            arg.grid_remove()
    except:
        pass


def empty_data():
    global l2,freeze_run
    PP_hide()
    PW_hide()
    AC_hide()
    hide_tool_instructions()
    if freeze_run == False:
        hide_run()
    hide_single_workflow()
    hide_stepped_workflow()
    Data_Frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17), minsize=int(0))
    Data_Frame.rowconfigure(1, minsize=60)
    l2=Label(Data_Frame,text="Select a tool on the left to begin your analysis.\nThen you will be prompted to upload your Data files\nand select parameters as needed. ", font=("default", 14),borderwidth=0, relief="solid", width = int(45//wf), justify="left",anchor="center")
    l2.grid(row=4, column = 0, columnspan=10, rowspan=5, sticky="NEWS")


def hide_empty_data():
    global l2
    try:
        Data_Frame.rowconfigure(1, minsize=0)
        hide_tool_instructions()
        l2.grid_remove()
    except:
        pass

def Show_instructions():
    global Cover_frame, mode_create_switch,freeze_run
    mode_create_switch = True
    if freeze_run == False:
        l1=tkButton.Button(window,text="  IMMS Workflow Automation Dashboard ", font=("default", int(30//wf)), width = int(45//wf),bg="lightgreen")
        l1.grid(row=0, column = 0, columnspan=10, ipady=(10), sticky="EW")
        Cover_frame = LabelFrame(window)
        Cover_frame.grid(row=2,column=0,columnspan=10,rowspan=9,sticky = "NEWS")
        Cover_frame.columnconfigure((1,2,3,4,5,6,7,8,9,10), minsize=int(40))
        Cover_frame.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=int(20))
        l3=Label(Cover_frame,text="Welcome to the Ion Mobility Mass Spec workflow automation tool. This dashboard is designed to \nfacilitate processing multiple rounds of Ion Mobility MS using previously developed tools.", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
        l3.grid(row=2, column = 5, columnspan=10, rowspan=2, sticky="NEWS")

        l4=Label(Cover_frame,text="The default mode of operation is in Single Tool mode. You can begin to run a single tool by \nselecting the Tools tab above. This will bring you to the Data tab to begin uploading files, selecting \nfolders, and adding parameters for your analysis. Then you can Run the pipeline to analyze your \nresults. ", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
        l4.grid(row=6, column = 5, columnspan=10, rowspan=2, sticky="NEWS")

        l5=Label(Cover_frame,text="You can also run multiple tools at once by selecting the Mode tab and choosing a pre-configured \nworkflow. ", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
        l5.grid(row=10, column = 5, columnspan=10, rowspan=2, sticky="NEWS")

        l6=Label(Cover_frame,text="If you would like to run our pre-configured workflows, select one of the buttons below. ", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
        l6.grid(row=13, column = 5, columnspan=10, rowspan=2, sticky="NEWS")
    
    try:
        hide_tools()
        hide_tool_instructions()
    except:
        pass
    try:
        hide_empty_data()
    except:
        pass
    try:
        hide_modes()
    except:
        pass
    try:
        if freeze_run ==False:
            hide_run()
    except:
        pass
    try:
        hide_single_workflow()
    except:
        pass
    try:
        AC_hide()
    except:
        pass
    try:
        AC_single_hide()
    except:
        pass
    try:
        AC_stepped_hide()
    except:
        pass
    try:
        PW_hide()
    except:
        pass
    try:
        PP_hide()
    except:
        pass
    try:
        hide_stepped_workflow()
    except:
        pass



def Hide_instructions():
    global Cover_frame
    Cover_frame.grid_remove()
    l1=tkButton.Button(window,text="  IMMS Workflow Automation Dashboard ", font=("default", int(30//wf)), width = int(45//wf), command = lambda: Show_instructions(),bg="lightgreen")
    l1.grid(row=0, column = 0, columnspan=10, ipady=(10), sticky="EW")


def Restore_cover():
    global Cover_frame
    Cover_frame.grid()

l1=tkButton.Button(window,text="  IMMS Workflow Automation Dashboard ", font=("default", int(30//wf)), width = int(45//wf), command = lambda: Show_instructions(),bg="lightgreen")
l1.grid(row=0, column = 0, columnspan=10, ipady=(10), sticky="EW")


Show_instructions()


Mode_Frame = LabelFrame(window)
Mode_Frame.grid(row=1, column = 0, sticky="NSWE")
Mode_Frame.grid_columnconfigure(0, weight=1)
Mode_buttons = tkButton.Button(Mode_Frame, text = "Workflow", height = 40, width = 120, bordersize=1,bg='lightgrey', command=lambda: [create_modes(),Hide_instructions()])
Mode_buttons.grid(row=0, column = 0, sticky="NEWS")

Tool_Frame = LabelFrame(window)
Tool_Frame.grid(row=1, column = 1, sticky="NSWE")
Tool_Frame.grid_columnconfigure(0, weight=1)
Gen_tool_buttons = tkButton.Button(Tool_Frame, text = "Tools", height = 40, width = 160, command=lambda: [create_tools("disabled","active","disabled","disabled","active"),Hide_instructions()],bg='lightgrey', bordersize=1)
Gen_tool_buttons.grid(row=0, column = 0, sticky="NEWS")

Data_Frame = LabelFrame(window)
Data_Frame.grid(row=1, column = 2, sticky="NSWE")
Data_Frame.grid_columnconfigure(0, weight=1)
Gen_Data_Stuff = tkButton.Button(Data_Frame, text = "Data", height = 40, width = 400, command=lambda: [create_modes(),create_tools("disabled","active","disabled","disabled","active"),Hide_instructions(),empty_data()],bg='lightgrey', bordersize=1)
Gen_Data_Stuff.grid(row=0, column = 0, columnspan=10, sticky="NEWS")

# Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(20))
# Data_Frame.rowconfigure((1,2,3,4,5,6,7), minsize=int(20))


Run_Frame = LabelFrame(window)
Run_Frame.grid(row=1, column = 3, sticky="NSWE")
Run_Frame.grid_columnconfigure(0, weight=1)
Gen_Run_Stuff = tkButton.Button(Run_Frame, text = "Run", height = 40, width = 400,bg='lightgrey',command = lambda: create_run(), bordersize=1)
Gen_Run_Stuff.grid(row=0, column = 0, sticky="NEWS")




def write_to_json(files):
    global_parameter_dictionary = collect_parameters()
    json_export = [global_parameter_dictionary,files]
    json_object = json.dumps(json_export, indent = 4)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    return json_export



def write_as_summary(files):
    f = open("Run_summary.txt", "w")
    f.write("Ion Mobility Application  -  User Selected Input\n\n")
    global_parameter_dictionary = collect_parameters()
    switch = False
    for key,value in global_parameter_dictionary.items():
        if str(key) == "ExpName":
            pline = "Experiment Name:\t" + value + "\n\n"
        if str(key) == "ExpType":
            pline = "Experiment Type:\t" + value + "\n"
        if str(key) == "ToolType":
            if isinstance(value,list) == True:
                counter = 1
                for item in value:
                    pline = "Tool " + str(counter) + " Selected:\t" + item + "\n"    
                    counter +=1
                    f.write(pline)
                continue
            else:
                pline = "Tool Selected:\t\t" + value + "\n"    
        if str(key) in ["DriftKernel", "LCKernel", "MinIntensity"]:
            if str(value).isspace() == False:
                if switch == False: 
                    wline = "\nParameters\n"
                    f.write(wline)
                    switch = True
                pline = str(key) + ":\t\t" + value + "\n"  
            else: 
                continue
        f.write(pline)

    tline = "\nFiles Selected"
    f.write(tline)
    for key,value in files.items():
        fline = "\n" + str(key) + ":\t" + str(value) + "\n" 
        f.write(fline)
    f.close()




#run tab
# pop up - double check parameters.
#Run
#View Results 

def create_run():
    # Run_Frame.columnconfigure((1,2,3), minsize=int(20))
    global Run_button, l47,l48,freeze_run
    Hide_instructions()
    if freeze_run ==False:
        hide_run()
        Run_Frame.rowconfigure((1,2,3,4,5), minsize=int(20))
        if tool_check != "":
            l47 = Label(Run_Frame,text="Please check parameters and file locations before\nrunning experiment. When complete, you may\nview a preview of the results and select a\nlocation to save the results folder.", font=("default", 14),borderwidth=0, relief="solid", width = int(45//wf), justify="left")
            l47.grid(row =2, column = 0)        
            Run_button = tk.Button(Run_Frame, text="Run\nExperiment", font=("default", 16), command = lambda: Run_Experiment(), height=3, width=12, bg="silver", fg= "darkgreen")
            Run_button.grid(row=4, column=0, rowspan=2, columnspan=2)
        elif tool_check == "":
            l48 = Label(Run_Frame,text="Before running an experiment, a tool\n or workflow must be selected.", font=("default", 14),borderwidth=0, relief="solid", width = int(45//wf), justify="left")
            l48.grid(row =2, column = 0)        



def hide_run():
    global Run_button, l47,l48, Save_button
    try:
        Run_Frame.rowconfigure((1,2,3,4,5), minsize=int(0))
        Run_button.grid_forget()
        l47.grid_forget()
    except:
        pass
    try:
        l48.grid_forget()
    except:
        pass




def Run_Experiment():
    global global_file_dictionary
    param_dict = collect_parameters()
    try:
        print(param_dict)
        for k,v in param_dict.items():
            print(k, " and... ", v)
            if isinstance(v,list) != True:
                if v.isspace() == True:
                    print("Here it fails")
                    print(k,v)
                    Fail_the_test
        print("now for files...")
        for k,v in global_file_dictionary.items():
            print(k, " and... ", v)
            if v.isspace() == True or v =="":
                print(k)
                Fail_the_test
    except:
        msg.showerror("Error","Please enter all parameter values and upload all files before running experiment!", icon = "warning")
    else:
        JE = write_to_json(global_file_dictionary)
        write_as_summary(global_file_dictionary)
        thread1 = threading.Thread(target=run_workflow, args = (JE,))
        thread1.start()
        return


def run_workflow(JE):    
    Run_name = JE[0]["ExpName"]
    if Run_name != "" and Run_name.isspace() == False :
        global Run_button, window, Save_button, freeze_run
        freeze_run = True
        Run_button.config(text="In progress", state=DISABLED)
        print("pipeline in progress. this is printed in function \"run_workflow\"")
        all_results = Pipeline.execute_workflow("sample.json")
        if all_results[4] + all_results[3] != "":
            Run_button.config(text="Run Complete \nView Results", font=("default",14), command=lambda:open_results(JE),state=NORMAL)
        else:
            Run_button.config(text="Run Complete", font=("default",14), state=DISABLED)
        
        Run_Frame.rowconfigure((1,2,3,4,5,6,7), minsize=int(30))
        Save_button = tk.Button(Run_Frame, text="Save Results", font=("default", 14), command=lambda:save_results(all_results,window,Run_name), height=4, width=10, bg="silver", fg= "green")
        Save_button.grid(row=7, column=0, rowspan=1, columnspan=2)
    return 


def open_results(JE):
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    if JE[0]["ExpType"] == "Single" or JE[0]["ExpType"] == "SLIM":
        front= Toplevel(window)
        front.geometry("900x600")
        front.title("Results")
        v1 = pdf.ShowPdf()
        if platform.system().upper() == "DARWIN":
            v2 = v1.pdf_view(front,
                    pdf_location =r"./IV_data/IV_Results/calibration_output.poly.pdf", bar=False)
        elif platform.system().upper() == "WINDOWS":
            v2 = v1.pdf_view(front,
                    pdf_location =r".\\IV_data\\IV_Results\\calibration_output.poly.pdf", bar=False)
        v2.grid()
    #step
    elif JE[0]["ExpType"] == "Stepped":
        matplotlib.use('TkAgg')
        if platform.system().upper() == "DARWIN":
            results_loc = os.path.dirname(__file__) + "/IV_data/IV_Results/ccs_table.tsv"
        elif platform.system().upper() == "WINDOWS":
             results_loc = os.path.dirname(__file__) + "\\IV_data\\IV_Results\\ccs_table.tsv"
        df = pd.read_csv(results_loc, sep='\\t', engine='python')

        #set colors
        color_by_Tunemix = []
        names = df.name.to_list()
        for n in names:
            if "tunemix" in n.lower():
                color_by_Tunemix.append("blue")
            else:
                color_by_Tunemix.append("green")
                
        mz = df.loc[df['adduct_mz'] >= 0, 'adduct_mz'].values
        ccs = df.loc[df['ccs'] >= 0, 'ccs'].values
        legend_elements = [Line2D([0], [0], marker='o', color='w', label='Experimental', markerfacecolor='g', markersize=15),
                            Line2D([0], [0], marker='o', color='w', label='Tunemix', markerfacecolor='b', markersize=15)]

        fig, ax = plt.subplots()
        ax.scatter(mz, ccs, color = color_by_Tunemix)
        plt.xlabel("adduct_mz")
        plt.ylabel("ccs")
        plt.title('Results: Adduct_MZ - CCS Values')
        ax.legend(handles=legend_elements, loc='lower right')
        plt.show()
        

def save_results(all_results,window,run_name):
    global Save_button
    copy_to_dir = tkinter.filedialog.askdirectory(parent=window,title='Select a file directory') +"/" + run_name
    for copy_from_here in all_results:
        if copy_from_here != "" and copy_to_dir != "" and copy_to_dir.isspace() == False and copy_to_dir != ("/" + run_name) :
            copy_to_here = copy_to_dir + "/" + os.path.basename(copy_from_here)
            if platform.system().upper() == "DARWIN":
                command_mac_mkdir = 'mkdir -p "' + copy_to_dir + '"'
                os.system(command_mac_mkdir)
                command_mac = 'cp -r "'  + copy_from_here + '" "' + copy_to_here + '"'
                os.system(command_mac)
            if platform.system().upper() == "WINDOWS":
                #command_PC = "copy "  + copy_from_here + " " + copy_to_here
                command_PC = 'xcopy /E /I "'  + copy_from_here + '" "' + copy_to_here + '"'
                # print("ffrom here:", copy_from_here)
                # print("to here: ", copy_to_here)
                os.system(command_PC)
            Save_button.config(text="Saved.\nSave again?", font=("default", 12))
        #To Do - Change saved button after saving.        
        #Save_button.config(text="Saved!", state=DISABLED)












# test_button= Button(window, height = 1, width = 4, text = "TEST", bg = "grey", command = lambda: [write_to_json(global_file_dictionary),write_as_summary(global_file_dictionary)])
# test_button.grid(row=5, column=5, sticky="NEWS")





window.mainloop()