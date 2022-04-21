#!/usr/bin/env python3.9

import tkinter as tk
import tkinter.filedialog
from tkinter.ttk import *
from tkinter import ttk
from tkinter import *
from tkinter.filedialog import askopenfile
import os
from turtle import bgcolor, st

"""
Front End for ION Mobility Desktop Application


Users can:

Select Experimental Type (Single Field, Stepped Field, SLIM)
Select experimental parameters
Upload experiment files
Run Experiment
Download Results


Naming conventions:
l1, l2, l3, etc = Label 1, Label 2, Label 3
t1, t2, t3, etc = Tab 1, Tab 2, Tab 3
p1, p2, p3, etc = Parameter 1, Parameter 2, Parameter 3
f1, f2, f3, etc = File 1, File 2, File 3
"""




# Functions
def open_file(file_variable,button):
    """ 
    Raw data - Choose a folder
    All others - Choose a file
    """
    if file_variable == "raw_data_file_string":
        file = tkinter.filedialog.askdirectory(parent=window,initialdir="/",title='Select a file directory')
        global raw_data_file
        raw_data_file = os.path.abspath(file)
        button.configure(background="green", fg = "green")
        return raw_data_file
    else:
        file = askopenfile(parent=window, mode = 'rb',title = "Select a file")
        if file_variable == "calibrant_list_file_string":
            global calibrant_list_file
            calibrant_list_file = os.path.abspath(file.name)
            button.configure(background="green", fg = "green")
            return calibrant_list_file

        elif file_variable == "calibrant_curve_file_string":
            global calibrant_curve_file
            calibrant_curve_file = os.path.abspath(file.name)
            button.configure(background="green", fg = "green")
            return calibrant_curve_file

        elif file_variable == "configuration_file_string":
            global configuration_file
            configuration_file = os.path.abspath(file.name)
            button.configure(background="green", fg = "green")
            return configuration_file

        elif file_variable == "target_list_file_string":
            global target_list_file
            target_list_file = os.path.abspath(file.name)
            button.configure(background="green", fg = "green")
            return target_list_file




def gather_everything_together(p1,p2,p3,p4,p5,p6,p7,p8,f1,f2,f3,f4):
    everything_file = open("everything.csv", "w")
    everything_file.write(str(tabControl.index(tabControl.select())))
    everything_file.write("\n")

    for item in vars().values():
        if item != everything_file and item != "empty":
            everything_file.write(str(item))
            everything_file.write("\n")
    return 


def Run_Experiment():
    #To do: 
    #Add correct parameters and files required for each
    #Add check_all_values function here too

    #Single Field
    if tabControl.index(tabControl.select()) == 0:
        gather_everything_together(t1_p1_input.get(),t1_p2_input.get(),t1_p3_input.get(),t1_p4_input.get(),t1_p5_input.get(),t1_p6_input.get(),t1_p7_input.get(),"empty",raw_data_file,calibrant_list_file,calibrant_curve_file,configuration_file)
        os.system("nextflow run hello")

    #Stepped Field
    if tabControl.index(tabControl.select()) == 1:
        gather_everything_together(t2_p1_input.get(),t2_p2_input.get(),t2_p3_input.get(),t2_p4_input.get(),t2_p5_input.get(),t2_p6_input.get(),raw_data_file,calibrant_list_file,target_list_file,"empty", "empty", "empty")
        os.system("nextflow run hello")
        
    #SLIM
    if tabControl.index(tabControl.select()) == 2:
        gather_everything_together(t3_p1_input.get(),t3_p2_input.get(),t3_p3_input.get(),t3_p4_input.get(),t3_p5_input.get(),t3_p6_input.get(),t3_p7_input.get(),t3_p8_input.get(),raw_data_file,calibrant_list_file,calibrant_curve_file,configuration_file)
        os.system("nextflow run hello")


# Initialize application
window = tk.Tk()
window.title("PNNL Ion Mobility Application",)
window.config(bg='#0C74BA')

# Global Labels
l1=Label(window,text="Experiment", font=("default, 20"),borderwidth=0, relief="solid", height=2).grid(row=1, column=7, pady=(5,0), sticky="EW")

