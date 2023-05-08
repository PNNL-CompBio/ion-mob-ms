Windows Graphical User Interface
==============
Windows is only recommended for small datasets. While all steps of the 
pipeline do work, there is an 
unidentified issue that will randomly cause Docker Desktop to freeze and 
leave containers in an unrecoverable state. 
This is due to the constant spinning up and down of containers and only 
occurs during the Proteowizard or MZmine steps.   
  
If Windows is your only option, this can still used. However, each time Docker freezes, you will have to restart Docker and remove hanging containers. 
It may be the case that you will have to restart your computer to get 
Docker to unfreeze. The Ion Mobility Dashboard will also have to be 
restarted.   
As consolation, we've built in a caching system so the pipeline will 
continue where it was left off and no data will be lost.


Installation
---------------

Two applications are required to run workflows: Docker Desktop, and 
Ion_Mob_PC.exe (note to dev: this needs to be rebuilt).

| 1. Download `Ion_Mob_PC.exe <https://github.com/PNNL-CompBio/ion-mob-ms/blob/main/Ion_Mob_PC.exe>`__.
| 2. Download `Docker Desktop for Windows <https://docs.docker.com/desktop/windows/install/>`__.
| 3. Install WSL2 via PowerShell. Open “Powershell” as an  **Administrator**, then type the command: 
  
  
.. code-block::
   
   wsl –install -d ubuntu


| Note: If this doesn't work, follow instructions `here <https://learn.microsoft.com/en-us/windows/wsl/install/>`__. 
| 4. Restart computer (for Docker setup).
| 5. **First** open Docker Desktop, and then Ion_Mob_PC.exe.
