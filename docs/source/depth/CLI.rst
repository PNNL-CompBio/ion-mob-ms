General Command Line Usage
==============

This page is meant as a guide for running your own data using either AWS or an HPC. Follow setup commands on the respective pages.


| Two Command Line Options Exist for runing this pipeline:   

- Json File Input
- Verbose Command
   
**Example Commands**   
  
.. code-block::  

   python3 CLI_hpc.py --json sample.json
   python3 CLI.py --json sample.json
   bash IMD_hpc_in_background.sh
   python3 CLI.py --ExpName Test_One --ExpType Stepped --ToolType PW MZ AC --PP ../test-data/SteppedField/II_Preprocessed --IMSMeta ../test-data/SteppedField/IV_ImsMetadata --ACConfig ../test-data/SteppedField/autoCCS_config.xml --TLF ../test-data/SteppedField/TargetList_NeutralMass.csv
 

**Note:** Running the verbose command option will generate a json file called sample.json. This will **overwrite** any existing sample.json file in the directory.
   
JSON Input Requirements
---------------------------

* ExpName: Experiment Name - Any name you desire. Avoid spacemarks and special characters besides underscores and dashes.
* ExpType: Experiment Type - Options are Single, Stepped, or SLIM
* ToolType: Tools you'd like to run. Options are PW, MZ, or AC. It is highly reccomended to run these sequentially or in a single pipeline.
* Data Folders - Options depend on the tool(s) you'd like to run. More information is below.

Some potential bugs currently exist with file pathing. Note to dev - fix this.  

Both relative and absolute paths are planned to be configured to work with this.  

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
           "IMS Metadata Folder": "../test-data/SteppedField/IV_ImsMetadata/*.txt",
           "AutoCCS Config File": "../test-data/SteppedField/autoCCS_config.xml",
           "Target List File": "../test-data/SteppedField/TargetList_NeutralMass.csv",
           "mzML Data Folder": "/people/jaco059/ion-mob-ms/singularity_dev/III_mzML",
           "Feature Data Folder": "/people/jaco059/ion-mob-ms/singularity_dev/IV_Features_csv/*.csv"
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




.. list-table:: Required Commands And Files for Each Experimental Pipeline Type  
   :class: scrolltable
   
   * - Experiment
     - Raw Data Folder
     - PreProcessed Data Folder
     - mzML Data Folder
     - Feature Data Folder
     - IMS Metadata Folder
     - AutoCCS Config File
     - Target List File
     - Metadata File
     - Calibrant File
   * - Command 
     - ``--Raw``
     - ``--PP``
     - ``--mzML``
     - ``--FF``
     - ``--IMSMeta``
     - ``--ACConfig``
     - ``--TLF``
     - ``--MetadataFile``
     - ``--Calibrant``
   * - Command Shorthand
     - ``-r``
     - ``-p``
     - ``-m``
     - ``-f``
     - ``-i``
     - ``-a``
     - ``-s``
     - ``-z``
     - ``-c``
   * - SingleField 
     - NA
     - Yes
     - No
     - No
     - Recommended
     - Yes
     - Recommended
     - No
     - Yes
   * - SteppedField 
     - NA
     - Yes
     - No
     - No
     - Yes
     - Yes
     - Yes
     - No
     - No
   * - SLIM
     - NA
     - Yes
     - No
     - No
     - No
     - Yes
     - Optional
     - Yes
     - Yes