l2=Label(window,text="  PNNL Ion Mobility Application  ", font=("default, 30"),borderwidth=1, relief="solid", width = 75).grid(row=0, columnspan=20, pady=(5,10), ipady=(10), sticky="EW")

l3=Label(window, borderwidth=1, relief="solid", text="    Instructions: \n 1. Select experiment tab \n 2. Define parameters \n 3. Upload requested files \n 4. Run experiment \n 5. Wait X minutes \n 6. Results will be in 'X_file'",  anchor = "w", justify="left", font=("default",22)).grid(row=2, column=1, ipady=5, sticky = "EW")

l4=Label(window, borderwidth=1, relief="solid", text="    Github: \n https://github.com/PNNL-Comp-Mass-Spec/AutoCCS \n https://github.com/PNNL-CompBio/ion-mob-ms", justify= "left", font=("default",18)).grid(row=4, column=1, ipady=5, sticky = "EW")

l5=Label(window, borderwidth=1, relief="solid", text="    Licenses: \n PNNL PreProcessor License Link \n ProteoWizard License Link \n DEIMoS License Link \n AutoCCS License Link", anchor = "w", justify="left", font=("default",18)).grid(row=5, column=1, sticky="EW")

#Seperator under Experiment
sep = tk.Frame(window, bg="black", height=2, bd=0).grid(row=1, column=7, sticky="EWS")





# Initialize Tabs
tabControl = ttk.Notebook(window)
tabControl.grid(row=2, rowspan=5,column=7)

#   Spacer for format
spacer_g1=Label(window,text="\t",bg='#0C74BA').grid(row=2, column=4)




########### ########### ########### ########### 
    ########### Single Field Tab ########### 
########### ########### ########### ########### 

tab1 = ttk.Frame(tabControl)
tabControl.add(tab1, text = "Single Field")
tab1.columnconfigure((1,2,3,4,5,6,7), minsize=75)
tab1.rowconfigure((1,2,3,4,5,6,7,8,9,10), minsize=40)

#   Parameters
#initialize values
t1_p1_input = tk.IntVar(value = 'Enter a number')
t1_p2_input = tk.IntVar(value = 'Enter a number')
t1_p3_input = tk.IntVar(value = 'Enter a number')
t1_p4_input = tk.StringVar()
t1_p5_input = tk.StringVar()
t1_p6_input = tk.StringVar()
t1_p7_input = tk.StringVar()


#Display and create entry boxes
tab1_l1=Label(tab1,text="PNNL Preprocessor Parameters", font=("default bold", 14), bg ="#E5E4E2", anchor="w", width = 25).grid(row=2, column=1)

tab1_l2=Label(tab1,text="driftKernal", anchor="w", width = 20, bg ="#E5E4E2").grid(row=3, column=1)
t1_p1 = ttk.Entry(tab1, textvariable=t1_p1_input).grid(row=3, column=2)

tab1_l3=Label(tab1,text="lcKernel", anchor="w", width = 20, bg ="#E5E4E2").grid(row=4, column=1)
t1_p2 = ttk.Entry(tab1, textvariable=t1_p2_input).grid(row=4, column=2)

tab1_l4=Label(tab1,text="minIntensity", anchor="w", width = 20, bg ="#E5E4E2").grid(row=5, column=1)
t1_p3 = ttk.Entry(tab1, textvariable=t1_p3_input).grid(row=5, column=2)


# No dynamic ProteoWizard Parameters
#No dynamic MZMine parameters 

tab1_l9=Label(tab1,text="AutoCCS Parameters", font=("default bold", 14), bg ="#E5E4E2", anchor="w", width = 25).grid(row=6, column=1)

tab1_l5=Label(tab1,text="Ionization Colname", anchor="w", width = 20, bg ="#E5E4E2").grid(row=7, column=1)
t1_p4 = ttk.Entry(tab1, textvariable=t1_p4_input).grid(row=7, column=2)

tab1_l6=Label(tab1,text="Tunemix Sample Type", anchor="w", width = 20, bg ="#E5E4E2").grid(row=8, column=1)
t1_p5 = ttk.Entry(tab1, textvariable=t1_p5_input).grid(row=8, column=2)

