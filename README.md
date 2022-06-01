# ion-mob-ms
This is a workflow for analyzing Ion Mobility Mass-Spectrometry data. The primary goal is to facilitate the numerous steps required to analyze and interpret this type of data, as it requires numerous steps and file management can be a burden.

## Architecture
The system is designed to enable users to run individual parts via the command line, using a graphical user interface, or using Nextflow.

<img src="architecture.png" width="500">

Each mode has separate needs for input files, but runs a combination of the modules depicted below.

### Dockerized framework

### Task framework

### Orchestration

### User interface

## Installation

## Contribution


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

## Summary
This framework will enable the end-to-end analysis of Ion Mobility MS-MS data.
