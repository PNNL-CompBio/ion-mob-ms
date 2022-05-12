#!/usr/bin/env python3.9

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


#Initialize All Variables

# These variables are used across all three experiments and are overwritten with each pipeline generation.
necessary_arguments = []
necessary_arguments_colors = []
necessary_files = set()
selected_boxes = {}
global_file_dictionary = {"Raw Data": "", "mzML Data": "","Metadata": "", "Feature Data": "","config_data (Hidden)": "", "calibrant_curves": "","calibrant_data": "", "Target List": ""}
file_label = ""
parameter_label = ""
user_input_list = []
user_entry_list = []
user_entry_label_list = []
user_file_list = []
user_file_label_list = []

#Single Field - Initalize Variables

#Here we can modify the arguments required for each tool. The color hex code corresponds to the tool color.
#To modify: each checkbox requires arguments and a color. If no required arguments, nest an empty list, color within a list.
#example with placeholders.

# Example with placeholders: 
# tab1_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],                                  #pp_1_args
# [["PP_2_arg_1","PP_2_arg_2","PP_2_arg_3"],"#FEA95E"],                                                     #pp_2_args
# [["pw_arg_1","pw_arg_2"],"#f11b23"],                                                                      #pw_args
# [["ds_1_arg_1","ds_1_arg_2","ds_1_arg_3"],"#FFE54C"],                                                     #ds_1_args
# [["ds_2_arg_1","ds_2_arg_2","ds_2_arg_3"],"#FFE54C"],                                                     #ds_2_args
# [["ac_1_arg_1","ac_1_arg_2","ac_1_arg_3"],"#7EC4EF"],                                                     #ac_1_args
# [["ac_2_arg_1","ac_2_arg_2","ac_2_arg_3"],"#7EC4EF"]]                                                     #ac_2_args

#Unique Parameters
tab1_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],    #pp_1_args
[[],"#FEA95E"],                                                             #pp_2_args
[[],"#f11b23"],                                                             #pw_args
[[],"#FFE54C"],                                                             #ds_1_args
[[],"#FFE54C"],                                                             #ds_2_args
[[],"#7EC4EF"],                                                             #ac_1_args
[[],"#7EC4EF"]]                                                             #ac_2_args

#Required files
tab1_files_list = [["Raw Data"],                                                           #pp_1_args
["Raw Data"],                                                                              #pp_2_args
["Raw Data"],                                                                              #pw_args
["mzML Data", "Metadata"],                                                                   #ds_1_args
["Feature Data", "Calibrant Data"],                                                         #ds_2_args
["Feature Data","Metadata","Target List", "Calibrant Data"],       #ac_1_args
["Feature Data","Metadata","Target List", "Calibrant Data"]]       #ac_2_args


#SLIM - Initalize Variables
#Unique Parameters
tab2_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],        #pp_1_args
[[],"#FEA95E"],                                                                 #pp_2_args
[[],"#f11b23"],                                                                 #pw_args
[[],"#FFE54C"],                                                                 #ds_1_args
[[],"#FFE54C"],                                                                 #ds_2_args
[[],"#7EC4EF"],                                                                 #ac_1_args
[[],"#7EC4EF"]]                                                                 #ac_2_args

#Required files
tab2_files_list = [["Raw Data"],                                                             #pp_1_args
["Raw Data"],                                                                                #pp_2_args
["Raw Data"],                                                                                #pw_args
["mzML Data", "Metadata"],                                                                    #ds_1_args
["Feature Data", "Calibrant Data"],                                                           #ds_2_args
["Feature Data","Metadata","Target List", "Calibrant Data"],         #ac_1_args
["Feature Data","Metadata","Target List", "Calibrant Data"]]         #ac_2_args

#Stepped Field - Initalize Variables
#Unique Parameters
tab3_args_list = [[["driftkernel","lckernel","minintensity"],"#FEA95E"],        #pp_1_args
[[],"#FEA95E"],                                                                 #pp_2_args
[[],"#f11b23"],                                                                 #pw_args
[[],"#FFE54C"],                                                                 #mm_1_args                                                            
[[],"#7EC4EF"],                                                                 #ac_1_args
[[],"#7EC4EF"]]                                                                 #ac_2_args

#Required files
tab3_files_list = [["Raw Data"],                                                #pp_1_args
["Raw Data"],                                                                   #pp_2_args
["Raw Data"],                                                                   #pw_args
["mzML Data", "Metadata"],                                                      #mm_1_args
["Feature Data","Target List"],                                                 #ac_1_args
["Feature Data","Target List"]]                                                 #ac_2_args




