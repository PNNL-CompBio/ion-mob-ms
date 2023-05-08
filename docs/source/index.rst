Ion Mobility Mass Spec Dashboard
================================

The Ion Mobility Mass Spec Dashboard is designed to allow scientists to
generate results from raw Ion Mobility-Mass Spectrometry data without
requiring assistance from an engineer or bioinformatician. This
dashboard links four sequential command line tools into a single
user-friendly application which communicates with Docker Desktop to
dynamically spin up docker containers and manage the filesystem. Each
tool has been dockerized and together they perform the following steps:
quality control data processing, file type conversion (from proprietary
to an open-source format), detection of unique features, and calculation
of collision-cross section (CCS).

IMS-MS Background
=================

Mass Spectrometry (MS) is used to identify and differentiate unknown
molecules by comparing intensities and mass-to-charge-ratio (m/z). This
is important in clinical research and drug development, however, this
method stuggles with identifying small molecules, isomers, and
enantiomers. To increase the accuracy of molecular identification, MS
can be paired with Ion Mobility Spectrometry (IMS). IMS generates an
additional descriptive variable called the “collision cross section”, or
CCS, which is used to further differentiate between unknown molecules.

| This application analyzes the following three methods of ion mobility
  spectrometry:
| 1) Single Field Drift Tube Ion Mobility Spectrometry (single field
  DTIMS)
| 2) Stepped Field Drift Tube Ion Mobility Spectrometry (stepped field
  DTIMS)
| 3) Structures for Lossless Ion Manipulations (SLIM)

**Drift Tube Ion Mobility Spectrometry**

DTIMS seperates ions by collision cross section. This works by
accelerating ions through a straight tube filled with an inert buffer
gas, as the ions pass through the tube, they bump into buffer gas
molecules and are slowed down. Drift (retention) time is used as a
predictor of CCS. Ions with a greater CCS collide with and are slowed
down more by buffer molecules, the inverse is true with small molecules.
Single field DTIMS uses a single electrical field to accelerate ions
through the tube. This differs from stepped field DTIMS which uses an
alternating electrical curent to propel ions though the tube. An
increase in the length of drift tube increases resolution and both
methods of DTIMS are limited by instrument space.

**Structures for Lossless Ion Manipulations**

SLIM uses the same principal as single field DTIMS without the
limitation of drift tube length. This technology allows the ions to be
pushed around corners without colliding with path walls; this allows for
significantly longer paths resulting in much greater resolution of ion
CCS values.

How to install
==============

Two applications are required to run workflows: Docker Desktop, and
Ion_Mob_PC.exe (or UI_V2).

| **Mac Installation**:
| 1. Download
  `Ion_Mob_MacOS.zip <https://zenodo.org/record/6941767#.YuRxcuzMIXA>`__.
  Ensure this is version 1.1, or “DOI 10.5281/zenodo.6941767”. 2.
  Download `Docker Desktop for
  Mac <https://docs.docker.com/desktop/mac/install/>`__
| 3. Restart computer if prompted
| 4. Open Docker Desktop and then Ion_Mob_MacOS
| **Note** Docker Desktop must be open before Ion_Mob_MacOS is started.

| **Windows Installation**:
| 1. Download
  `Ion_Mob_PC.exe <https://github.com/PNNL-CompBio/ion-mob-ms/blob/main/Ion_Mob_PC.exe>`__
| 2. Download `Docker Desktop for
  Windows <https://docs.docker.com/desktop/windows/install/>`__
| 3. Install WSL2 via PowerShell. Open “Powershell” as an
  **Administrator**, then type the command “wsl –install -d ubuntu”

4. Restart computer
5. **First** open Docker Desktop, and then Ion_Mob_PC.exe.

| **Dashboard Image**
| 

Run Overview
============

1) Workflow choice will be dictated by which type of experiment you are
   running. The option to run any individual tool is also available.
2) Depending on which workflow you’d like to run,a set of files and
   folders must be prepared ahead of time.
