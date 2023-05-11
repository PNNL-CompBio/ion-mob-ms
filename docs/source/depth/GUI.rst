Graphical User Interface
=====================

The Ion Mobility Dashboard was originally developed as a GUI and this guide was developed to hopefully answer all your questions related to this dashboard.



Run Overview
-------------

1) Workflow choice will be dictated by which type of experiment you are
   running. The option to run any individual tool is also available.
2) Depending on which workflow you’d like to run,a set of files and
   folders must be prepared ahead of time.
3) Enter parameter values and use a unique experiment name. Avoid spaces
   or any special characters in this name.
4) Double check parameter inputs, files, then run the experiment.
5) If AutoCCS was performed, you will be able to view a preview of the
   results. If this does not appear, the experiment likely failed.
6) Save results to folder. Do not use a duplicate folder name. Once
   results are saved, they will be removed from the application
   workspace.

First Step - Run PNNL PreProcessor
------------------------------

| At this point in time, PNNL PreProcessor has not been integrated into
  the application. This tool has two important aspects in the workflow:
  1) it filters and smooths data for quality control purposes, 2) it
  splits multi-field (.d) data into separate (.d) folders.
| This spliting function adds a suffix to (.d) folders depending on the
  ms level as follows: ms1 would be in “filename_1.d”, ms2 would be in
  “filename_2.d”, etc.
| This allows for both stepped-field and single-field to be processed in
  this application.
| For singlefield, metadata must be extracted **after** splitting raw files. 
| For steppedfield, metadata must be extracted **before** splitting raw files. 

Select your Workflow
---------------------

There are three types of workflows to run. Each mode has separate needs
for input files, but runs a combination of the modules depicted below.

**DTIMS Single field**

Drift tube ion mobility mass spectrometry requires knowledge of
experiments and a table of calibration ions. 

*A note on Proteowizard and Nomenclature:* For the single tool option, this application
will convert all (.d) files to mzML. For the Single-Field workflow, this
application will filter out all files suspected to come from multi-field
data - this will be determined by the PNNL PreProcessor naming suffix.
If a file suffix contains any number greater than
(filename)\ **1**\ *.d, it will be removed. For example,
(filename)*\ **2**.d would be removed from this workflow.

**DTIMS Stepped field**

Drift tube ion mobility mass spectrometry that requires specific known
targets and their masses.

*A Note on AutoCCS:* For the stepped-field experiment, autoCCS does
not generate a (hidden) metadata file. Instead, it extracts the
ionization from the file name (POS or NEG). As such, any Feature files
and Ims_Metadata files run through stepped-field AutoCCS must include
POS or NEG in their names.

| **SLIM**
| Data from instrument performing Structures for Lossless Ion
  Manipulation.

Single Tool Option
------------------

This option is selected to run tools individually.

Select which tool you would like to run. Grey boxes are unavailable,
white boxes are available, and the orange box indicates which is
selected.

If AutoCCS is selected, choose single field, stepped field, or SLIM
depending on your experiment.

   
Upload your files
--------------------

Prior to uploading files, please sort each file type into their own
folder, then select the folder by clicking “Browse”. For example, all
Raw data files should be placed in a single folder without any other
files. This includes data types such as Agilent (.d) which are folders
themselves - ie: select the encompassing folder/directory which holds
one or more raw data types, not the data files themselves.

Individual File uploads do not require folders and may be selected
directly. These include: Calibrant File, Target List File, and Metadata
File.

Once files are uploaded, select the Run tab.

Run Experiment
-------------------

**Prior** to selecting “Run Experiment”, Docker Desktop must be open.

Please confirm all variables and path locations before running
experiment.

When running experiment, do not exit the application or Docker. Doing so
may result in temporary files (such as .tar files in data folders) not
being deleted. If exited early, please ensure no temporary files exist
in experimental folders before running again.

Viewing and Saving Results
------------------------------

After an experiment is completed, a “Save Results” button should appear.
Select this button to find a folder to save results at.

If CCS Values were generated, a summary graph or PDF will be available
to preview depending on the experiment type.

Running Additional Experiments
---------------------------------

To clear all parameters and results, select the “Clear Experiment”
button and confirm. Save results before clearing or they will be lost.