tab1_l7=Label(tab1,text="Degree", anchor="w", width = 20, bg ="#E5E4E2").grid(row=9, column=1)
t1_p6 = ttk.Entry(tab1, textvariable=t1_p6_input).grid(row=9, column=2)

tab1_l8=Label(tab1,text="Skip Samples", anchor="w", width = 20, bg ="#E5E4E2").grid(row=10, column=1)
t1_p7 = ttk.Entry(tab1, textvariable=t1_p7_input).grid(row=10, column=2)

#L9 taken


#    File Upload

#Initialize Variables and Label
browse_text =tk.StringVar()
browse_text.set("Browse")

tab1_l10=Label(tab1,text="File Upload", font=("default bold", 14), bg ="#E5E4E2").grid(row=2, column=6)

# Display and activate buttons
tab1_l11=Label(tab1,text="Raw Data", bg ="#E5E4E2").grid(row=3, column=5)
Raw_data_button_Single = tk.Button(tab1, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("raw_data_file_string",Raw_data_button_Single), height=2, width=4)
Raw_data_button_Single.grid(row=3, column=6)

tab1_l12=Label(tab1,text="Calibrant List", bg ="#E5E4E2").grid(row=4, column=5)
Calibrant_list_button_Single = tk.Button(tab1,textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("calibrant_list_file_string",Calibrant_list_button_Single), height=2, width=4)
Calibrant_list_button_Single.grid(row=4, column=6)

tab1_l12=Label(tab1,text="Calibrant Curves", bg ="#E5E4E2").grid(row=5, column=5)
Calibrant_curves_button_Single = tk.Button(tab1, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("calibrant_curve_file_string",Calibrant_curves_button_Single), height=2, width=4)
Calibrant_curves_button_Single.grid(row=5, column=6)

tab1_l12=Label(tab1,text="Configuration File", bg ="#E5E4E2").grid(row=6, column=5)
Configuration_button_Single = tk.Button(tab1, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("configuration_file_string",Configuration_button_Single), height=2, width=4)
Configuration_button_Single.grid(row=6, column=6)

#    Run Button 
# This calls the Run_Experiment function 
# This checks that all values are expected, writes them to a csv, and then initalizes nextflow.
Run_button = tk.Button(tab1, text="Run", command=lambda:Run_Experiment(), height=4, width=8).grid(row=10, column=6)




########### ########### ########### ########### 
    ########### Stepped Field Tab ########### 
########### ########### ########### ########### 

tab2 = ttk.Frame(tabControl)
tabControl.add(tab2, text = "Stepped Field")

#   Parameters
#initialize values
t2_p1_input = tk.StringVar()
t2_p2_input = tk.StringVar()
t2_p3_input = tk.StringVar()
t2_p4_input = tk.StringVar()
t2_p5_input = tk.StringVar()
t2_p6_input = tk.StringVar()
t2_p7_input = tk.StringVar()
t2_p8_input = tk.StringVar()

#Display and create entry boxes
tab2_l1=Label(tab2,text="Parameter", font=("default bold", 14), bg ="#E5E4E2").grid(row=2, column=1)

tab2_l2=Label(tab2,text="R² Threshold").grid(row=3, column=1)
t2_p1 = ttk.Entry(tab2, textvariable=t2_p1_input).grid(row=3, column=2)

tab2_l3=Label(tab2,text="Isotopes Threshold").grid(row=4, column=1)
t2_p2 = ttk.Entry(tab2, textvariable=t2_p2_input).grid(row=4, column=2)

tab2_l4=Label(tab2,text="Intensity Threshold").grid(row=5, column=1)
t2_p3 = ttk.Entry(tab2, textvariable=t2_p3_input).grid(row=5, column=2)

tab2_l5=Label(tab2,text="Max Peak Selection").grid(row=6, column=1)
t2_p4 = ttk.Entry(tab2, textvariable=t2_p4_input).grid(row=6, column=2)

tab2_l6=Label(tab2,text="Feature File Format").grid(row=7, column=1)
t2_p5 = ttk.Entry(tab2, textvariable=t2_p5_input).grid(row=7, column=2)