#Button creation class - this is required to create buttons dynamically
class My_Button(tk.Button):
    def __init__(self, master, txt, r, c,colspan, value, col,col2, window):
        self.a_button = tk.Button(master, text = txt, width=7, height = 2, command = lambda: open_file(value,self.a_button,window), fg=col,bg=col2)
        self.a_button.grid(row = r, column = c, columnspan = colspan, sticky = "w")
        self.val = value
    def doom(self):
        self.a_button.destroy()


#Creates rounded rectangular shapes. Required for tkinter canvas. 
def round_rectangle(obj, x1, y1, x2, y2, r, **kwargs):    
    points = (x1+r, y1, x1+r, y1, x2-r, y1, x2-r, y1, x2, y1, x2, y1+r, x2, y1+r, x2, y2-r, x2, y2-r, x2, y2, x2-r, y2, x2-r, y2, x1+r, y2, x1+r, y2, x1, y2, x1, y2-r, x1, y2-r, x1, y1+r, x1, y1+r, x1, y1)
    return obj.create_polygon(points, **kwargs, smooth=True)


#Pipeline Generation
#This generates the pipeline (arguments, file uploads, labels, run button) for the single field experiment.
def Generate_pipeline(t_num,tab,window, hf,wf,smol,*args):
    global user_entry_list, user_input_list, user_entry_label_list, user_file_list, user_file_label_list, selected_boxes, \
        parameter_label, file_label, Run_button, necessary_files, necessary_arguments, necessary_arguments_colors
    if t_num == 0:
        arg_by_exp = tab1_args_list
        file_by_exp = tab1_files_list
        the_keys = ["pp_1","pp_2","pw_1","ds_1","ds_2","ac_1","ac_2"]
    elif t_num == 1:
        arg_by_exp = tab2_args_list
        file_by_exp = tab2_files_list
        the_keys = ["pp_1","pp_2","pw_1","ds_1","ds_2","ac_1","ac_2"]
    elif t_num == 2:
        arg_by_exp = tab3_args_list
        file_by_exp = tab3_files_list
        the_keys = ["pp_1","pp_2","pw_1","mm_1","ac_1","ac_2"]

    the_values = args
    arguments = dict(zip(the_keys, the_values))
    the_tab = tab
    counter = 0

#Reset Pipeline Arguments and Lists
    reset_all_pipelines()

#Checkbox values for json file 
    for k,v in arguments.items():
        selected_boxes[k] = v