3) Enter parameter values and use a unique experiment name. Avoid spaces
   or any special characters in this name.
4) Double check parameter inputs, files, then run the experiment.
5) If AutoCCS was performed, you will be able to view a preview of the
   results. If this does not appear, the experiment may have failed.
6) Save results to folder. Do not use a duplicate folder name. Once
   results are saved, they will be removed from the application
   workspace.

First - Run PNNL PreProcessor
=============================

| At this point in time, PNNL PreProcessor has not been integrated into
  the application. This tool has two important aspects in the workflow:
  1) it filters and smooths data for quality control purposes, 2) it
  splits multi-field (.d) data into separate (.d) folders.
| This spliting function adds a suffix to (.d) folders depending on the
  ms level as follows: ms1 would be in “filename_1.d”, ms2 would be in
  “filename_2.d”, etc.
| This allows for both stepped-field and single-field to be processed in
  this application.

Select your Workflow
====================

There are three types of workflows to run. Each mode has separate needs
for input files, but runs a combination of the modules depicted below.

**DTIMS Single field**

Drift tube ion mobility mass spectrometry requires knowledge of
experiments and a table of calibration ions.

**A Note on Proteowizard:** For the single tool option, this application
will convert all (.d) files to mzML. For the Single-Field workflow, this
application will filter out all files suspected to come from multi-field
data - this will be determined by the PNNL PreProcessor naming suffix.
If a file suffix contains any number greater than
(filename)\ **1**\ *.d, it will be removed. For example,
(filename)*\ **2**.d would be removed from this workflow.

**DTIMS Stepped field**

Drift tube ion mobility mass spectrometry that requires specific known
targets and their masses.

**A Note on AutoCCS:** For the stepped-field experiment, autoCCS does
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

Prepare your Files
==================

Examples of each data type can be found under `test
data <https://github.com/PNNL-CompBio/ion-mob-ms/tree/main/test-data>`__
in the `github
repository <https://github.com/PNNL-CompBio/ion-mob-ms/>`__.

| **Raw Data Folder**
| Raw data is generated by vendor instruments. This data is commonly
  encoded in a propriatory format. All raw data must be together in an
  encompassing folder, some raw data types such as Agilent (.d) are
  folders themselves, these must still be isolated in an encompassing
  folder. See more details in section titled “Upload your files” below.
  Supported file types can be found on the `proteowizard
  website <https://proteowizard.sourceforge.io/doc_users.html>`__.

| **IMS Metadata Folder**
| This data is generated alongside and paired with the raw data by some
  vendors. It includes information such as instrument specifications,
  temperature deviations between runs, and electrical current changes.
  This is required for stepped field experiments and optional for single
  field experiments. Including this data for single field experiments
  improves accuracy of CCS value predictions.

| **Feature Data Folder**
| Feature files are generated by Mzmine or DEIMoS. Features, also known
  as peaks, are predicted based on signal-to-noise ratio of drift time,
  intensity, and mass/charge (m/z) ratios.

| **Target List File**
| This excel file is required for stepped field experiments. This
  contains four columns: compound name, compound ID, exact mass, unique
  ID4D file names.
| This must be created by the user with known molecules/standards and
  neutral masses in order to compare with sample data and calculate CCS
  values.

| **Metadata File**
| This hidden metadata file is generated from PreProcessed data and
  includes the following metrics: RawFileName, AcquiredTime,
  InstrumentName, IonPolarity, Well, Cartridge. This is generated in and
  required for the AutoCCS step.

| **Calibrant File**
| This text file includes calibrant information for single field
  experiments. Calibrant information includes: CCS values, mass(m),
  charge(z), m/z, and ionization.

Upload your files
=================

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
==============

**Prior** to selecting “Run Experiment”, Docker Desktop must be open.

Please confirm all variables and path locations before running
experiment.

When running experiment, do not exit the application or Docker. Doing so
may result in temporary files (such as .tar files in data folders) not
being deleted. If exited early, please ensure no temporary files exist
in experimental folders before running again.

