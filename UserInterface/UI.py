#!/usr/bin/env python3.9

from email.contentmanager import raw_data_manager
from email.policy import default
import tkinter as tk
import tkinter.filedialog
from tkinter.ttk import *
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfile
from tkinter import messagebox as msg
from tkinter import font
import os
from turtle import bgcolor, st
import threading
import sv_ttk
from ttkthemes import ThemedTk
import nextflow
import json
import Pmw


#TO DO!
#Edit the Nextflow stuff when I have more info .

#To do - replace nessesary args set with dictionary 
#This will preserve order of file uploads in UI


#To Do:
# Add pops up to all sections.
# Add results to all sections.
# Add colors to all sections.

# !!!
# Add results to all sections.

# To DO:
# Work on visualization for data!!!! 
# be creativve


"""
Front End for ION Mobility Desktop Application


Users can:

Select their experiment type
Build a Pipeline
Fill in required experimental parameters
Upload required files
Run Experiment
Download/View Results

"""

#Notes
#SV Black = #1c1c1c
#Standard Background = #E5E4E2

# Button class
class My_Button(tk.Button):
    def __init__(self, master, txt, r, c, value, col):
        self.a_button = tk.Button(master, text = txt, width=5, height = 2, command = lambda: open_file(value,self.a_button), fg=col)
        self.a_button.grid(row = r, column = c, columnspan = 2, sticky = "w")
        self.val = value
    def doom(self):
        self.a_button.destroy()


necessary_arguments = []
necessary_arguments_colors = []
necessary_files = set()
global_file_dictionary = {"Raw Data": "", "mzML Data": "","Metadata": "", "Feature Data": "","config_data (Hidden)": "", "calibrant_curves": "","calibrant_data": "", "Target List": ""}

#Todo - Compartmentalize the above arguments for each experiment


#Single Field - Initalize Variables

single_input_list = []
single_entry_list = []
single_label_list = []
single_file_list = []
single_file_label_list = []
selected_boxes_single = {}
t1_l8 = ""
t1_l10 = ""

tab1_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],                              #pp_1_args
[["PP_2_arg_1","PP_2_arg_2","PP_2_arg_3"],"#FEA95E"],                                                     #pp_2_args
[["pw_arg_1","pw_arg_2"],"#f11b23"],                                                                      #pw_args
[["ds_1_arg_1","ds_1_arg_2","ds_1_arg_3"],"#FFE54C"],                                                      #ds_1_args
[["ds_2_arg_1","ds_2_arg_2","ds_2_arg_3"],"#FFE54C"],                                                     #ds_2_args
[["ac_1_arg_1","ac_1_arg_2","ac_1_arg_3"],"#7EC4EF"],                                                       #ac_1_args
[["ac_2_arg_1","ac_2_arg_2","ac_2_arg_3"],"#7EC4EF"]]                                                     #ac_2_args

tab1_files_list = [["Raw Data"],                                                           #pp_1_args
["Raw Data"],                                                                              #pp_2_args
["Raw Data"],                                                                              #pw_args
["mzML Data"],                                                                               #ds_1_args
["Metadata","Feature Data", "Calibrant Data"],                                                  #ds_2_args
["Feature Data", "config_data (Hidden)","Metadata","Target List", "Calibrant Data"],         #ac_1_args
["Feature Data", "config_data (Hidden)","Metadata","Target List", "Calibrant Data"]]         #ac_2_args

#SLIM - Initalize Variables
slim_input_list = []
slim_entry_list = []
slim_label_list = []
slim_file_list = []
slim_file_label_list = []
selected_boxes_slim = {}
t2_l8 = ""
t2_l10 = ""

tab2_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],                              #pp_1_args
[["PP_2_arg_1","PP_2_arg_2","PP_2_arg_3"],"#FEA95E"],                                                 #pp_2_args
[["pw_arg_1","pw_arg_2"],"#f11b23"],                                                                  #pw_args
[["ds_1_arg_1","ds_1_arg_2","ds_1_arg_3"],"#FFE54C"],                                                 #ds_1_args
[["ds_2_arg_1","ds_2_arg_2","ds_2_arg_3"],"#FFE54C"],                                                 #ds_2_args
[["ac_1_arg_1","ac_1_arg_2","ac_1_arg_3"],"#7EC4EF"],                                                 #ac_1_args
[["ac_2_arg_1","ac_2_arg_2","ac_2_arg_3"],"#7EC4EF"]]                                                 #ac_2_args

tab2_files_list = [["Raw Data"],                                                             #pp_1_args
["Raw Data"],                                                                                #pp_2_args
["Raw Data"],                                                                                #pw_args
["mzML Data"],                                                                               #ds_1_args
["Metadata","Feature Data", "Calibrant Data"],                                               #ds_2_args
["Feature Data", "config_data (Hidden)","Metadata","Target List", "Calibrant Data"],         #ac_1_args
["Feature Data", "config_data (Hidden)","Metadata","Target List", "Calibrant Data"]]         #ac_2_args

#Stepped Field - Initalize Variables
step_input_list = []
step_entry_list = []
step_label_list = []
step_file_list = []
step_file_label_list = []
selected_boxes_step = {}
t3_l8 = ""
t3_l10 = ""

tab3_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],               #pp_1_args
[["PP_2_arg_1","PP_2_arg_2","PP_2_arg_3"],"#FEA95E"],                                  #pp_2_args
[["pw_arg_1","pw_arg_2"],"#f11b23"],                                                   #pw_args
[["mm_arg_1","mm_arg_2","mm_arg_3"],"#A44CD3"],                                        #mm_1_args
[["ac_1_arg_1","ac_1_arg_2","ac_1_arg_3"],"#7EC4EF"],                                  #ac_1_args
[["ac_2_arg_1","ac_2_arg_2","ac_2_arg_3"],"#7EC4EF"]]                                  #ac_2_args

tab3_files_list = [["Raw Data"],                                                #pp_1_args
["Raw Data"],                                                                   #pp_2_args
["Raw Data"],                                                                   #pw_args
["mzML Data"],                                                                  #mm_1_args
["Feature Data", "config_data (Hidden)","Metadata","Target List"],              #ac_1_args
["Feature Data", "config_data (Hidden)","Metadata","Target List"]]              #ac_2_args


#Maybe Need an extract metadata button?