#Create Pipeline
    #Generate required arugments and required files lists
    for item in arguments.values():
        if item ==True:
            necessary_arguments.extend(arg_by_exp[counter][0])
            necessary_files.update(file_by_exp[counter])
            for item in range(0,len((arg_by_exp[counter][0]))):
                necessary_arguments_colors.append(arg_by_exp[counter][1])
        counter +=1
    if (arguments["pp_1"] == True or arguments["pp_2"] == True) and "Metadata" in necessary_files:
        necessary_files.remove("Metadata")
    if arguments["pw_1"] == True and "mzML Data" in necessary_files:
        necessary_files.remove("mzML Data")
    if t_num == 0 or t_num == 1:
        if (arguments["ds_1"] == True) and "Feature Data" in necessary_files:
            necessary_files.remove("Feature Data")
    elif t_num == 2:
        if (arguments["mm_1"] == True) and "Feature Data" in necessary_files:
            necessary_files.remove("Feature Data")

   #Create all Argument labels and Entry Boxes
    row_placer = 6
    column_placer = 1
    num_of_desired_rows = 5
    args_exist = False
    if len(necessary_arguments) >= 1:
        parameter_label=Label(tab,text="Enter Parameter Values", font=("Helvetica Neue", 16), height=2)
        parameter_label.grid(row=5, column=1, columnspan=7, sticky = "W")
        counter = 0
        args_exist = True
        for arg in necessary_arguments:
            user_entry_label_list.append(tk.Label(tab,text=arg, font=("Helvetica Neue",12), anchor="w", width = 20, fg =necessary_arguments_colors[counter]))
            user_entry_label_list[counter].grid(row=row_placer, column = column_placer,pady=(5,5),columnspan=2)
            column_placer += 1
            user_input_list.append(tk.StringVar())
            user_entry_list.append(ttk.Entry(tab, width=10, justify = "left", textvariable=user_input_list[counter]))
            user_entry_list[counter].grid(row=row_placer, column = column_placer, columnspan=2, sticky="W")
            column_placer -= 1
            row_placer += 1
            counter += 1
            if counter%6 == num_of_desired_rows:
                column_placer +=3
                row_placer = 6
                num_of_desired_rows -=1

    #Create all File upload labels and file upload buttons
    if len(necessary_files) >= 1:
        column_placer = 1
        run_row_placer=12
        run_col_placer=8
        if args_exist == False:
            row_placer = 6
        else:
            row_placer = 12
        if args_exist == True and smol == True:
            column_placer = 4
            row_placer = 6
        if smol == True:
            run_row_placer=6
            run_col_placer=8
            
        counter = 0
        file_label=Label(tab,text="Upload the Following File(s)", font=("Helvetica Neue", 16), height=2)
        file_label.grid(row=(row_placer-1), column=column_placer, columnspan=7, sticky = "W")
        browse_text =tk.StringVar()
        browse_text.set("Browse")
        for file in necessary_files:
            user_file_label_list.append(tk.Label(tab,text=file, anchor="w", font=("Helvetica Neue",12), width = 20, bg ="#1c1c1c"))
            user_file_label_list[counter].grid(row=row_placer, column = column_placer,columnspan=2, sticky = "w")
            column_placer += 1
            user_file_list.append(My_Button(tab, browse_text.get(), row_placer, column_placer, 3, file,'red', 'silver', window))
            column_placer -= 1
            row_placer += 1
            counter += 1
        Run_button = tk.Button(tab, text="Run\nExperiment", font=("default", 16), command=lambda:Run_Experiment(t_num,window), height=5, width=14, bg="silver", fg= "green")
        Run_button.grid(row=run_row_placer, column=run_col_placer, rowspan=4, columnspan=2)
    
    #this gets screen size
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    window_height = window.winfo_height()
    window_width = window.winfo_width()

    #Print the screen size
   
    print("Screen height: ", screen_height)
    print("Screen width: ", screen_width)
    print("\ntkinter height: ", window_height)
    print("tkinter width: ", window_width)

    return  



#Reset All Pipelines
#This clears all three pipelines everytime a pipeline is generated. This is implemented to allow for shared variables between pipelines. 

def reset_all_pipelines():
    #Single Field Pipeline

    global user_entry_label_list, user_input_list, user_file_list, selected_boxes, global_file_dictionary, \
            file_label, parameter_label, Run_button, necessary_files, necessary_arguments, necessary_arguments_colors, \
            user_entry_list, user_file_label_list

    for label in range(0,len(user_entry_list)):
        user_entry_list[label].destroy()
    for entry in range(0,len(user_entry_label_list)):
        user_entry_label_list[entry].destroy()
    for lab in range(0,len(user_file_label_list)):
        user_file_label_list[lab].destroy()
    for button in range(0,len(user_file_list)):
        user_file_list[button].doom()
    global_file_dictionary = {"Raw Data": "", "mzML Data": "","Metadata": "", "Feature Data": "","config_data (Hidden)": "", "calibrant_curves": "","calibrant_data": "", "Target List": ""}
    user_input_list = []
    user_entry_label_list = []
    user_entry_list = []
    user_file_list = []
    user_file_label_list = []
    selected_boxes = {}
    necessary_arguments = []
    necessary_arguments_colors = []
    necessary_files = set()
    try:
        Run_button.destroy()
        file_label.destroy()
        parameter_label.destroy()
    except:
        pass



