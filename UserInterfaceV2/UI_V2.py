#!/usr/bin/env python3.9

# Author: Jeremy Jacobson 
# Email: jeremy.jacobson@pnnl.gov

from time import sleep
import tkinter as tk
import tkinter.filedialog
from tkinter.ttk import *
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter.messagebox import askyesno
from tkinter import messagebox as msg
from tkinter import font
import os
import threading
from ttkthemes import ThemedTk
import json
import tkButton
import platform
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import Pipeline_V2
from matplotlib.lines import Line2D
from tkPDFViewer import tkPDFViewer as pdf
import multiprocessing


#issue with __name == main with pyinstaller ??

# Initialize application
#This first line is required to allow this to work with pyinstaller / subprocesses.
if __name__=="__main__":
    #This may be needed for pyinstaller.
    multiprocessing.freeze_support()
    #Set working directory
    cur_dir = os.path.dirname(__file__)
    os.chdir(cur_dir)
    # Initialize application     
    window = ThemedTk(theme="none")
    window.title("IMMS Workflow Automation Dashboard",)
    window.config(bg='#0C74BA')


    #initilize variables
    label_list = []
    entry_list = []
    entry_file_dict= {}
    entry_param_dict = {}
    button_list = []
    global_file_dictionary = {}
    mode_create_switch = True
    save_switch = False
    freeze_run = False
    ExpName = ""
    DriftKernel = ""
    LCKernel = ""
    MinIntensity = ""
    ExpType = ""
    ToolType = ""
    last_tool=""
    tool_check = ""
    last_mode=""

    #Modify this list and also "open_file" function to allow for more files types.
    possible_files = ["Raw Data Folder","PreProcessed Data Folder","Feature Data Folder","IMS Metadata Folder","IMS Metadata Folder (optional)",
                        "Calibrant File","Target List File","Target List File (optional)","Metadata File","mzML Data Folder"]


    #Create Initial Buttons on screen. - Instructions/"IMMS dashboard" buttons are created at end of script because they includes functions created later.
    Mode_Frame = LabelFrame(window)
    Mode_Frame.grid(row=1, column = 0, sticky="NSWE")
    Mode_Frame.grid_columnconfigure(0, weight=1)
    Mode_buttons = tkButton.Button(Mode_Frame, text = "Workflow", height = 40, width = 120, bordersize=1,bg='lightgrey', command=lambda: [create_modes(),hide_instructions()])
    Mode_buttons.grid(row=0, column = 0, sticky="NEWS")

    Tool_Frame = LabelFrame(window)
    Tool_Frame.grid(row=1, column = 1, sticky="NSWE")
    Tool_Frame.grid_columnconfigure(0, weight=1)
    Gen_tool_buttons = tkButton.Button(Tool_Frame, text = "Tools", height = 40, width = 160, command=lambda: [create_tools("disabled","active","active","active","active"),hide_instructions()],bg='lightgrey', bordersize=1)
    Gen_tool_buttons.grid(row=0, column = 0, sticky="NEWS")

    Data_Frame = LabelFrame(window)
    Data_Frame.grid(row=1, column = 2, sticky="NSWE")
    Data_Frame.grid_columnconfigure(0, weight=1)
    Gen_Data_Stuff = tkButton.Button(Data_Frame, text = "Data", height = 40, width = 400, command=lambda: [create_modes(),create_tools("disabled","active","active","active","active"),hide_instructions(),data_instruction()],bg='lightgrey', bordersize=1)
    Gen_Data_Stuff.grid(row=0, column = 0, columnspan=10, sticky="NEWS")

    Run_Frame = LabelFrame(window)
    Run_Frame.grid(row=1, column = 3, sticky="NSWE")
    Run_Frame.grid_columnconfigure(0, weight=1)
    Gen_Run_Stuff = tkButton.Button(Run_Frame, text = "Run", height = 40, width = 400,bg='lightgrey',command = lambda: create_run(), bordersize=1)
    Gen_Run_Stuff.grid(row=0, column = 0, sticky="NEWS")

    # Instructions and Defaults
    #The following functions display instructions and tool/mode buttons.

    def Show_instructions():
        global Cover_frame, mode_create_switch,freeze_run
        mode_create_switch = True
        if freeze_run == False:
            hide_run()
            l1=tkButton.Button(window,text="  IMMS Workflow Automation Dashboard ", font=("default", 30), width = 45,bg="lightgreen")
            l1.grid(row=0, column = 0, columnspan=10, ipady=(10), sticky="EW")
            Cover_frame = LabelFrame(window)
            Cover_frame.grid(row=2,column=0,columnspan=10,rowspan=9,sticky = "NEWS")
            Cover_frame.columnconfigure((1,2,3,4,5,6,7,8,9,10), minsize=int(40))
            Cover_frame.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=int(20))
            l3=Label(Cover_frame,text="Welcome to the Ion Mobility Mass Spec workflow automation tool. This dashboard is designed to \nfacilitate processing multiple rounds of Ion Mobility MS using previously developed tools.", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
            l3.grid(row=2, column = 5, columnspan=10, rowspan=2, sticky="NEWS")

            l4=Label(Cover_frame,text="The default mode of operation is the Single Tool mode. You can run any single tool by selecting \nthe Tools tab above. This will populate the Data tab where you may upload files, select folders,\nand add parameters to your analysis. Then you may Run the pipeline to analyze your results. ", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
            l4.grid(row=6, column = 5, columnspan=10, rowspan=2, sticky="NEWS")

            l5=Label(Cover_frame,text="You can also run multiple tools at once by selecting the Workflow tab and choosing a \npre-configured workflow. ", font=("default", 14),borderwidth=0, relief="solid", justify="left", anchor = "w")
            l5.grid(row=10, column = 5, columnspan=10, rowspan=2, sticky="NEWS")
        try:
            hide_tools()
        except:
            pass
        try:
            hide_modes()
        except:
            pass
        try:
            hide_data_frame()
        except:
            pass

#These are located below "Workflow" in GUI
    def create_modes(*args):
        global Single_tool_button,Single_field_button, Stepped_field_button,SLIM_button, mode_create_switch
        if mode_create_switch == True:
            Single_tool_button = tkButton.Button(Mode_Frame, height = 50, width = 100, text = "Single Tools", bordersize=1, command = lambda: [hide_tools(),create_tools("disabled","active","active","active","active"),change_mode_color(Single_tool_button)])
            Single_tool_button.grid(row=1, column = 0, sticky="NEWS")
            Single_field_button = tkButton.Button(Mode_Frame, height = 50, width = 100, text = "Single Field", bordersize=1, command = lambda: create_single_field(Single_field_button))
            Single_field_button.grid(row=2, column = 0, sticky="NEWS")
            Stepped_field_button = tkButton.Button(Mode_Frame, height = 50, width = 100, text = "Stepped Field", bordersize=1, command = lambda:create_stepped_field(Stepped_field_button))
            Stepped_field_button.grid(row=3, column = 0, sticky="NEWS")
            SLIM_button= tkButton.Button(Mode_Frame, height = 50, width = 100, text = "SLIM", bordersize=1, command = lambda:create_slim_field(SLIM_button))
            SLIM_button.grid(row=4, column = 0, sticky="NEWS")
            mode_create_switch = False

#These are located below "Tools" in GUI
    def create_tool_instructions():
        global Tool_instruction_frame,freeze_run
        if freeze_run ==False: 
            hide_run()

        Tool_instruction_frame = LabelFrame(Data_Frame)
        Tool_instruction_frame.grid(row=2,column=0,columnspan=10,rowspan=9,sticky = "NEWS")
        Tool_instruction_frame.columnconfigure((1,2,3,4,5,6,7,8,9,10), minsize=int(40))
        Tool_instruction_frame.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17), minsize=int(20))

        l7=Label(Tool_instruction_frame,text="Tool Descriptions", font=("default", 18, "bold"),borderwidth=0, relief="solid",anchor="w")
        l7.grid(row=1, column = 3, columnspan=10, rowspan=1, sticky="NEWS")
        
        l8=Label(Tool_instruction_frame,text="PNNL PreProcessor", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
        l8.grid(row=3, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

        l9=Label(Tool_instruction_frame,text="Sum frames and smooth raw data. (Unavailable)", font=("default", 14),borderwidth=0, relief="solid",anchor="w")
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

        l15=Label(Tool_instruction_frame,text="Feature detection is used from this advanced suite of tools.", font=("default", 14),borderwidth=0, relief="solid",anchor="w")
        l15.grid(row=13, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

        l16=Label(Tool_instruction_frame,text="AutoCCS", font=("default", 14, "bold"),borderwidth=0, relief="solid",anchor="w")
        l16.grid(row=15, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

        l17=Label(Tool_instruction_frame,text='Calculate collision cross-section values from feature files \nusing "standard" or "enhanced" methods.', font=("default", 14),borderwidth=0, relief="solid",anchor="w", justify="left")
        l17.grid(row=16, column = 3, columnspan=10, rowspan=1, sticky="NEWS")

#These are located below "Data" in GUI
    def data_instruction():
        global l2
        hide_data_frame()
        Data_Frame.rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17), minsize=int(0))
        Data_Frame.rowconfigure(1, minsize=70)
        l2=Label(Data_Frame,text="Select a tool on the left to begin your analysis.\nThen you will be prompted to upload your Data\nfiles and select parameters as needed. ", font=("default", 14),borderwidth=0, relief="solid", width = 45, justify="left",anchor="center")
        l2.grid(row=4, column = 0, columnspan=10, rowspan=5, sticky="NEWS")

#This function controls which tools are "active"/"disabled" (state) and their colors.
    def create_tools(PP_state,PW_state,MZ_state,DM_state,AC_state,PP_color="grey",PW_color="grey",MZ_color="grey",DM_color="grey",AC_color="grey"):
        global PP,PW,MZ,DM,AC
        try:
            hide_tools()
            hide_data_frame()
        except:
            pass
        if PP_state =="active":
            PP = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "PNNL PreProcessor???",bordersize=1, command = lambda: [change_tool_color(PP),PP_create()])
        if PP_state == "disabled":
            PP = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "PNNL PreProcessor",bordersize=1,bg=PP_color)
        PP.grid(row=1, column = 0, sticky="NEWS")
        if PW_state == "active":
            PW = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "ProteoWizard", bordersize=1,command = lambda: [change_tool_color(PW),PW_create()])
        if PW_state == "disabled":
            PW = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "ProteoWizard", bordersize=1,bg=PW_color)
        PW.grid(row=2, column = 0, sticky="NEWS")
        if MZ_state == "active":
            MZ = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "MZmine", bordersize=1,command = lambda: [change_tool_color(MZ),MZ_create()])
        if MZ_state == "disabled":
            MZ = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "MZmine", bordersize=1,bg=MZ_color)
        MZ.grid(row=3, column = 0, sticky="NEWS")
        if DM_state=="active":
            DM = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "DEIMoS", bordersize=1,command = lambda: [change_tool_color(DM), DM_create()])
        if DM_state =="disabled":
            DM = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "DEIMoS", bordersize=1,bg=DM_color)
        DM.grid(row=4, column = 0, sticky="NEWS")
        if AC_state == "active":
            AC = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "AutoCCS", bordersize=1,command = lambda: [change_tool_color(AC),AC_page_create()])
        if AC_state == "disabled":
            AC = tkButton.Button(Tool_Frame, height = 40, width = 100, text = "AutoCCS", bordersize=1,bg=AC_color)
        AC.grid(row=5, column = 0, sticky="NEWS")
        Mode_buttons = tkButton.Button(Mode_Frame, text = "Workflow", height = 40, width = 120, bordersize=1,bg='lightgrey', command=lambda: [create_modes(),create_tools("disabled","active","active","active","active"),hide_instructions()])
        Mode_buttons.grid(row=0, column = 0, sticky="NEWS")
        create_tool_instructions()