#SINGLE
#This generates the pipeline (arguments, file uploads, labels, run button) for the single field experiment.
def Generate_pipeline_single(pp_1,pp_2,pw_1,ds_1,ds_2,ac_1,ac_2):
    arguments = locals()
    counter = 0
    global single_label_list, single_input_list, single_entry_list, single_file_list, selected_boxes_single, \
            single_file_label_list, t1_l8, t1_l10, Run_button_single, necessary_files, necessary_arguments, necessary_arguments_colors

    #Reset Pipeline
    for label in range(0,len(single_label_list)):
        single_label_list[label].destroy()
    for entry in range(0,len(single_entry_list)):
        single_entry_list[entry].destroy()
    for lab in range(0,len(single_file_label_list)):
        single_file_label_list[lab].destroy()
    for button in range(0,len(single_file_list)):
        single_file_list[button].doom()
    single_input_list = []
    single_entry_list = []
    single_label_list = []
    single_file_list = []
    single_file_label_list = []
    selected_boxes_single = {}
    necessary_arguments = []
    necessary_arguments_colors = []
    necessary_files = set()
    try:
        Run_button_single.destroy()
        t1_l8.destroy()
        t1_l10.destroy()
    except:
        pass
        #info for json file
    for k,v in arguments.items():
        selected_boxes_single[k] = v

    #Create Pipeline
    for item in arguments.values():
        if item ==True:
            necessary_arguments.extend(tab1_args_list[counter][0])
            necessary_files.update(tab1_files_list[counter])
            for item in range(0,len((tab1_args_list[counter][0]))):
                necessary_arguments_colors.append(tab1_args_list[counter][1])
        counter +=1
    if (arguments["pp_1"] == True or arguments["pp_2"] == True) and "Metadata" in necessary_files:
        necessary_files.remove("Metadata")
    if arguments["pw_1"] == True and "mzML Data" in necessary_files:
        necessary_files.remove("mzML Data")
    if (arguments["ds_1"] == True) and "Feature Data" in necessary_files:
        necessary_files.remove("Feature Data")

    row_placer_t1 = 6
    column_placer_t1 = 1
    num_of_desired_rows = 5
    if len(necessary_arguments) >= 1:
        t1_l8=Label(tab1,text="Enter Parameter Values", font=("Helvetica Neue", 16), height=2)
        t1_l8.grid(row=5, column=1, columnspan=5)
        counter = 0
        for arg in necessary_arguments:
            single_label_list.append(tk.Label(tab1,text=arg, font=("Helvetica Neue",12), anchor="w", width = 20, fg =necessary_arguments_colors[counter]))
            single_label_list[counter].grid(row=row_placer_t1, column = column_placer_t1,pady=(5,5))
            column_placer_t1 += 1
            single_input_list.append(tk.StringVar())
            single_entry_list.append(ttk.Entry(tab1, width=10, justify = "left", textvariable=single_input_list[counter]))
            single_entry_list[counter].grid(row=row_placer_t1, column = column_placer_t1)
            column_placer_t1 -= 1
            row_placer_t1 += 1
            counter += 1
            if counter%6 == num_of_desired_rows:
                column_placer_t1 +=2
                row_placer_t1 = 6
                num_of_desired_rows -=1

        t1_l10=Label(tab1,text="Upload the Following File(s)", font=("Helvetica Neue", 16), height=2)
        t1_l10.grid(row=11, column=1, columnspan=5)
        counter = 0
        row_placer_t1 = 12
        column_placer_t1 = 1
        browse_text =tk.StringVar()
        browse_text.set("Browse")
        for file in necessary_files:
            single_file_label_list.append(tk.Label(tab1,text=file, anchor="w", font=("Helvetica Neue",12), width = 20, bg ="#1c1c1c"))
            single_file_label_list[counter].grid(row=row_placer_t1, column = column_placer_t1, sticky = "w")
            column_placer_t1 += 1
            single_file_list.append(My_Button(tab1, browse_text.get(), row_placer_t1, column_placer_t1, file,'red'))
            column_placer_t1 -= 1
            row_placer_t1 += 1
            counter += 1
        Run_button_single = tk.Button(tab1, text="Run", command=lambda:Run_Experiment(), height=5, width=12, fg= "green")
        Run_button_single.grid(row=12, column=8, rowspan=3)
    return  


#SLIM
#This generates the pipeline (arguments, file uploads, labels, run button) for the slim field experiment.
def Generate_pipeline_slim(pp_1,pp_2,pw_1,ds_1,ds_2,ac_1,ac_2):
    arguments = locals()
    counter = 0
    global slim_label_list, slim_input_list, slim_entry_list, slim_file_list, selected_boxes_slim, \
            slim_file_label_list, t2_l8, t2_l10, Run_button_slim, necessary_files, necessary_arguments, necessary_arguments_colors

    #Reset Pipeline
    for label in range(0,len(slim_label_list)):
        slim_label_list[label].destroy()
    for entry in range(0,len(slim_entry_list)):
        slim_entry_list[entry].destroy()
    for lab in range(0,len(slim_file_label_list)):
        slim_file_label_list[lab].destroy()
    for button in range(0,len(slim_file_list)):
        slim_file_list[button].doom()
    slim_input_list = []
    slim_entry_list = []
    slim_label_list = []
    slim_file_list = []
    slim_file_label_list = []
    necessary_arguments = []
    necessary_arguments_colors = []
    selected_boxes_slim = {}
    necessary_files = set()
    try:
        Run_button_slim.destroy()
        t2_l8.destroy()
        t2_l10.destroy()
    except:
        pass

        #info for json file
    for k,v in arguments.items():
        selected_boxes_slim[k] = v
        #print(k, "=", v)

        #Create Pipeline
    for item in arguments.values():
        if item ==True:
            necessary_arguments.extend(tab2_args_list[counter][0])
            necessary_files.update(tab2_files_list[counter])
            for item in range(0,len((tab2_args_list[counter][0]))):
                necessary_arguments_colors.append(tab2_args_list[counter][1])
        counter +=1
    if (arguments["pp_1"] == True or arguments["pp_2"] == True) and "Metadata" in necessary_files:
        necessary_files.remove("Metadata")
    if arguments["pw_1"] == True and "mzML Data" in necessary_files:
        necessary_files.remove("mzML Data")
    if (arguments["ds_1"] == True) and "Feature Data" in necessary_files:
        necessary_files.remove("Feature Data")
        

    row_placer_t2 = 6
    column_placer_t2 = 1
    num_of_desired_rows = 5
    if len(necessary_arguments) >= 1:
        t2_l8=Label(tab2,text="Enter Parameter Values", font=("Helvetica Neue", 16), height=2)
        t2_l8.grid(row=5, column=1, columnspan=5)
        counter = 0
        for arg in necessary_arguments:
            slim_label_list.append(tk.Label(tab2,text=arg, font=("Helvetica Neue",12), anchor="w", width = 20, fg =necessary_arguments_colors[counter]))
            slim_label_list[counter].grid(row=row_placer_t2, column = column_placer_t2)
            column_placer_t2 += 1
            slim_input_list.append(tk.StringVar())
            slim_entry_list.append(ttk.Entry(tab2, width=10, justify = "left", textvariable=slim_input_list[counter]))
            slim_entry_list[counter].grid(row=row_placer_t2, column = column_placer_t2)
            column_placer_t2 -= 1
            row_placer_t2 += 1
            counter += 1
            if counter%6 == num_of_desired_rows:
                column_placer_t2 +=2
                row_placer_t2 = 6
                num_of_desired_rows -=1

        t2_l10=Label(tab2,text="Upload the Following File(s)", font=("Helvetica Neue", 16), height=2)
        t2_l10.grid(row=11, column=1, columnspan=5)
        counter = 0
        row_placer_t2 = 12
        column_placer_t2 = 1
        browse_text =tk.StringVar()
        browse_text.set("Browse")
        for file in necessary_files:
            slim_file_label_list.append(tk.Label(tab2,text=file, anchor="w", font=("Helvetica Neue",12), width = 20, bg ="#1c1c1c"))
            slim_file_label_list[counter].grid(row=row_placer_t2, column = column_placer_t2, sticky = "w")
            column_placer_t2 += 1
            slim_file_list.append(My_Button(tab2, browse_text.get(), row_placer_t2, column_placer_t2, file,'red'))
            column_placer_t2 -= 1
            row_placer_t2 += 1
            counter += 1
        Run_button_slim = tk.Button(tab2, text="Run", command=lambda:Run_Experiment(), height=5, width=12, fg= "green")
        Run_button_slim.grid(row=12, column=8, rowspan=3)

    return  