Viewing and Saving Results
==========================

After an experiment is completed, a “Save Results” button should appear.
Select this button to find a folder to save results at.

If CCS Values were generated, a summary graph or PDF will be available
to preview depending on the experiment type.

Running Additional Experiments
==============================

To clear all parameters and results, select the “Clear Experiment”
button and confirm. Save results before clearing or they will be lost.

Errors and Troubleshooting
==========================

| **Docker Errors**
| Connectivity issues between Docker Desktop and UI_V2 may lead to
  issues with experiments completing. When an error message is seen in
  the console, check which data file was running, then manually
  **Delete** all containers in docker desktop and **restart** both
  applications. Last, check data files to ensure that no intermediate
  files (.tar extension) were left behind.

The most common connectivity timeout error may occur when the computer
logs out or enters sleep mode partway through a run. This issue becomes
more frequent when Docker Desktop is not restarted between runs.

The first time the application uses a tool, the container is pulled from
dockerhub (which is updated via github). This first pull event may be
slow but afterwards, it will be faster. One issue that may occur here is
once a container is pulled, it will not automatically update to the
latest version. To update to the latest version, you must navigate to
the “Images” tab in Docker Desktop, then “clean up” or remove images.
Once the application is run again, it will automatically update to the
latest version.

Two docker containers with the same name can not be run at the same
time, ensure that all files have unique names and no docker containers
are running or stopped before starting an experiment (these must be
deleted).

| **Recovering Data**
| When a docker container exits on its own, its experiment was completed
  successfully. When left running indefinitely, it has failed. To
  retrieve any data from partial runs, see the message console to find
  the location or “Working Directory” of the run. Data is deleted upon
  exit of the application and must be retrieved before then.

| **Docker Setup on Windows**
| Docker requires WSL2 to be enabled. This should be automatically
  enabled, is not enter “Settings”, then on the “General” page, select
  the box titled “Use the WSL 2 based engine”. Then select “Apply and
  Restart”.

| **Current Issues Exist with DEIMos in the workflow**
| DEIMos generates a slightly different output from mzMine, autoCCS
  requires the mzMine values. DEIMos has received some modifications to
  allow it to work, however some small differences exist. DEIMos is best
  suited for single field usage at this time.

DEIMos is a very efficient and accurate tool that also outperforms
mzMine in terms of speed. However, the current version is not entirely
compatible with usage in a docker container and as such, it runs slower
than expected and may run into memory issues. We hope this can be
resolved in future versions of this application. We also hope to
incorporate additional DEIMos functions in the future.

Available Tools
===============

Currently we have enabled the use of the following tools.

PNNL PreProcessor Tool - Unavailable
------------------------------------

Docker image and script to run `PNNL Pre-Processor
tool <https://pnnl-comp-mass-spec.github.io/PNNL-PreProcessor>`__.

ProteoWizard Tool
-----------------

Docker image and script to run `ProteoWizard
tool <https://proteowizard.sourceforge.io/>`__

MZMine Tool
-----------

Docker image and script to run `MZMine Java
Program <http://mzmine.github.io/>`__.

AutoCCS Tool
------------


Docker image and script to run `AutoCCS Python
script <https://github.com/PNNL-Comp-Mass-Spec/AutoCCS>`__.

Ion_Mob_PC.exe (or UI_V2)
-------------------------

This is the GUI for the dashboard.

Citation
========







.. toctree::
   :caption: Background
   :maxdepth: 1
   :hidden:

   background/info


.. toctree::
   :caption: Getting Started
   :maxdepth: 1
   :hidden:
   
   getting_started/Mac
   getting_started/Windows
   getting_started/AWS
   getting_started/HPC
   getting_started/CLI


.. toctree::
   :caption: Getting Started
   :maxdepth: 1
   :hidden:
   
   depth/CLI
   depth/GUI

.. toctree::
   :caption: Troubleshooting
   :maxdepth: 1
   :hidden:

   troubleshooting/common_issues