#These two functions change colors of the current button and the previous button when selected.
    def change_mode_color(button):
        global last_mode
        button.configurebg(bg="#FBB80F")
        if last_mode != "" and last_mode != button:
            last_mode.configurebg(bg="white")
        last_mode = button

    def change_tool_color(button):
        global last_tool,tool_check
        button.configurebg(bg="#FBB80F")
        if last_tool != "" and last_tool != button:
            last_tool.configurebg(bg="white")
        last_tool = button
        tool_check = button

#These are located below "Run" in GUI
    def create_run():
        global Run_button, Reset_button, l47,l48,freeze_run
        hide_instructions()
        if freeze_run ==False:
            hide_run()
            if tool_check != "":
                Run_Frame.rowconfigure((1,2,3,4,5,6,7), minsize=int(20))
                l47 = Label(Run_Frame,text="Please check parameters and file locations before\nrunning experiment. When complete, you may\nview a preview of the results and select a\nlocation to save the results folder.", font=("default", 14),borderwidth=0, relief="solid", width = 45, justify="left")
                l47.grid(row =2, column = 0,columnspan = 3)        
                Run_button = tk.Button(Run_Frame, text="Run\nExperiment", font=("default", 16), command = lambda: Run_Experiment(), height=3, width=12, bg="silver", fg= "darkgreen")
                Run_button.grid(row=4, column=0, rowspan=2, columnspan=2)
            elif tool_check == "":
                Run_Frame.rowconfigure((1,2,3,4,5,6,7), minsize=int(0))
                Run_Frame.rowconfigure((1), minsize=int(70))
                Run_Frame.rowconfigure((3), minsize=int(60))
                l48 = Label(Run_Frame,text="Before running an experiment, a tool\n or workflow must be selected.", font=("default", 14),borderwidth=0, relief="solid", width = 45, justify="left",anchor="center")
                l48.grid(row =2, column = 0,sticky="NEWS")      


    # Create Tool Reqs
    #This function is responsible for generating all user inputs (labels, entry boxes, browse buttons)
    #that populate the "Data" region.
    #This function is re-used for each tool/workflow.
    def generate_tool_page(input_list,tool_title):
        global label_list,entry_list,entry_file_dict,entry_param_dict,button_list
        label_list = []
        entry_list = []
        entry_param_dict = {}
        button_list = []
        entry_file_dict = {}

        row_counter = 1
        lab_num = 0
        if tool_title != "":
            label_list.append(Label(Data_Frame,text=tool_title, font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="center", anchor="center"))
            label_list[lab_num].grid(row=row_counter, column = 0, columnspan=5, rowspan=1, sticky="NWS")
            row_counter +=1
            lab_num +=1

        label_list.append(Label(Data_Frame,text="Upload the required data below and select Run to begin analysis.", font=("default", 14, "bold"),borderwidth=0, relief="solid", justify="left", anchor="w"))
        label_list[lab_num].grid(row=row_counter, column = 0, columnspan=5, rowspan=1, sticky="NWS")
        row_counter +=2
        lab_num +=1
        label_list.append(Label(Data_Frame,text="Files", font=("default", 14, "bold"),borderwidth=0, relief="solid",justify="left", anchor="w"))
        label_list[lab_num].grid(row=row_counter, column = 0, columnspan=1, rowspan=1, sticky="NWS")
        lab_num +=1

        row_counter = 4
        entry_counter = 0
        button_counter = 0
        param_label = False
        for item in input_list:
            if item in possible_files:
                label_list.append(Label(Data_Frame,text=item, font=("default", 14),borderwidth=1, justify="left", anchor="w"))
                label_list[lab_num].grid(row=row_counter, column = 0, columnspan=1, rowspan=1, sticky="NWS")
                entry_file_dict[str(item)] = tk.StringVar()
                entry_list.append(ttk.Entry(Data_Frame,textvariable = entry_file_dict[str(item)],state = DISABLED,width=50, font=("default",10,"bold")))
                entry_list[entry_counter].grid(row=row_counter, column = 2, columnspan=3, rowspan=1, sticky="NEWS")
                button_list.append(Button(Data_Frame, height=1, width =6, text="Browse", command = lambda item=item: open_file(item,global_file_dictionary,entry_file_dict[item])))
                button_list[button_counter].grid(row=row_counter, column = 7)
                lab_num +=1
                entry_counter +=1
                row_counter +=1
                button_counter +=1
            if item not in possible_files:
                if param_label == False:
                    row_counter +=1
                    label_list.append(Label(Data_Frame,text="Parameters", font=("default", 14, "bold"),borderwidth=0, relief="solid",  justify="left", anchor="w"))
                    label_list[lab_num].grid(row=row_counter, column = 0, columnspan=1, rowspan=1, sticky="NWS")
                    param_label = True
                    lab_num +=1
                    row_counter +=1
                label_list.append(Label(Data_Frame,text=item, font=("default", 14),borderwidth=1, justify="left", anchor="w"))
                label_list[lab_num].grid(row=row_counter, column = 0, columnspan=1, rowspan=1, sticky="NWS")

                entry_param_dict[str(item)] = tk.StringVar()
                entry_list.append(ttk.Entry(Data_Frame,textvariable = entry_param_dict[str(item)],width=50, font=("default",10,"bold")))
                entry_list[entry_counter].grid(row=row_counter, column = 2, columnspan=3, rowspan=1, sticky="NEWS")
                entry_counter +=1
                row_counter +=1
                lab_num +=1