#Stepped
def Generate_pipeline_step(pp_1,pp_2,pw_1,mm_1,ac_1,ac_2):
    arguments = locals()
    counter = 0
    global step_label_list, step_input_list, step_entry_list, step_file_list, selected_boxes_step, \
            step_file_label_list, t3_l8, t3_l10, Run_button_step, necessary_arguments, necessary_files, necessary_arguments_colors

    #Reset Pipeline
    for label in range(0,len(step_label_list)):
        step_label_list[label].destroy()
    for entry in range(0,len(step_entry_list)):
        step_entry_list[entry].destroy()
    for lab in range(0,len(step_file_label_list)):
        step_file_label_list[lab].destroy()
    for button in range(0,len(step_file_list)):
        step_file_list[button].doom()
    step_input_list = []
    step_entry_list = []
    step_label_list = []
    step_file_list = []
    step_file_label_list = []
    necessary_arguments = []
    necessary_arguments_colors = []
    selected_boxes_step = {}
    necessary_files = set() 
    try:
        Run_button_step.destroy()
        t3_l8.destroy()
        t3_l10.destroy()
    except:
        pass

        #info for json file
    for k,v in arguments.items():
        selected_boxes_step[k] = v

    #Create Pipeline
    for item in arguments.values():
        if item ==True:
            necessary_arguments.extend(tab3_args_list[counter][0])
            necessary_files.update(tab3_files_list[counter])
            for item in range(0,len((tab3_args_list[counter][0]))):
                necessary_arguments_colors.append(tab3_args_list[counter][1])
        counter +=1
    if (arguments["pp_1"] == True or arguments["pp_2"] == True) and "Metadata" in necessary_files:
        necessary_files.remove("Metadata")
    if arguments["pw_1"] == True and "mzML Data" in necessary_files:
        necessary_files.remove("mzML Data")
    if (arguments["mm_1"] == True) and "Feature Data" in necessary_files:
        necessary_files.remove("Feature Data")
        

    row_placer_t3 = 6
    column_placer_t3 = 1
    num_of_desired_rows = 5
    if len(necessary_arguments) >= 1:
        t3_l8=Label(tab3,text="Enter Parameter Values", font=("Helvetica Neue", 16), height=2)
        t3_l8.grid(row=5, column=1, columnspan=5)
        counter = 0
        for arg in necessary_arguments:
            step_label_list.append(tk.Label(tab3,text=arg, font=("Helvetica Neue",12), anchor="w", width = 20, fg =necessary_arguments_colors[counter]))
            step_label_list[counter].grid(row=row_placer_t3, column = column_placer_t3)
            column_placer_t3 += 1
            step_input_list.append(tk.StringVar())
            step_entry_list.append(ttk.Entry(tab3, width=10, justify = "left", textvariable=step_input_list[counter]))
            step_entry_list[counter].grid(row=row_placer_t3, column = column_placer_t3)
            column_placer_t3 -= 1
            row_placer_t3 += 1
            counter += 1
            if counter%6 == num_of_desired_rows:
                column_placer_t3 +=2
                row_placer_t3 = 6
                num_of_desired_rows -=1

        t3_l10=Label(tab3,text="Upload the Following File(s)", font=("Helvetica Neue", 16), height=2)
        t3_l10.grid(row=11, column=1, columnspan=5)
        counter = 0
        row_placer_t3 = 12
        column_placer_t3 = 1
        browse_text =tk.StringVar()
        browse_text.set("Browse")
        for file in necessary_files:
            step_file_label_list.append(tk.Label(tab3,text=file, anchor="w", font=("Helvetica Neue",12), width = 20, bg ="#1c1c1c"))
            step_file_label_list[counter].grid(row=row_placer_t3, column = column_placer_t3, sticky = "w")
            column_placer_t3 += 1
            step_file_list.append(My_Button(tab3, browse_text.get(), row_placer_t3, column_placer_t3, file,'red'))
            column_placer_t3 -= 1
            row_placer_t3 += 1
            counter += 1
        Run_button_step = tk.Button(tab3, text="Run", command=lambda:Run_Experiment(), height=5, width=12, fg= "green")
        Run_button_step.grid(row=12, column=8, rowspan=3)
    return  

# Open File function - linked to file upload buttons
def open_file(file_variable,button):
    """ 
    Raw data - Choose a folder
    All others - Choose a file
    """
    global global_file_dictionary
    if file_variable == "Raw Data":
        #To do - fix green bug when not selecting directory.
        file = tkinter.filedialog.askdirectory(parent=window,title='Select a file directory')
        if file != "":
            global raw_data_file
            raw_data_file = os.path.abspath(file)
            global_file_dictionary["Raw Data"]=raw_data_file
            button.configure(background="green", fg = "green")
            return raw_data_file
    else:
        file = askopenfile(parent=window, mode = 'rb',title = "Select a file")
        if file_variable == "mzML Data":
            global mz_file
            mz_data_file = os.path.abspath(file.name)
            global_file_dictionary["mzML Data"] = mz_data_file
            button.configure(background="green", fg = "green")
            return mz_data_file

        elif file_variable == "Metadata":
            global meta_file
            meta_data_file = os.path.abspath(file.name)
            global_file_dictionary["Metadata"]=meta_data_file
            button.configure(background="green", fg = "green")
            return meta_data_file

        elif file_variable == "Feature Data":
            global feature_file
            feature_file = os.path.abspath(file.name)
            global_file_dictionary["Feature Data"]= feature_file
            button.configure(background="green", fg = "green")
            return feature_file

        elif file_variable == "config_data (Hidden)":
            global config_file
            config_file = os.path.abspath(file.name)
            global_file_dictionary["config_data (Hidden)"] = config_file
            button.configure(background="green", fg = "green")
            return config_file

        elif file_variable == "calibrant_curves":
            global calibrant_curve_file
            calibrant_curve_file = os.path.abspath(file.name)
            global_file_dictionary["calibrant_curves"] = calibrant_curve_file
            button.configure(background="green", fg = "green")
            return calibrant_curve_file

        elif file_variable == "Calibrant Data":
            global calibrant_data_file
            calibrant_data_file = os.path.abspath(file.name)
            global_file_dictionary["Calibrant Data"] = calibrant_data_file
            button.configure(background="green", fg = "green")
            return calibrant_data_file

        elif file_variable == "Target List":
            global target_list_file
            target_list_file = os.path.abspath(file.name)
            global_file_dictionary["Target List"] = target_list_file
            button.configure(background="green", fg = "green")
            return target_list_file


