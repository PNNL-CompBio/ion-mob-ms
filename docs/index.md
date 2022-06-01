## Ion Mobility Mass Spec Dashboard

[to edit this]
You can use the [editor on GitHub](https://github.com/PNNL-CompBio/ion-mob-ms/edit/main/docs/index.md) to maintain and preview the content for your website in Markdown files. Whenever you commit to this repository, GitHub Pages will run [Jekyll](https://jekyllrb.com/) to rebuild the pages in your site, from the content in your Markdown files.

This dashboard is designed to facilitate the numerous steps required to run analysis tools required for Ion Mobility Mass Spectrometry Analysis. 

## How to install

Describe how to install this on your local machine.

## Prepare to run
You will need a series of files to start. 

## Build your workflow

There are generally three types of workflows to run:

### DTIMS single field
Drift tube ion mobility mass spectrometry requires knowledge of experiments and a table of calibration ions.

### SLIM data (also single field)
Data from the SLIM machine.

### DTIMS stepped field
Drift tube ion mobiology mass spectrometry that requires specific known targets and their masses.
Each mode has separate needs for input files, but runs a combination of the modules depicted below.

## Available Tools

Currently we have enabled the use of the following tools. 

### PNNL PreProcessor Tool
Docker image and script to run [PNNL Pre-Processor tool](https://pnnl-comp-mass-spec.github.io/PNNL-PreProcessor).

### ProteoWizard Tool
Docker image and script to run [ProteoWizard tool](https://proteowizard.sourceforge.io/)

### MZMine Tool
Docker image and script to run [MZMine Java Program](http://mzmine.github.io/).

### AutoCCS Tool
Docker image and script to run [AutoCCS Python script](https://github.com/PNNL-Comp-Mass-Spec/AutoCCS).

### ion-mob-UI
This is the front-end for the entire workflow.  TODO: determine implementation and design.

## Citation