#In the following functions:
#Exptype and Tooltype are used in Pipeline.py to determine which workflow/tools will be used.
#Modify Tooltype in workflows to change which tools should be run.
#For example: ToolType = ["PW","DM","AC"] will run PW, then DM, then AC.
#To replace DM (Deimos) with MZmine (MZ), use ToolType = ["PW","MZ","AC"] instead.
#Label list informs what files and parameters must be entered. Replace values to change it.



    #PNNL PreProcessor
    def PP_create():
        global global_file_dictionary, ExpType,ToolType
        hide_data_frame()
        create_modes()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "Any"
        ToolType = "PP"
        label_list = ["Raw Data Folder","Experiment Name","Drift Kernel","LC Kernel","Minimum Intensity"]
        generate_tool_page(label_list,"")

    #ProteoWizard
    def PW_create():
        global global_file_dictionary, ExpType,ToolType
        hide_data_frame()
        create_modes()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "Any"
        ToolType = "PW"
        label_list = ["PreProcessed Data Folder","Experiment Name"]
        generate_tool_page(label_list,"")

    def MZ_create():
        global global_file_dictionary, ExpType,ToolType
        hide_data_frame()
        create_modes()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "Any"
        ToolType = "MZ"
        label_list = ["mzML Data Folder","Experiment Name"]
        generate_tool_page(label_list,"")

    def DM_create():
        global global_file_dictionary, ExpType,ToolType
        hide_data_frame()
        create_modes()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "Any"
        ToolType = "DM"
        label_list = ["mzML Data Folder","Experiment Name"]
        generate_tool_page(label_list,"Not yet supported with SLIM.\n")


    #AutoCCS Page with buttons for single, stepped, and slim
    def AC_page_create():
        global l36,AC_single_button,AC_stepped_button,AC_slim_button,tool_check
        hide_data_frame()
        create_modes()
        change_mode_color(Single_tool_button)
        tool_check = ""
        Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(40))
        Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(40))
        l36=Label(Data_Frame,text="Select Experiment Type", font=("default", 16, "bold"),borderwidth=0, relief="solid", justify="center", anchor="center")
        l36.grid(row=1, column = 0, columnspan=7, rowspan=1, sticky="NWES")
        AC_single_button= Button(Data_Frame, height = 1, width = 10, text = "Single Field", bg = "white", command = lambda: AC_single_create())
        AC_single_button.grid(row=3, column = 1, sticky="NEWS")
        AC_stepped_button= Button(Data_Frame, height = 1, width = 10, text = "Stepped Field", bg = "white", command = lambda: AC_stepped_create())
        AC_stepped_button.grid(row=3, column = 3, sticky="NEWS")
        AC_slim_button= Button(Data_Frame, height = 1, width = 10, text = "SLIM", bg = "white", command = lambda: AC_slim_create())
        AC_slim_button.grid(row=3, column = 5, sticky="NEWS")

    #AutoCCS Single Field
    def AC_single_create():
        global global_file_dictionary, ExpType,ToolType,tool_check
        hide_data_frame()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "Single"
        ToolType = "AC"
        tool_check = True
        label_list = ["PreProcessed Data Folder","Feature Data Folder","Calibrant File","IMS Metadata Folder (optional)","Target List File (optional)","Experiment Name"]
        generate_tool_page(label_list,"Single Field")

    #AutoCCS Stepped Field
    def AC_stepped_create():
        global global_file_dictionary, ExpType,ToolType,tool_check
        hide_data_frame()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "Stepped"
        ToolType = "AC"
        tool_check = True
        Data_Frame.rowconfigure((1), minsize=int(40))
        label_list = ["Feature Data Folder","IMS Metadata Folder","Target List File","Experiment Name"]
        generate_tool_page(label_list,"Stepped Field")

    def AC_slim_create():
        global global_file_dictionary, ExpType,ToolType,tool_check
        hide_data_frame()
        change_mode_color(Single_tool_button)
        global_file_dictionary = {}
        ExpType = "SLIM"
        ToolType = "AC"
        tool_check = True
        label_list = ["Feature Data Folder","Calibrant File","Metadata File","Target List File (optional)","Experiment Name"]
        generate_tool_page(label_list,"Structures for Lossless Ion Manipulations")

    #Single Field Workflow
    def create_single_field(Single_field_button):
        global global_file_dictionary, ExpType,ToolType,tool_check
        change_mode_color(Single_field_button)
        hide_tools()
        create_tools("disabled","disabled","disabled","disabled","disabled","grey","#FBB80F","#FBB80F","grey","#FBB80F")
        hide_data_frame()
        create_modes()
        global_file_dictionary = {}
        ExpType = "Single"
        ToolType = ["PW","MZ","AC"]
        tool_check = True
        Data_Frame.rowconfigure((1), minsize=int(40))
        # label_list = ["PreProcessed Data Folder","mzML Data Folder","Feature Data Folder","Metadata File","Calibrant File","IMS Metadata Folder (optional)","Experiment Name"]
        label_list = ["PreProcessed Data Folder","Calibrant File", "IMS Metadata Folder (optional)","Target List File (optional)","Experiment Name"]
        
        #Because mzML files and feature files are generated within the workflow, these are not specified by the user
        if platform.system().upper() == "DARWIN":
            global_file_dictionary["mzML Data Folder"] = os.path.dirname(__file__) + "/III_mzML"
            global_file_dictionary["Feature Data Folder"] = os.path.dirname(__file__) + "/IV_Features_csv/*.csv"
        elif platform.system().upper() == "WINDOWS":
            global_file_dictionary["mzML Data Folder"] = os.path.dirname(__file__) + "\\III_mzML"
            global_file_dictionary["Feature Data Folder"] = os.path.dirname(__file__) + "\IV_Features_csv\*.csv"
        generate_tool_page(label_list, "")

    #Stepped Field Workflow
    def create_stepped_field(Stepped_field_button):
        global global_file_dictionary, ExpType,ToolType,tool_check
        change_mode_color(Stepped_field_button)
        hide_tools()
        create_tools("disabled","disabled","disabled","disabled","disabled","grey","#FBB80F","#FBB80F","grey","#FBB80F")
        hide_data_frame()
        create_modes()
        global_file_dictionary = {}
        ExpType = "Stepped"
        ToolType = ["PW","MZ","AC"]
        tool_check = True
        Data_Frame.rowconfigure((1), minsize=int(40))
        label_list = ["PreProcessed Data Folder","IMS Metadata Folder","Target List File","Experiment Name"]
        if platform.system().upper() == "DARWIN":
            global_file_dictionary["mzML Data Folder"] = os.path.dirname(__file__) + "/III_mzML"
            global_file_dictionary["Feature Data Folder"] = os.path.dirname(__file__) + "/IV_Features_csv/*.csv"
        elif platform.system().upper() == "WINDOWS":
            global_file_dictionary["mzML Data Folder"] = os.path.dirname(__file__) + "\\III_mzML"
            global_file_dictionary["Feature Data Folder"] = os.path.dirname(__file__) + "\IV_Features_csv\*.csv"
        generate_tool_page(label_list, "")


    def create_slim_field(SLIM_button):
        global global_file_dictionary, ExpType,ToolType,tool_check
        change_mode_color(SLIM_button)
        hide_tools()
        create_tools("disabled","disabled","disabled","disabled","disabled","grey","#FBB80F","#FBB80F","grey","#FBB80F")
        hide_data_frame()
        create_modes()
        global_file_dictionary = {}
        ExpType = "SLIM"
        #A Note: Don't replace MZ with Deimos here. It does not currently work with slim.
        ToolType = ["PW","MZ","AC"]
        tool_check = True
        Data_Frame.rowconfigure((1), minsize=int(40))
        label_list = ["PreProcessed Data Folder","Calibrant File","Metadata File","Target List File (optional)","Experiment Name"]
        if platform.system().upper() == "DARWIN":
            global_file_dictionary["mzML Data Folder"] = os.path.dirname(__file__) + "/III_mzML"
            global_file_dictionary["Feature Data Folder"] = os.path.dirname(__file__) + "/IV_Features_csv/*.csv"
        elif platform.system().upper() == "WINDOWS":
            global_file_dictionary["mzML Data Folder"] = os.path.dirname(__file__) + "\\III_mzML"
            global_file_dictionary["Feature Data Folder"] = os.path.dirname(__file__) + "\IV_Features_csv\*.csv"
        generate_tool_page(label_list, "")


    # Hide Functions
    # The following functions are used to hide/delete/refresh the previous results of the tabs they refer to.

    def hide_instructions():
        global Cover_frame
        Cover_frame.grid_remove()
        l1=tkButton.Button(window,text="  IMMS Workflow Automation Dashboard ", font=("default", 30), width = 45, command = lambda: Show_instructions(),bg="lightgreen")
        l1.grid(row=0, column = 0, columnspan=10, ipady=(10), sticky="EW")

    def hide_modes():
        for arg in [Single_tool_button,Single_field_button,Stepped_field_button,SLIM_button]:
            arg.grid_forget()

    def hide_tools():
        global PP,PW,DM,MZ,AC, last_tool,tool_check
        try:
            last_tool = ""
            tool_check = ""
            for arg in [PP,PW,DM,MZ,AC]:
                arg.grid_forget()
        except:
            pass

    def hide_data_frame():
        global freeze_run,label_list,entry_list,entry_file_dict,entry_param_dict,button_list,l36,AC_single_button,AC_stepped_button,AC_slim_button,Tool_instruction_frame,l2
        Data_Frame.columnconfigure((0,1,2,3,4,5,6,7), minsize=int(0))
        Data_Frame.rowconfigure((0,1,2,3,4,5), minsize=int(0))
        try:
            entry_param_dict = {}
            entry_file_dict = {}
            for arg in (label_list + entry_list + button_list):
                arg.grid_remove()
        except:
            pass
        try:
            for arg in [l36,AC_single_button,AC_stepped_button,AC_slim_button]:
                arg.grid_remove()
        except:
            pass
        try:
            l2.grid_remove()
        except:
            pass
        Tool_instruction_frame.grid_remove()
        if freeze_run == False:
            hide_run()

    def hide_run():
        global Run_button, l47,l48, Save_button
        try:
            Run_Frame.rowconfigure((0,1,2,3,4,5,6,7,8), minsize=int(0))
            Run_button.grid_forget()
            l47.grid_forget()
        except:
            pass
        try:
            l48.grid_forget()
        except:
            pass

    #Reset Everything - available after experiment is complete. 
    #If code is run in the future
    def reset_results(all_results):
        global freeze_run, global_file_dictionary, JE, Save_button, Reset_button,save_switch
        answer = askyesno("Reset Experiment and Data", "Are you sure that you want to reset the experiment? Please save all data before confirming.")
        if answer ==True:
            if save_switch == False:
                delete_results(all_results)
            try:
                save_switch = False
                Run_Frame.rowconfigure((1,2,3,4,5,6,7,8), minsize=int(0))
                freeze_run = False
                global_file_dictionary = {}
                Save_button.grid_forget()
                Reset_button.grid_forget()
                JE = []
                hide_tools()
            except:
                pass
            try:
                hide_modes()
            except:
                pass
            try:
                hide_run()
            except:
                pass
            try:
                hide_data_frame()
            except:
                pass
        Show_instructions()


    # Browse Buttons connect to this function.
    def open_file(file_variable,global_files,value_for_entry):
        global entry_file_dict
        """ 
        Choose a folder
        OR
        Choose a file
        """
        if file_variable == "IMS Metadata Folder (optional)":
            file_variable = "IMS Metadata Folder"
        if file_variable == "Target List File (optional)":
            file_variable = "Target List File"

        if file_variable in ["Raw Data Folder","PreProcessed Data Folder","IMS Metadata Folder","Feature Data Folder", "mzML Data Folder"]:
            file = tkinter.filedialog.askdirectory(parent=window,title='Select a file directory')
            
            if file != "":
                if file_variable == "Raw Data Folder":
                    global_files["Raw Data Folder"]=os.path.abspath(file)
                elif file_variable == "PreProcessed Data Folder":
                    global_files["PreProcessed Data Folder"]=os.path.abspath(file)
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
                elif file_variable == "mzML Data Folder":
                    global_files["mzML Data Folder"]=os.path.abspath(file)
                    # if platform.system().upper() == "DARWIN":
                    #     global_files["mzML Data Folder"]= (os.path.abspath(file) + "/*.mzML")
                    # elif platform.system().upper() == "WINDOWS":
                    #     global_files["mzML Data Folder"]= (os.path.abspath(file) + "\*.mzML")
                value_for_entry.set(str(os.path.abspath(file)))

        else:
            file = askopenfile(parent=window, mode = 'rb',title = "Select a file")
            if file != None:
                value_for_entry.set(str(os.path.abspath(file.name)))
                if file_variable == "Metadata File":
                    global_files["Metadata File"]= os.path.abspath(file.name)

                elif file_variable == "calibrant_curves":
                    global_files["calibrant_curves"] = os.path.abspath(file.name)

                elif file_variable == "Calibrant File":
                    global_files["Calibrant File"] = os.path.abspath(file.name)

                elif file_variable == "Target List File":
                    global_files["Target List File"] = os.path.abspath(file.name)



    # Connection to the Backend
    # The following functions are responsible for gathering all user inputs, 
    # writing json files, writing summary files, and passing them to the backend.
    # The Backend connects to Pipeline.py which calls the docker scripts based on the json file.


    def Run_Experiment():
        global global_file_dictionary
        param_dict = collect_parameters()
        try:
            for k,v in param_dict.items():
                if isinstance(v,list) != True:
                    if v == "" or v.isspace() == True:
                        #print("failed in params")
                        Fail_the_test
            if len(global_file_dictionary) == 0:
                Fail_the_test
            for k,v in global_file_dictionary.items():
                if v.isspace() == True or v =="":
                    #print("failed in files")
                    Fail_the_test
        except:
            msg.showerror("Error","Please enter all parameter values and upload all files before running experiment!", icon = "warning")
        else:
            JE = write_to_json(global_file_dictionary)
            write_as_summary(global_file_dictionary)
            thread1 = threading.Thread(target=run_workflow, args = (JE,))
            thread1.start()
            return