# Required for tkinter canvas rounded rectange shapes - UX
def round_rectangle(obj, x1, y1, x2, y2, r, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return obj.create_polygon(points, **kwargs, smooth=True)


# This will write to a json file!
def gather_everything_together(*args):
    global necessary_arguments, necessary_files
    counter = -1
    json_args = {}
    for arg in args:
        if counter == -1:
            #print("experiment = :", arg)
            json_exp =  {"Experiment": arg}
        else: 
            #print(necessary_arguments[counter], " = ", arg)
            json_args[necessary_arguments[counter]] = arg
        counter += 1
        #single
    json_files = {}
    if tabControl.index(tabControl.select()) == 0:
        for file in single_file_list:
            #print(file.val, " = ", global_file_dictionary[file.val])
            json_files[file.val] = global_file_dictionary[file.val]
            json_selected = selected_boxes_single
        #slim
    if tabControl.index(tabControl.select()) == 1:
        for file in slim_file_list:
            #print(file.val, " = ", global_file_dictionary[file.val])
            json_files[file.val] = global_file_dictionary[file.val]
            json_selected = selected_boxes_slim
        #step
    if tabControl.index(tabControl.select()) == 2:
        for file in step_file_list:
           #print(file.val, " = ", global_file_dictionary[file.val])
            json_files[file.val] = global_file_dictionary[file.val]
            json_selected = selected_boxes_step

    json_export = [json_exp,json_selected,json_args,json_files]
    json_object = json.dumps(json_export, indent = 4)
    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    return 


def run_nextflow():
    confirmation_step = msg.askquestion("Run Experiment", "Please confirm all arguments before running experiment. There will be no option to cancel run.")
    if confirmation_step == "yes":
        Run_button_single = tk.Button(tab1, text="In progress", height=5, width=12, fg="green").grid(row=12, column=8, rowspan=3)
        Run_button_step = tk.Button(tab1, text="In progress", height=5, width=12, fg="green").grid(row=12, column=8, rowspan=3)
        Run_button_slim = tk.Button(tab1, text="In progress", height=5, width=12, fg="green").grid(row=12, column=8, rowspan=3)
        #os.system("nextflow run hello")
        pipeline = nextflow.Pipeline("main.nf")
        execution = pipeline.run()  
        print("Duration of Pipeline: ", execution.duration)
        print("Standard Out: ", execution.stdout)
        print("Status: ", execution.status)
        Run_button_single = tk.Button(tab1, text="Run Complete. \nView Results.", command=lambda:open_popup(), height=5, width=12, fg="green").grid(row=12, column=8, rowspan=3)
        Run_button_slim = tk.Button(tab1, text="Run Complete. \nView Results.", command=lambda:open_popup(), height=5, width=12, fg="green").grid(row=12, column=8, rowspan=3)
        Run_button_step = tk.Button(tab1, text="Run Complete. \nView Results.", command=lambda:open_popup(), height=5, width=12, fg="green").grid(row=12, column=8, rowspan=3)




#Run Experiment!
#add in nextflow stuff
#add in button changes when clicked.

def Run_Experiment():
    #To do: 
    #Add correct parameters and files required for each
    #Add check_all_values function here too

    #single Field
   if tabControl.index(tabControl.select()) == 0:
            #check for files too
        try:
            error_catch_arguments_single = [var.get() for var in single_input_list if var.get() !='']
            if len(error_catch_arguments_single) != len(single_input_list):
                fail_the_test
        except:
            msg.showerror("Error","Please enter all parameter values and upload all files before running experiment!", icon = "warning")
        else:
            L = [var.get() for var in single_input_list]
            L = [tabControl.index(tabControl.select())] + L
            #add files too
            gather_everything_together(*L)
            thread1 = threading.Thread(target=run_nextflow)
            thread1.start()
    #slim
   elif tabControl.index(tabControl.select()) == 1:
            #check for files too
        try:
            error_catch_arguments_slim = [var.get() for var in slim_input_list if var.get() !='']
            if len(error_catch_arguments_slim) != len(slim_input_list):
                fail_the_test
        except:
            msg.showerror("Error","Please enter all parameter values and upload all files before running experiment!", icon = "warning")
        else:
            L = [var.get() for var in slim_input_list]
            L = [tabControl.index(tabControl.select())] + L
            #L.extend((raw_data_file,target_list_file))
            gather_everything_together(*L)
            thread1 = threading.Thread(target=run_nextflow)
            thread1.start()

   elif tabControl.index(tabControl.select()) == 2:
            #check for files too
        try:
            error_catch_arguments_step = [var.get() for var in step_input_list if var.get() !='']
            if len(error_catch_arguments_step) != len(step_input_list):
                fail_the_test
        except:
            msg.showerror("Error","Please enter all parameter values and upload all files before running experiment!", icon = "warning")
        else:
            L = [var.get() for var in step_input_list]
            L = [tabControl.index(tabControl.select())] + L
            #L.extend((raw_data_file,target_list_file))
            gather_everything_together(*L)
            thread1 = threading.Thread(target=run_nextflow)
            thread1.start()


#Results Popup
def open_popup():
    top= Toplevel(window)
    top.geometry("1000x500")
    top.title("Child Window")
    results = open("./sample.json", "r")
    text_box = tk.Text(top, height = 20, width = 60, padx=15, pady=15)
    for line in results:
        text_box.insert(tkinter.END, line)
    text_box.config(state=DISABLED)
    text_box.grid(row = 1, column = 1)


#Layout
# Initialize application
window = ThemedTk(theme="none")
window.title("PNNL Ion Mobility Application",)
window.config(bg='#0C74BA')
window.geometry("1500x900")
window.columnconfigure(1, weight=1)
window.columnconfigure(8, weight=1)
tabControl = ttk.Notebook(window)
tabControl.grid(row=2, rowspan=10,column=7)
Pmw.initialise(window)
# window.columnconfigure(0,weight=1)
# window.columnconfigure(10,weight=1)
sv_ttk.set_theme("dark")

#Label
l1=Label(window,text="  PNNL Ion Mobility Application  ", font=("default, 30"),borderwidth=1, relief="solid", width = 60).grid(row=0, column = 7, ipady=(10), sticky="EW")
l2=Label(window,text="Experiment", font=("default", 20, "bold"),borderwidth=0, relief="solid", height=2).grid(row=1, column=7, ipadx=(0), pady=(5,0), sticky="EW")
sep = tk.Frame(window, bg="black", height=2, bd=0).grid(row=1, column=7, sticky="EWS", ipadx=(0), padx=(8,8))

#tabs
tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text = "Single Field")
tab1.columnconfigure((1,2,3,4,5,6,7,8,9), minsize=140)
tab1.columnconfigure((0), minsize=20)
tab1.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=40)

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text = "SLIM")
tab2.columnconfigure((0,1,2,3,4,5,6,7,8,9), minsize=140)
tab2.columnconfigure((0), minsize=20)
tab2.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=40)

tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text = "Stepped Field")
tab3.columnconfigure((0,1,2,3,4,5,6,7,8,9), minsize=140)
tab3.columnconfigure((0), minsize=20)
tab3.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=40)

# tab4 = ttk.Frame(tabControl)
# tabControl.add(tab4, text = "Multidimensional")
# tab4.columnconfigure((0,1,2,3,4,5,6,7,8,9), minsize=140)
# tab4.columnconfigure((0), minsize=20)
# tab4.rowconfigure((1,2,3,4,5,6,7,8,9,10,11,12,13,14,15), minsize=40)