tab2_l7=Label(tab2,text="Instrument").grid(row=8, column=1)
t2_p6 = ttk.Entry(tab2, textvariable=t2_p6_input).grid(row=8, column=2)

# tab2_l8=Label(tab2,text="Mode")
# tab2_l8.grid(row=9, column=1)
# t2_p7 = ttk.Entry(tab2, textvariable=t2_p7_input)
# t2_p7.grid(row=9, column=2)

# tab2_l9=Label(tab2,text="Skip Samples")
# tab2_l9.grid(row=10, column=1)
# t2_p8 = ttk.Entry(tab2, textvariable=t2_p8_input)
# t2_p8.grid(row=10, column=2)




#    File Upload

#Initialize Variables and Label
browse_text =tk.StringVar()
browse_text.set("Browse")

tab2_l10=Label(tab2,text="File Upload", font=("default bold", 14), bg ="#E5E4E2").grid(row=2, column=6)

# Display and activate buttons
tab2_l11=Label(tab2,text="Raw Data").grid(row=3, column=5)
Raw_data_button_Step = tk.Button(tab2, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("raw_data_file_string", Raw_data_button_Step), height=2, width=4)
Raw_data_button_Step .grid(row=3, column=6)

tab2_l12=Label(tab2,text="Configuration File").grid(row=4, column=5)
Calibrant_list_button_Step = tk.Button(tab2,textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("calibrant_list_file_string", Calibrant_list_button_Step), height=2, width=4)
Calibrant_list_button_Step.grid(row=4, column=6)

tab2_l12=Label(tab2,text="Target List File").grid(row=5, column=5)
Calibrant_curves_button_Step = tk.Button(tab2, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("target_list_file_string", Calibrant_curves_button_Step), height=2, width=4)
Calibrant_curves_button_Step.grid(row=5, column=6)



#    Run Button 
# This calls the Run_Experiment function 
# This checks that all values are expected, writes them to a csv, and then initalizes nextflow.
Run_button = tk.Button(tab2, text="Run", command=lambda:Run_Experiment(), height=4, width=8).grid(row=10, column=6)




########### ########### ########### ########### 
    ########### SLIM Tab ########### 
########### ########### ########### ########### 
tab3 = ttk.Frame(tabControl)
tabControl.add(tab3, text = "SLIM")


#   Parameters
#initialize values
t3_p1_input = tk.IntVar()
t3_p2_input = tk.StringVar()
t3_p3_input = tk.StringVar()
t3_p4_input = tk.StringVar()
t3_p5_input = tk.StringVar()
t3_p6_input = tk.IntVar()
t3_p7_input = tk.StringVar()
t3_p8_input = tk.StringVar()

#Display and create entry boxes
tab3_l1=Label(tab3,text="Parameter", font=("default bold", 14), bg ="#E5E4E2").grid(row=2, column=1)

tab3_l2=Label(tab3,text="Mass to Charge Tolerance").grid(row=3, column=1)
t3_p1 = ttk.Entry(tab3, textvariable=t3_p1_input).grid(row=3, column=2)

tab3_l3=Label(tab3,text="Calibration Method").grid(row=4, column=1)
t3_p2 = ttk.Entry(tab3, textvariable=t3_p2_input).grid(row=4, column=2)

tab3_l4=Label(tab3,text="Column Name of Sampletype").grid(row=5, column=1)
t3_p3 = ttk.Entry(tab3, textvariable=t3_p3_input).grid(row=5, column=2)

tab3_l5=Label(tab3,text="Ionization Colname").grid(row=6, column=1)
t3_p4 = ttk.Entry(tab3, textvariable=t3_p4_input).grid(row=6, column=2)

tab3_l6=Label(tab3,text="Tunemix Sample Type").grid(row=7, column=1)
t3_p5 = ttk.Entry(tab3, textvariable=t3_p5_input).grid(row=7, column=2)

tab3_l7=Label(tab3,text="Degree").grid(row=8, column=1)
t3_p6 = ttk.Entry(tab3, textvariable=t3_p6_input).grid(row=8, column=2)