#Required for json and summary files
    def collect_parameters():
        global entry_param_dict, ExpType, ToolType
        p_dict ={}
        try:
            p_dict = {"ExpName":entry_param_dict["Experiment Name"].get(),"ExpType": ExpType,"ToolType":ToolType}
            p_dict = {"ExpName":entry_param_dict["Experiment Name"].get(),"ExpType": ExpType,"ToolType":ToolType,"DriftKernel":entry_param_dict["Drift Kernel"].get(),"LCKernel":entry_param_dict["LC Kernel"].get(),"MinIntensity":entry_param_dict["Minimum Intensity"].get()}
        except:
            pass
        return p_dict

#Generate json file 
    def write_to_json(files):
        global_parameter_dictionary = collect_parameters()
        json_export = [global_parameter_dictionary,files]
        json_object = json.dumps(json_export, indent = 4)
        with open("sample.json", "w") as outfile:
            outfile.write(json_object)
        return json_export

#Generate Run_summary.txt
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

#Connect to Pipeline.py - pass json file.
#This also changes the Run button to disabled / Complete.
    def run_workflow(JE):    
        Run_name = JE[0]["ExpName"]
        if Run_name != "" and Run_name.isspace() == False :
            global Run_button, window, Save_button, freeze_run, Reset_button
            freeze_run = True
            Run_button.config(text="In progress", state=DISABLED)
            print("pipeline in progress. this is printed in function \"run_workflow\"")
            cur_dir = os.path.dirname(__file__)
            os.chdir(cur_dir)
            all_results = Pipeline_V2.execute_workflow("sample.json")
            if all_results[4] != "":
                Run_button.config(text="Run Complete \nView Results", font=("default",14), command=lambda:open_results(JE),state=NORMAL)
            else:
                Run_button.config(text="Run Complete", font=("default",14), state=DISABLED)

            Run_Frame.rowconfigure((1,2,3,4,5,6,7), minsize=int(30))
            Reset_button = tk.Button(Run_Frame, text="Clear\nExperiment", font=("default", 12), command = lambda: reset_results(all_results), height=2, width=12, bg="silver", fg= "darkred")
            Reset_button.grid(row=6, column=0, rowspan=2, columnspan=2)
            Save_button = tk.Button(Run_Frame, text="Save Results", font=("default", 14), command=lambda:save_results(all_results,window,Run_name), height=4, width=10, bg="silver", fg= "green")
            Save_button.grid(row=8, column=0, rowspan=1, columnspan=2)

