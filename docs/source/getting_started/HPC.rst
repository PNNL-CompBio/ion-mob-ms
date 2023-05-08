HPC Command Line Interface
==============
Usage on a High Performance Computing Cluster (HPC) is slightly different from the other methods.
This system uses Singularity instead of Docker due to security requirements on an HPC. As HPCs may differ, 
these commands are meant to serve as a general template but may not reflect the exact usage you will require.  
These commands and scripts are build for a SLURM queue managment system. 


HPC Setup Commands
---------------------------

**Setup**   

.. code-block::  

   module load singularity
   module load python/3.7.0
   sudo yum install git
   git clone https://github.com/PNNL-CompBio/ion-mob-ms.git
   cd ion-mob-ms
   pip3 install -r requirements_py3.7_CLI.txt
   cd singularity_dev
   
   
**Run Test Data on Current Node** 

.. code-block::  
   
   python3 CLI_hpc.py --json sample.json
   
**Run Test Data using SLURM Queue** 

.. code-block::  
   
   bash IMD_hpc_in_background.sh
   
   
SLURM options in IMD_hpc_in_background.sh will have to be modified to allow it to run on your own account. 
For running large datasets, it is recommended to increase the number of available CPUS.

To run your own data view General Command Line Usage <https://ionmobility.readthedocs.io/en/latest/getting_started/AWS.html/>`__.