##### Single Field Tab  #####
t1_l3=Label(tab1,text="     Build Your Pipeline   ", font=("Helvetica Neue", 18, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "nw", justify = "left").grid(row=1, rowspan=4, column=0, columnspan=10, pady=(5,0), sticky="NEWS")
t1_l11=Label(tab1,text="     Hover over the tools for a description of usage.   ", font=("Helvetica Neue", 14, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "center", justify = "left").grid(row=1, rowspan=1, column=3, columnspan=4, pady=(5,0), sticky="NEWS")

t1_tool_1 = tk.Frame(tab1)
t1_tool_2 = tk.Frame(tab1)
t1_tool_3 = tk.Frame(tab1)
t1_tool_4 = tk.Frame(tab1)
t1_generate_pipeline = tk.Frame(tab1)

t1_canvas1 = tk.Canvas(t1_tool_1 , height=100, width=200, bg ="grey", highlightthickness=0)
t1_canvas2 = tk.Canvas(t1_tool_2 , height=100, width=200, bg ="grey", highlightthickness=0)
t1_canvas3 = tk.Canvas(t1_tool_3 , height=100, width=200, bg ="grey", highlightthickness=0)
t1_canvas4 = tk.Canvas(t1_tool_4 , height=100, width=200, bg ="grey", highlightthickness=0)
t1_canvas5 = tk.Canvas(t1_generate_pipeline, height=101, width=116, bg ="grey", highlightthickness=0)

t1_canvas1.pack()
t1_canvas2.pack()
t1_canvas3.pack()
t1_canvas4.pack()
t1_canvas5.pack()

t1_tool_1.grid(row=2,column=1, columnspan=2,sticky = "W")
t1_tool_2.grid(row=2,column=3, columnspan=2,sticky = "W")
t1_tool_3.grid(row=2,column=5, columnspan=2,sticky = "W")
t1_tool_4.grid(row=2,column=7, columnspan=2,sticky = "W")
t1_generate_pipeline.grid(row=2,column=9, columnspan=2,sticky = "W")


#PNNL PreProcessor
round_rectangle(t1_canvas1, 0, 0, 200, 100, 25, fill="#FE994A")
round_rectangle(t1_canvas1, 5, 5, 195, 95, 25, fill="#FEA95E")
#round_rectangle(canvas1, 20, 20, 180, 80, 25, fill="#FEBF6E")
round_rectangle(t1_canvas1, 20, 20, 180, 80, 25, fill="#FFCD91")
t1_canvas1.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="PNNL PreProcessor")

t1_canvas1_help = Pmw.Balloon(window)
t1_canvas1_help.bind(t1_canvas1, "PNNL PreProcessor\nInput: Raw Data\tOutput: Processed data & metadata\nProcess raw data to reduce noise and highlight features.\nFilter out low count signals with \"minIntensity\".\nPerform smoothing to improve signal of low intensity peaks with \"driftkernel\".\nSum all frames into one by setting \"lcKernel\" to 0.")
t1_canvas1_lbl = t1_canvas1_help.component("label")
t1_canvas1_lbl.config(background="black", foreground="white")

t1_l3=Label(tab1,text="Filter data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=1, columnspan=1)
t1_l4=Label(tab1,text="Smooth data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=1, columnspan=1)

PP_check_1_single = BooleanVar(False)
PP_button_1_single = Checkbutton(tab1, variable=PP_check_1_single, onvalue=True, offvalue=False, bg="grey")
PP_button_1_single.grid(row=3, column=2, sticky = "EW")

PP_check_2_single = BooleanVar(False)
PP_button_2_single = Checkbutton(tab1, variable=PP_check_2_single, onvalue=True, offvalue=False, bg="grey")
PP_button_2_single.grid(row=4, column=2, sticky = "EW")


#ProteoWizard
t1_pw_tag0 = round_rectangle(t1_canvas2, 0, 0, 200, 100, 25, fill="#bd1c1f")
t1_pw_tag1 = round_rectangle(t1_canvas2, 5, 5, 195, 95, 25, fill="#f11b23")
#round_rectangle(canvas2, 20, 20, 180, 80, 25, fill="#ff3a3a")
t1_pw_tag2 = round_rectangle(t1_canvas2, 20, 20, 180, 80, 25, fill="#fd6861")
t1_canvas2.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="ProteoWizard")

t1_canvas2_help = Pmw.Balloon(window) 
t1_canvas2_help.bind(t1_canvas2, "ProteoWizard\nInput: Raw or Preprocessed data\t Output: mzML Files \nThis tool is capable of converting proprietary data (raw or preprocessed) into (gz compressed) mzML files.\nmzML format is universal file type that is required for many open source tools.")
t1_canvas2_lbl = t1_canvas2_help.component("label")
t1_canvas2_lbl.config(background="black", foreground="white")



t1_l5=Label(tab1,text= "  Convert to mzML", font=("default, 14"),borderwidth=0, relief="solid", height=2, bg="grey").grid(row=3, rowspan =1, column=3, columnspan=1, sticky = "w")

PW_check_1_single = BooleanVar(False)
PW_button_1_single = Checkbutton(tab1, variable=PW_check_1_single, onvalue=True, offvalue=False, bg="grey")
PW_button_1_single.grid(row=3, column=4, sticky = "EW")



#DEIMoS
round_rectangle(t1_canvas3, 0, 0, 200, 100, 25, fill="#FFD300")
round_rectangle(t1_canvas3, 5, 5, 195, 95, 25, fill="#FFE54C")
#round_rectangle(canvas3, 20, 20, 180, 80, 25, fill="#FFED73")
round_rectangle(t1_canvas3, 20, 20, 180, 80, 25, fill="#FFFFBF")
t1_canvas3.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="DEIMoS")

t1_canvas3_help = Pmw.Balloon(window)
t1_canvas3_help.bind(t1_canvas3, "DEIMoS\nInput: mzML files & metadata\tOutput: Feature files and/or CCS results\nThis tool has many capabilities including feature detection and CCS calculation.")
t1_canvas3_lbl = t1_canvas3_help.component("label")
t1_canvas3_lbl.config(background="black", foreground="white")



t1_l6=Label(tab1,text="  Feature Detection", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=5, columnspan=1)
t1_l7=Label(tab1,text="Calculate CCS", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=5, columnspan=1)

DS_check_1_single = BooleanVar(False)
DS_button_1_single = Checkbutton(tab1, variable=DS_check_1_single, onvalue=True, offvalue=False, bg="grey")
DS_button_1_single.grid(row=3, column=6, sticky = "EW")

DS_check_2_single = BooleanVar(False)
DS_button_2_single = Checkbutton(tab1, variable=DS_check_2_single, onvalue=True, offvalue=False, bg="grey")
DS_button_2_single.grid(row=4, column=6, sticky = "EW")


#AutoCCS
round_rectangle(t1_canvas4, 0, 0, 200, 100, 25, fill="#5CB6F2")
round_rectangle(t1_canvas4, 5, 5, 195, 95, 25, fill="#7EC4EF")
#round_rectangle(canvas4, 20, 20, 180, 80, 25, fill="#A0D1EC")
round_rectangle(t1_canvas4, 20, 20, 180, 80, 25, fill="#BEDFF1")
t1_canvas4.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="AutoCCS")

t1_canvas4_help = Pmw.Balloon(window)
t1_canvas4_help.bind(t1_canvas4, "AutoCCS\nInput: Feature files \tOutput: CCS results\nThis tool offers two methods of CCS calculations.\nThe \"standard\" method is comparable to DEIMoS.\nThe \"enhanced\" method takes into account the temperature and pressure of the instrument across runs.")
t1_canvas4_lbl = t1_canvas4_help.component("label")
t1_canvas4_lbl.config(background="black", foreground="white")