#To Do:
#Add cancel_run Function that stops the workflow mid-run.


# Show Results Preview. 
#either display generated PDF or generate a new kind-of helpful summary graph
    def open_results(JE):
        global save_switch, view_results_at
        if save_switch == False:
            view_results_at = "."

        cur_dir = os.path.dirname(__file__)
        os.chdir(cur_dir)
        if JE[0]["ExpType"] == "Single" or JE[0]["ExpType"] == "SLIM":
            front= Toplevel(window)
            front.geometry("900x600")
            front.title("Results")
            v1 = pdf.ShowPdf()
            if platform.system().upper() == "DARWIN":
                if  JE[0]["ExpType"] == "Single":
                    view_file = view_results_at + "/IV_data/IV_Results/calibration_output.poly.pdf"
                elif  JE[0]["ExpType"] == "SLIM":
                    view_file = view_results_at + "/IV_data/IV_Results/calibration_output.power.pdf"
                v2 = v1.pdf_view(front, pdf_location =view_file, bar=False)
            elif platform.system().upper() == "WINDOWS":
                if  JE[0]["ExpType"] == "Single":
                    view_file = view_results_at + "\\IV_data\\IV_Results\\calibration_output.poly.pdf"
                elif  JE[0]["ExpType"] == "SLIM":
                    view_file = view_results_at + "\\IV_data\\IV_Results\\calibration_output.power.pdf"
                v2 = v1.pdf_view(front, pdf_location =view_file, bar=False)
            v2.grid()
        #step
        elif JE[0]["ExpType"] == "Stepped":
            matplotlib.use('TkAgg')
            if platform.system().upper() == "DARWIN":
                view_file = view_results_at + "/IV_data/IV_Results/ccs_table.tsv"
            elif platform.system().upper() == "WINDOWS":
                view_file = view_results_at + "\\IV_data\\IV_Results\\ccs_table.tsv"
            df = pd.read_csv(view_file, sep='\\t', engine='python')

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
            