# Open File function - linked to file upload buttons
#this is called in the button class
def open_file(file_variable,button,window):
    """ 
    Raw data - Choose a folder

    All others - Choose a file
    """
    global global_file_dictionary
    if file_variable == "Raw Data":
        file = tkinter.filedialog.askdirectory(parent=window,title='Select a file directory')
        if file != "":
            global_file_dictionary["Raw Data"]=os.path.abspath(file)
            button.configure(bg="silver", fg = "green")
    else:
        file = askopenfile(parent=window, mode = 'rb',title = "Select a file")
        if file_variable == "mzML Data":
            global_file_dictionary["mzML Data"] = os.path.abspath(file.name)
            button.configure(bg="silver", fg = "green")

        elif file_variable == "Metadata":
            global_file_dictionary["Metadata"]= os.path.abspath(file.name)
            button.configure(bg="silver", fg = "green")

        elif file_variable == "Feature Data":
            global_file_dictionary["Feature Data"]= os.path.abspath(file.name)
            button.configure(bg="silver", fg = "green")

        # elif file_variable == "config_data (Hidden)":
        #     global_file_dictionary["config_data (Hidden)"] = os.path.abspath(file.name)
        #     button.configure(bg="silver", fg = "green")

        elif file_variable == "calibrant_curves":
            global_file_dictionary["calibrant_curves"] = os.path.abspath(file.name)
            button.configure(bg="silver", fg = "green")

        elif file_variable == "Calibrant Data":
            global_file_dictionary["Calibrant Data"] = os.path.abspath(file.name)
            button.configure(bg="silver", fg = "green") 

        elif file_variable == "Target List":
            global_file_dictionary["Target List"] = os.path.abspath(file.name)
            button.configure(bg="silver", fg = "green")
    return 


#Called when the Run experiment button is pressed
def Run_Experiment(t_num,window):
    global win
    win = window
    #single Field
    try:
        error_catch_arguments_single = [var.get() for var in user_input_list if var.get() !='']
        if len(error_catch_arguments_single) != len(user_input_list):
            fail_the_test
    except:
        msg.showerror("Error","Please enter all parameter values and upload all files before running experiment!", icon = "warning")
    else:
        L = [var.get() for var in user_input_list]
        L = [t_num] + L
        write_to_json(*L)
        thread1 = threading.Thread(target=run_workflow)
        thread1.start()

# This will write all relevent information to a json file!
#this is called in run_experiment
def write_to_json(*args):
    global necessary_arguments, necessary_files
    counter = -1
    json_args = {}
    json_files = {}
    for arg in args:
        if counter == -1:
            json_exp =  {"Experiment": arg}
        else: 
            json_args[necessary_arguments[counter]] = arg
        counter += 1

    for file in user_file_list:
        json_files[file.val] = global_file_dictionary[file.val]
        json_selected = selected_boxes

    json_export = [json_exp,json_selected,json_args,json_files]
    json_object = json.dumps(json_export, indent = 4)

    with open("sample.json", "w") as outfile:
        outfile.write(json_object)
    return 


#Run nextflow! 
#if this section is not working, check if main.nf is in current directory!
#to do: find current directory of nextflow file and run.
def run_workflow():
    confirmation_step = msg.askquestion("Run Experiment", "Please confirm all arguments before running experiment. There will be no option to cancel run.")
    if confirmation_step == "yes":
        global Run_button, win
        Run_button.config(text="In progress")
        print("pipeline in progress. this is printed in function \"run_workflow\"")
        Run_button.config(text="Run Complete. \nView Results.", command=lambda:open_popup(win))


#Results Popup window
#called on run button press after nextflow thread is complete
def open_popup(window):
    top= Toplevel(window)
    top.geometry("1000x500")
    top.title("Tool Documentation")
    results = open("./sample.json", "r")
    text_box = tk.Text(top, height = 20, width = 60, padx=15, pady=15)
    for line in results:
        text_box.insert(tkinter.END, line)
    text_box.config(state=DISABLED)
    text_box.grid(row = 1, column = 1)

#Documentation Single field / SLIM
#called on "show documentation" button press
def show_help_single(window):
    front= Toplevel(window)
    front.geometry("900x500")
    front.title("Tool Documentation Single Field / SLIM")
    results = open("./documentation_single.txt", "r")
    help_box_single = scrolledtext.ScrolledText(front, height = 30, width = 90, padx=15, pady=15, bg = "grey")
    help_box_single.configure(font=("default", 14))
    for line in results:
        help_box_single.insert(tkinter.END, line)
    help_box_single.config(state=DISABLED)
    help_box_single.grid(row = 1, column = 1)

#Documentation Stepped field
#called on "show documentation" button press
def show_help_step(window):
    front= Toplevel(window)
    front.geometry("900x500")
    front.title("Tool Documentation Stepped Field")
    results = open("./documentation_step.txt", "r")
    help_box_step = scrolledtext.ScrolledText(front, height = 30, width = 90, padx=15, pady=15, bg = "grey")
    help_box_step.configure(font=("default", 14))
    for line in results:
        help_box_step.insert(tkinter.END, line)
    help_box_step.config(state=DISABLED)
    help_box_step.grid(row = 1, column = 1)
