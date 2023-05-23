Command Line Interface
==============

This page is meant as a guide for running your own data using either AWS or an HPC. Follow setup commands on the respective pages.


| Two Command Line Options Exist for runing this pipeline:   

- Json File Input
- Verbose Command
   
**Example Commands**   
  
.. code-block::  

   python3 CLI_hpc.py --json sample.json
   python3 CLI.py --json sample.json
   sbatch IMD_hpc_in_background.sh
   python3 CLI.py --ExpName Test_One --ExpType Stepped --ToolType PW MZ AC --PP ../test-data/SteppedField/II_Preprocessed --IMSMeta ../test-data/SteppedField/IV_ImsMetadata --ACConfig ../test-data/SteppedField/autoCCS_config.xml --TLF ../test-data/SteppedField/TargetList_NeutralMass.csv --mzML /absolute/path/to/III_mzML --FF /absolute/path/to/IV_Features --AutoCCS /absolute/path/to/IV_data
 

**Note:** Running the verbose command option will generate a json file called sample.json. This will **overwrite** any existing sample.json file in the directory.
   
JSON Input Requirements
---------------------------

* ExpName: Experiment Name - Any name you desire. Avoid spacemarks and special characters besides underscores and dashes.
* ExpType: Experiment Type - Options are Single, Stepped, or SLIM
* ToolType: Tools you'd like to run. Options are PW, MZ, or AC. It is highly reccomended to run these sequentially or in a single pipeline.
* Data Folders - Options depend on the tool(s) you'd like to run. More information is below.

Some potential bugs currently exist with file pathing. Note to dev - fix this.  

The use of absolute paths is **required** for any docker mounts, this consists of the three files in the example that use absolue paths.  
Either relative or absolute paths can be used to specify data locations.

**Example JSON File** 
  
.. code-block:: json

   [
       {
           "ExpName": "Test_One",
           "ExpType": "Stepped",
           "ToolType": [
               "PW",
               "MZ",
               "AC"
           ]
       },
       {
           "PreProcessed Data Folder": "../test-data/SteppedField/II_Preprocessed",
           "IMS Metadata Folder": "../test-data/SteppedField/IV_ImsMetadata",
           "AutoCCS Config File": "../test-data/SteppedField/autoCCS_config.xml",
           "Target List File": "../test-data/SteppedField/TargetList_NeutralMass.csv",
           "mzML Data Folder": "/people/UserName/ion-mob-ms/HPC/III_mzML",
           "Feature Data Folder": "/people/UserName/ion-mob-ms/HPC/IV_Features_csv",
           "AutoCCS Results": "/people/UserName/ion-mob-ms/HPC/IV_data"
       }
   ]



Verbose Command Line Options
---------------------------



.. list-table:: General Commands   
   :class: scrolltable
   
   * - Command Description
     - Path to Json
     - Experiment Name
     - Experiment Type
     - Tool Type, multiple arguments accepted.
   * - Command
     - ``--json``
     - ``--ExpName``
     - ``--ExpType``
     - ``--ToolType``
   * - Command Shorthand
     - ``-j``
     - ``-n``
     - ``-e``
     - ``-t``

     
     
.. list-table:: Required Commands And Files For Each **Pipeline**
   :class: scrolltable
   
   * - Experiment
     - Command
     - Command Shorthand
     - SingleField
     - SteppedField
     - SLIM
   * - PreProcessed Data Folder
     - ``--PP``
     - ``-p``
     - Yes
     - Yes
     - Yes
   * - mzML Data Folder
     - ``--mzML``
     - ``-m``
     - Yes
     - Yes
     - Yes
   * - Feature Data Folder
     - ``--FF``
     - ``-f``
     - Yes
     - Yes
     - Yes
   * - AutoCCS Results
     - ``--AutoCCS``
     - ``-o``
     - Yes
     - Yes
     - Yes
   * - AutoCCS Config File
     - ``--ACConfig``
     - ``-a``
     - Yes
     - Yes
     - Yes
   * - Target List File
     - ``--TLF``
     - ``-s``
     - Optional
     - Yes
     - Optional
   * - IMS Metadata Folder
     - ``--IMSMeta``
     - ``-i``
     - Recommended
     - Yes
     - No
   * - Calibrant File
     - ``--Calibrant``
     - ``-c``
     - Yes
     - No
     - Yes
   * - Metadata File
     - ``--MetadataFile``
     - ``-z``
     - No
     - No
     - Yes
     
     
     
     