t1_l8=Label(tab1,text="Calculate CCS (Standard)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=7, columnspan=1)
t1_l9=Label(tab1,text="Calculate CCS (Enhanced)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=7, columnspan=1)

AC_check_1_single = BooleanVar(False)
AC_button_1_single = Checkbutton(tab1, variable=AC_check_1_single, onvalue=True, offvalue=False, bg="grey")
AC_button_1_single.grid(row=3, column=8, sticky = "EW")

AC_check_2_single = BooleanVar(False)
AC_button_2_single = Checkbutton(tab1, variable=AC_check_2_single, onvalue=True, offvalue=False, bg="grey")
AC_button_2_single.grid(row=4, column=8, sticky = "EW")


#Generate Pipeline Button
t1_tag0 = round_rectangle(t1_canvas5, 0, 0, 115, 100, 25, fill="black")
t1_tag1 = round_rectangle(t1_canvas5, 5, 5, 110, 95, 25, fill="#72cc50")
t1_tag2 = t1_canvas5.create_text(57,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="Generate\nNew\nPipeline", justify="center")
t1_tag3 = t1_canvas5.create_rectangle(0, 0, 0, 0, fill="grey", width=0)

t1_canvas5.tag_bind(t1_tag0, "<ButtonPress-1>", lambda event: Generate_pipeline_single(PP_check_1_single.get(),PP_check_2_single.get(),PW_check_1_single.get(),DS_check_1_single.get(),DS_check_2_single.get(),AC_check_1_single.get(),AC_check_2_single.get()))
t1_canvas5.tag_bind(t1_tag1, "<ButtonPress-1>", lambda event: Generate_pipeline_single(PP_check_1_single.get(),PP_check_2_single.get(),PW_check_1_single.get(),DS_check_1_single.get(),DS_check_2_single.get(),AC_check_1_single.get(),AC_check_2_single.get()))
t1_canvas5.tag_bind(t1_tag2, "<ButtonPress-1>", lambda event: Generate_pipeline_single(PP_check_1_single.get(),PP_check_2_single.get(),PW_check_1_single.get(),DS_check_1_single.get(),DS_check_2_single.get(),AC_check_1_single.get(),AC_check_2_single.get()))

t1_canvas5.tag_bind(t1_tag0, "<Enter>", lambda event: t1_canvas5.config(bg="yellow"))
t1_canvas5.tag_bind(t1_tag1, "<Enter>", lambda event: t1_canvas5.config(bg="yellow"))
t1_canvas5.tag_bind(t1_tag2, "<Enter>", lambda event: t1_canvas5.config(bg="yellow"))
t1_canvas5.tag_bind(t1_tag0, "<Leave>", lambda event: t1_canvas5.config(bg="grey"))
t1_canvas5.tag_bind(t1_tag1, "<Leave>", lambda event: t1_canvas5.config(bg="grey"))
t1_canvas5.tag_bind(t1_tag2, "<Leave>", lambda event: t1_canvas5.config(bg="grey"))




#### SLIM Tab ####
t2_l3=Label(tab2,text="     Build Your Pipeline", font=("Helvetica Neue", 18, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "nw", justify = "left").grid(row=1, rowspan=4, column=0, columnspan=10, pady=(5,0), sticky="NEWS")
t2_l11=Label(tab2,text="     Hover over the tools for a description of usage.   ", font=("Helvetica Neue", 14, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "center", justify = "left").grid(row=1, rowspan=1, column=3, columnspan=4, pady=(5,0), sticky="NEWS")

t2_tool_1 = tk.Frame(tab2)
t2_tool_2 = tk.Frame(tab2)
t2_tool_3 = tk.Frame(tab2)
t2_tool_4 = tk.Frame(tab2)
t2_generate_pipeline = tk.Frame(tab2)

t2_canvas1 = tk.Canvas(t2_tool_1 , height=100, width=200, bg ="grey", highlightthickness=0)
t2_canvas2 = tk.Canvas(t2_tool_2 , height=100, width=200, bg ="grey", highlightthickness=0)
t2_canvas3 = tk.Canvas(t2_tool_3 , height=100, width=200, bg ="grey", highlightthickness=0)
t2_canvas4 = tk.Canvas(t2_tool_4 , height=100, width=200, bg ="grey", highlightthickness=0)
t2_canvas5 = tk.Canvas(t2_generate_pipeline , height=101, width=116, bg ="grey", highlightthickness=0)

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


#PNNL PreProcessor
round_rectangle(t2_canvas1, 0, 0, 200, 100, 25, fill="#FE994A")
round_rectangle(t2_canvas1, 5, 5, 195, 95, 25, fill="#FEA95E")
#round_rectangle(canvas1, 20, 20, 180, 80, 25, fill="#FEBF6E")
round_rectangle(t2_canvas1, 20, 20, 180, 80, 25, fill="#FFCD91")
t2_canvas1.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="PNNL PreProcessor")

t2_canvas1_help = Pmw.Balloon(window)
t2_canvas1_help.bind(t2_canvas1, "PNNL PreProcessor\nInput: Raw Data\tOutput: Processed data & metadata\nProcess raw data to reduce noise and highlight features.\nFilter out low count signals with \"minIntensity\".\nPerform smoothing to improve signal of low intensity peaks with \"driftkernel\".\nSum all frames into one by setting \"lcKernel\" to 0.")
t2_canvas1_lbl = t2_canvas1_help.component("label")
t2_canvas1_lbl.config(background="black", foreground="white")

t2_l3=Label(tab2,text="Filter data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=1, columnspan=1)
t2_l4=Label(tab2,text="Smooth data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=1, columnspan=1)

PP_check_1_slim = BooleanVar(False)
PP_button_1_slim = Checkbutton(tab2, variable=PP_check_1_slim, onvalue=True, offvalue=False, bg="grey")
PP_button_1_slim.grid(row=3, column=2, sticky = "EW")

PP_check_2_slim = BooleanVar(False)
PP_button_2_slim = Checkbutton(tab2, variable=PP_check_2_slim, onvalue=True, offvalue=False, bg="grey")
PP_button_2_slim.grid(row=4, column=2, sticky = "EW")


#ProteoWizard
round_rectangle(t2_canvas2, 0, 0, 200, 100, 25, fill="#bd1c1f")
round_rectangle(t2_canvas2, 5, 5, 195, 95, 25, fill="#f11b23")
#round_rectangle(canvas2, 20, 20, 180, 80, 25, fill="#ff3a3a")
round_rectangle(t2_canvas2, 20, 20, 180, 80, 25, fill="#fd6861")
t2_canvas2.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="ProteoWizard")

t2_canvas2_help = Pmw.Balloon(window) 
t2_canvas2_help.bind(t2_canvas2, "ProteoWizard\nInput: Raw or Preprocessed data\t Output: mzML Files \nThis tool is capable of converting proprietary data (raw or preprocessed) into (gz compressed) mzML files.\nmzML format is universal file type that is required for many open source tools.")
t2_canvas2_lbl = t2_canvas2_help.component("label")
t2_canvas2_lbl.config(background="black", foreground="white")


t2_l5=Label(tab2,text= "  Convert to mzML", font=("default, 14"),borderwidth=0, relief="solid", height=2, bg="grey").grid(row=3, rowspan =1, column=3, columnspan=1, sticky = "w")

PW_check_1_slim = BooleanVar(False)
PW_button_1_slim = Checkbutton(tab2, variable=PW_check_1_slim, onvalue=True, offvalue=False, bg="grey")
PW_button_1_slim.grid(row=3, column=4, sticky = "EW")


#DEIMoS
round_rectangle(t2_canvas3, 0, 0, 200, 100, 25, fill="#FFD300")
round_rectangle(t2_canvas3, 5, 5, 195, 95, 25, fill="#FFE54C")
#round_rectangle(canvas3, 20, 20, 180, 80, 25, fill="#FFED73")
round_rectangle(t2_canvas3, 20, 20, 180, 80, 25, fill="#FFFFBF")
t2_canvas3.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="DEIMoS")

t2_l6=Label(tab2,text="  Feature Detection", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=5, columnspan=1)
t2_l7=Label(tab2,text="Calculate CCS", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=5, columnspan=1)

DS_check_1_slim = BooleanVar(False)
DS_button_1_slim = Checkbutton(tab2, variable=DS_check_1_slim, onvalue=True, offvalue=False, bg="grey")
DS_button_1_slim.grid(row=3, column=6, sticky = "EW")

DS_check_2_slim = BooleanVar(False)
DS_button_2_slim = Checkbutton(tab2, variable=DS_check_2_slim, onvalue=True, offvalue=False, bg="grey")
DS_button_2_slim.grid(row=4, column=6, sticky = "EW")

t2_canvas3_help = Pmw.Balloon(window)
t2_canvas3_help.bind(t2_canvas3, "DEIMoS\nInput: mzML files & metadata\tOutput: Feature files and/or CCS results\nThis tool has many capabilities including feature detection and CCS calculation.")
t2_canvas3_lbl = t2_canvas3_help.component("label")
t2_canvas3_lbl.config(background="black", foreground="white")


#AutoCCS
round_rectangle(t2_canvas4, 0, 0, 200, 100, 25, fill="#5CB6F2")
round_rectangle(t2_canvas4, 5, 5, 195, 95, 25, fill="#7EC4EF")
#round_rectangle(canvas4, 20, 20, 180, 80, 25, fill="#A0D1EC")
round_rectangle(t2_canvas4, 20, 20, 180, 80, 25, fill="#BEDFF1")
t2_canvas4.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="AutoCCS")

t2_canvas4_help = Pmw.Balloon(window)
t2_canvas4_help.bind(t2_canvas4, "AutoCCS\nInput: Feature files \tOutput: CCS results\nThis tool offers two methods of CCS calculations.\nThe \"standard\" method is comparable to DEIMoS.\nThe \"enhanced\" method takes into account the temperature and pressure of the instrument across runs.")
t2_canvas4_lbl = t2_canvas4_help.component("label")
t2_canvas4_lbl.config(background="black", foreground="white")

t2_l8=Label(tab2,text="Calculate CCS (Standard)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=7, columnspan=1)
t2_l9=Label(tab2,text="Calculate CCS (Enhanced)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=7, columnspan=1)

AC_check_1_slim = BooleanVar(False)
AC_button_1_slim = Checkbutton(tab2, variable=AC_check_1_slim, onvalue=True, offvalue=False, bg="grey")
AC_button_1_slim.grid(row=3, column=8, sticky = "EW")

AC_check_2_slim = BooleanVar(False)
AC_button_2_slim = Checkbutton(tab2, variable=AC_check_2_slim, onvalue=True, offvalue=False, bg="grey")
AC_button_2_slim.grid(row=4, column=8, sticky = "EW")


#Generate Pipeline Button
t2_tag0 = round_rectangle(t2_canvas5, 0, 0, 115, 100, 25, fill="black")
t2_tag1 = round_rectangle(t2_canvas5, 5, 5, 110, 95, 25, fill="#72cc50")
t2_tag2 = t2_canvas5.create_text(57,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="Generate\nNew\nPipeline", justify="center")
t2_tag3 = t2_canvas5.create_rectangle(0, 0, 0, 0, fill="grey", width=0)

t2_canvas5.tag_bind(t2_tag0, "<ButtonPress-1>", lambda event: Generate_pipeline_slim(PP_check_1_slim.get(),PP_check_2_slim.get(),PW_check_1_slim.get(),DS_check_1_slim.get(),DS_check_2_slim.get(),AC_check_1_slim.get(),AC_check_2_slim.get()))
t2_canvas5.tag_bind(t2_tag1, "<ButtonPress-1>", lambda event: Generate_pipeline_slim(PP_check_1_slim.get(),PP_check_2_slim.get(),PW_check_1_slim.get(),DS_check_1_slim.get(),DS_check_2_slim.get(),AC_check_1_slim.get(),AC_check_2_slim.get()))
t2_canvas5.tag_bind(t2_tag2, "<ButtonPress-1>", lambda event: Generate_pipeline_slim(PP_check_1_slim.get(),PP_check_2_slim.get(),PW_check_1_slim.get(),DS_check_1_slim.get(),DS_check_2_slim.get(),AC_check_1_slim.get(),AC_check_2_slim.get()))


t2_canvas5.tag_bind(t2_tag0, "<Enter>", lambda event: t2_canvas5.config(bg="yellow"))
t2_canvas5.tag_bind(t2_tag1, "<Enter>", lambda event: t2_canvas5.config(bg="yellow"))
t2_canvas5.tag_bind(t2_tag2, "<Enter>", lambda event: t2_canvas5.config(bg="yellow"))
t2_canvas5.tag_bind(t2_tag0, "<Leave>", lambda event: t2_canvas5.config(bg="grey"))
t2_canvas5.tag_bind(t2_tag1, "<Leave>", lambda event: t2_canvas5.config(bg="grey"))
t2_canvas5.tag_bind(t2_tag2, "<Leave>", lambda event: t2_canvas5.config(bg="grey"))


#### Stepped Field #### 
t3_l3=Label(tab3,text="     Build Your Pipeline", font=("Helvetica Neue", 18, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "nw", justify = "left").grid(row=1, rowspan=4, column=0, columnspan=10, pady=(5,0), sticky="NEWS")
t3_l11=Label(tab3,text="     Hover over the tools for a description of usage.   ", font=("Helvetica Neue", 14, "bold"),borderwidth=0, relief="solid", height=2, bg="grey", anchor= "center", justify = "left").grid(row=1, rowspan=1, column=3, columnspan=4, pady=(5,0), sticky="NEWS")


t3_tool_1 = tk.Frame(tab3)
t3_tool_2 = tk.Frame(tab3)
t3_tool_3 = tk.Frame(tab3)
t3_tool_4 = tk.Frame(tab3)
t3_generate_pipeline = tk.Frame(tab3)

t3_canvas1 = tk.Canvas(t3_tool_1 , height=100, width=200, bg ="grey", highlightthickness=0)
t3_canvas2 = tk.Canvas(t3_tool_2 , height=100, width=200, bg ="grey", highlightthickness=0)
t3_canvas3 = tk.Canvas(t3_tool_3 , height=100, width=200, bg ="grey", highlightthickness=0)
t3_canvas4 = tk.Canvas(t3_tool_4 , height=100, width=200, bg ="grey", highlightthickness=0)
t3_canvas5 = tk.Canvas(t3_generate_pipeline , height=101, width=116, bg ="grey", highlightthickness=0)

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


#PNNL PreProcessor
round_rectangle(t3_canvas1, 0, 0, 200, 100, 25, fill="#FE994A")
round_rectangle(t3_canvas1, 5, 5, 195, 95, 25, fill="#FEA95E")
#round_rectangle(canvas1, 20, 20, 180, 80, 25, fill="#FEBF6E")
round_rectangle(t3_canvas1, 20, 20, 180, 80, 25, fill="#FFCD91")
t3_canvas1.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="PNNL PreProcessor")

t3_canvas1_help = Pmw.Balloon(window)
t3_canvas1_help.bind(t3_canvas1, "PNNL PreProcessor\nInput: Raw Data\tOutput: Processed data & metadata\nProcess raw data to reduce noise and highlight features.\nFilter out low count signals with \"minIntensity\".\nPerform smoothing to improve signal of low intensity peaks with \"driftkernel\".\nSum all frames into one by setting \"lcKernel\" to 0.")
t3_canvas1_lbl = t3_canvas1_help.component("label")
t3_canvas1_lbl.config(background="black", foreground="white")

t3_l3=Label(tab3,text="Filter data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=1, columnspan=1)
t3_l4=Label(tab3,text="Smooth data", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=1, columnspan=1)

PP_check_1_step = BooleanVar(False)
PP_button_1_step = Checkbutton(tab3, variable=PP_check_1_step, onvalue=True, offvalue=False, bg="grey")
PP_button_1_step.grid(row=3, column=2, sticky = "EW")

PP_check_2_step = BooleanVar(False)
PP_button_2_step = Checkbutton(tab3, variable=PP_check_2_step, onvalue=True, offvalue=False, bg="grey")
PP_button_2_step.grid(row=4, column=2, sticky = "EW")


#ProteoWizard
round_rectangle(t3_canvas2, 0, 0, 200, 100, 25, fill="#bd1c1f")
round_rectangle(t3_canvas2, 5, 5, 195, 95, 25, fill="#f11b23")
#round_rectangle(canvas2, 20, 20, 180, 80, 25, fill="#ff3a3a")
round_rectangle(t3_canvas2, 20, 20, 180, 80, 25, fill="#fd6861")
t3_canvas2.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="ProteoWizard")

t3_canvas2_help = Pmw.Balloon(window) 
t3_canvas2_help.bind(t3_canvas2, "ProteoWizard\nInput: Raw or Preprocessed data\t Output: mzML Files \nThis tool is capable of converting proprietary data (raw or preprocessed) into (gz compressed) mzML files.\nmzML format is universal file type that is required for many open source tools.")
t3_canvas2_lbl = t3_canvas2_help.component("label")
t3_canvas2_lbl.config(background="black", foreground="white")


t3_l5=Label(tab3,text= "  Convert to mzML", font=("default, 14"),borderwidth=0, relief="solid", height=2, bg="grey").grid(row=3, rowspan =1, column=3, columnspan=1, sticky = "w")

PW_check_1_step = BooleanVar(False)
PW_button_1_step = Checkbutton(tab3, variable=PW_check_1_step, onvalue=True, offvalue=False, bg="grey")
PW_button_1_step.grid(row=3, column=4, sticky = "EW")


#MZMine
round_rectangle(t3_canvas3, 0, 0, 200, 100, 25, fill="#8800C7")
round_rectangle(t3_canvas3, 5, 5, 195, 95, 25, fill="#A44CD3")
#round_rectangle(canvas3, 20, 20, 180, 80, 25, fill="#FFED73")
round_rectangle(t3_canvas3, 20, 20, 180, 80, 25, fill="#E090EF")
t3_canvas3.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="Mzmine")

t3_canvas3_help = Pmw.Balloon(window)
t3_canvas3_help.bind(t3_canvas3, "MZmine\nInput: mzML files & metadata\tOutput: Feature files \nThis open source tool has feature detection capabilities.")
t3_canvas3_lbl = t3_canvas3_help.component("label")
t3_canvas3_lbl.config(background="black", foreground="white")

t3_l6=Label(tab3,text="  Feature Detection", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=5, columnspan=1)
MM_check_1_step = BooleanVar(False)
MM_button_1_step = Checkbutton(tab3, variable=MM_check_1_step, onvalue=True, offvalue=False, bg="grey")
MM_button_1_step.grid(row=3, column=6, sticky = "EW")


#AutoCCS
round_rectangle(t3_canvas4, 0, 0, 200, 100, 25, fill="#5CB6F2")
round_rectangle(t3_canvas4, 5, 5, 195, 95, 25, fill="#7EC4EF")
#round_rectangle(canvas4, 20, 20, 180, 80, 25, fill="#A0D1EC")
round_rectangle(t3_canvas4, 20, 20, 180, 80, 25, fill="#BEDFF1")
t3_canvas4.create_text(100,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="AutoCCS")

t3_canvas4_help = Pmw.Balloon(window)
t3_canvas4_help.bind(t3_canvas4, "AutoCCS\nInput: Feature files \tOutput: CCS results\nThis tool offers two methods of CCS calculations.\nThe \"standard\" method is comparable to DEIMoS.\nThe \"enhanced\" method takes into account the temperature and pressure of the instrument across runs.")
t3_canvas4_lbl = t3_canvas4_help.component("label")
t3_canvas4_lbl.config(background="black", foreground="white")


t3_l8=Label(tab3,text="Calculate CCS (Standard)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=3, column=7, columnspan=1)
t3_l9=Label(tab3,text="Calculate CCS (Enhanced)", font=("default, 14"),borderwidth=0, relief="solid", height=1, bg="grey").grid(row=4, column=7, columnspan=1)

AC_check_1_step = BooleanVar(False)
AC_button_1_step = Checkbutton(tab3, variable=AC_check_1_step, onvalue=True, offvalue=False, bg="grey")
AC_button_1_step.grid(row=3, column=8, sticky = "EW")

AC_check_2_step = BooleanVar(False)
AC_button_2_step = Checkbutton(tab3, variable=AC_check_2_step, onvalue=True, offvalue=False, bg="grey")
AC_button_2_step.grid(row=4, column=8, sticky = "EW")

#Generate Pipeline Button
t3_tag0 = round_rectangle(t3_canvas5, 0, 0, 115, 100, 25, fill="black")
t3_tag1 = round_rectangle(t3_canvas5, 5, 5, 110, 95, 25, fill="#72cc50")
t3_tag2 = t3_canvas5.create_text(57,50,fill="black",font=("Helvetica Neue", 15, "bold"), text="Generate\nNew\nPipeline", justify="center")
t3_tag3 = t3_canvas5.create_rectangle(0, 0, 0, 0, fill="grey", width=0)

t3_canvas5.tag_bind(t3_tag0, "<ButtonPress-1>", lambda event: Generate_pipeline_step(PP_check_1_step.get(),PP_check_2_step.get(),PW_check_1_step.get(),MM_check_1_step.get(),AC_check_1_step.get(),AC_check_2_step.get()))
t3_canvas5.tag_bind(t3_tag1, "<ButtonPress-1>", lambda event: Generate_pipeline_step(PP_check_1_step.get(),PP_check_2_step.get(),PW_check_1_step.get(),MM_check_1_step.get(),AC_check_1_step.get(),AC_check_2_step.get()))
t3_canvas5.tag_bind(t3_tag2, "<ButtonPress-1>", lambda event: Generate_pipeline_step(PP_check_1_step.get(),PP_check_2_step.get(),PW_check_1_step.get(),MM_check_1_step.get(),AC_check_1_step.get(),AC_check_2_step.get()))

t3_canvas5.tag_bind(t3_tag0, "<Enter>", lambda event: t3_canvas5.config(bg="yellow"))
t3_canvas5.tag_bind(t3_tag1, "<Enter>", lambda event: t3_canvas5.config(bg="yellow"))
t3_canvas5.tag_bind(t3_tag2, "<Enter>", lambda event: t3_canvas5.config(bg="yellow"))
t3_canvas5.tag_bind(t3_tag0, "<Leave>", lambda event: t3_canvas5.config(bg="grey"))
t3_canvas5.tag_bind(t3_tag1, "<Leave>", lambda event: t3_canvas5.config(bg="grey"))
t3_canvas5.tag_bind(t3_tag2, "<Leave>", lambda event: t3_canvas5.config(bg="grey"))




window.mainloop()