#Save results.
#This moves it from the temp directory to a new directory
#Could alter to have the option to copy instead (and this way it could be saved multiple times)
    def save_results(all_results,window,run_name):
        global Save_button, view_results_at, save_switch
        cur_dir = os.path.dirname(__file__)
        os.chdir(cur_dir)
        save_switch = False
        copy_to_dir = tkinter.filedialog.askdirectory(parent=window,title='Select a file directory') +"/" + run_name
        for copy_from_here in all_results:
            if copy_from_here != "" and copy_to_dir != "" and copy_to_dir.isspace() == False and copy_to_dir != ("/" + run_name):
                copy_to_here = copy_to_dir + "/" + os.path.basename(copy_from_here)
                if platform.system().upper() == "DARWIN":
                    command_mac_mkdir = 'mkdir -p "' + copy_to_dir + '"'
                    os.system(command_mac_mkdir)
                    command_mac = 'mv "'  + copy_from_here + '" "' + copy_to_here + '"'
                    os.system(command_mac)
                    command_mac = 'mv "'  + "sample.json" + '" "' + copy_to_dir + '"'
                    os.system(command_mac)
                    command_mac = 'mv "'  + "Run_summary.txt" + '" "' + copy_to_dir + '"'
                    os.system(command_mac)
                if platform.system().upper() == "WINDOWS":
                    command_PC = 'mkdir "' + copy_to_dir + '"'
                    os.system(command_PC)
                    command_PC = 'move /y "'  + copy_from_here + '" "' + copy_to_here + '"'
                    os.system(command_PC)
                    command_PC = 'move /y "'  + "sample.json" + '" "' + copy_to_dir + '\sample.json"'
                    os.system(command_PC)
                    command_PC = 'move /y "'  + "Run_summary.txt" + '" "' + copy_to_dir + '\Run_summary.txt"'
                    os.system(command_PC)
                Save_button.config(text="Results saved.", font=("default", 12),state=DISABLED)
                view_results_at = copy_to_dir
                save_switch = True
        cur_dir = os.path.dirname(__file__)
        os.chdir(cur_dir)
        

    def delete_results(all_results):
        cur_dir = os.path.dirname(__file__)
        os.chdir(cur_dir)
        for file in all_results:
            if file != "":
                if platform.system().upper() == "DARWIN":
                    print("File removed: ", file)
                    command_mac = 'rm -r "'  + file + '"'
                    os.system(command_mac)
                if platform.system().upper() == "WINDOWS":
                    print("File removed: ", file)
                    command_PC = 'rd /s /q "'  + file + '"'
                    os.system(command_PC)


        cur_dir = os.path.dirname(__file__)
        os.chdir(cur_dir)



    ####

    # Show Instructions when app opens!
    Show_instructions()

    window.mainloop()