tab3_l8=Label(tab3,text="Mode").grid(row=9, column=1)
t3_p7 = ttk.Entry(tab3, textvariable=t3_p7_input).grid(row=9, column=2)

tab3_l9=Label(tab3,text="Skip Samples").grid(row=10, column=1)
t3_p8 = ttk.Entry(tab3, textvariable=t3_p8_input).grid(row=10, column=2)



#   Spacer for format
tab3_l10=Label(tab3,text="                ")
tab3_l10.grid(row=2, column=4)


#    File Upload

#Initialize Variables and Label
browse_text =tk.StringVar()
browse_text.set("Browse")

tab3_l10=Label(tab3,text="File Upload", font=("default bold", 14), bg ="#E5E4E2").grid(row=2, column=6)

# Display and activate buttons
tab3_l11=Label(tab3,text="Raw Data").grid(row=3, column=5)
Raw_data_button_SLIM = tk.Button(tab3, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("raw_data_file_string",Raw_data_button_SLIM), height=2, width=4)
Raw_data_button_SLIM.grid(row=3, column=6)

tab3_l12=Label(tab3,text="Calibrant List").grid(row=4, column=5)
Calibrant_list_button_SLIM = tk.Button(tab3,textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("calibrant_list_file_string",Calibrant_list_button_SLIM), height=2, width=4)
Calibrant_list_button_SLIM.grid(row=4, column=6)

tab3_l12=Label(tab3,text="Calibrant Curves").grid(row=5, column=5)
Calibrant_curves_button_SLIM = tk.Button(tab3, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("calibrant_curve_file_string",Calibrant_curves_button_SLIM), height=2, width=4)
Calibrant_curves_button_SLIM .grid(row=5, column=6)

tab3_l12=Label(tab3,text="Configuration File").grid(row=6, column=5)
Configuration_button_SLIM = tk.Button(tab3, textvariable=browse_text, bg ='green', fg = 'red', command=lambda:open_file("configuration_file_string",Configuration_button_SLIM), height=2, width=4)
Configuration_button_SLIM.grid(row=6, column=6)


#    Run Button 
# This calls the Run_Experiment function 
# This checks that all values are expected, writes them to a csv, and then initalizes nextflow.
Run_button = tk.Button(tab3, text="Run", command=lambda:Run_Experiment(), height=4, width=8).grid(row=10, column=6)








# canvas = tk.Canvas(window, width = 600, height = 6000)
# canvas.grid(columnspan = 10 ,rowspan = 10)



window.mainloop()










#


# Software    Parameters  InputFiles  Output

# E:/CCS_Calculations/a_Software/I_PNNL-PreProcessor/PNNL-PreProcessor_v2020.07.24/PNNL-PreProcessor.exe  -smooth -driftKernel 1 -lcKernel 0 -minIntensity 20 -split  DMS_dataset_Dorrestein_KB_Edit_SteppedField.txt 
# II_PreprocessedI_Extract-Agilent-d-file-metadata.R     DMS_dataset_Dorrestein_KB_Edit_SteppedField.txt RawFiles_Metadata.csv

# C:/Program Files/ProteoWizard/ProteoWizard 3.0.19228.a2fc6eda4/msconvert.exe    --zlib --gzip -e .mzML.gz   II_Preprocessed 
# III_mzMLII_Parse-DT-as-RT-mzML.R  \\pnl\projects\PNACIC\Experimental-CCS\Dorrestein_DT_2021-01_SteppedField\III_mzML  III_mzML


# C:\Users\bilb280\Desktop\MZmine-2.41.2\startMZmine_Windows.bat  MZmine_FeatureFinder-batch.xml  III_mzML    IV_Features_csv


# ------
# PNNL-PreProcessor.exe   -smooth -driftKernel 1 -lcKernel 0 -minIntensity 20 -split  DMS_dataset_Dorrestein_KB_Edit_SteppedField.txt II_Preprocessed
# I_Extract-Agilent-d-file-metadata.R     DMS_dataset_Dorrestein_KB_Edit_SteppedField.txt RawFiles_Metadata.csv