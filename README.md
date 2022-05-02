# ion-mob-ms
This is a workflow for analyzing Ion Mobility Mass-Spectrometry data. It comprises scripts and images that run diverse tools and a graphical user interface that runs data from specific experimental files. Our goal is to analyze data from three types of experiments:
1. DTIMS single field: Drift tube ion mobility mass spectrometry requires knowledge of experiments and a table of calibration ions.
2. SLIM data (also single field): Data from the SLIM machine.
3. DTIMS stepped field: Drift tube ion mobiology mass spectrometry that requires specific known targets and their masses.

![workflow](./workflow.png)

Each mode has separate needs for input files, but runs a combination of the modules depicted below.

## To run ion-mob-ms
Installation:
1. [Download and install docker](https://docs.docker.com/get-docker/) on your operating system.
2. For running the workflows developed in [Nextflow](https://www.nextflow.io/docs/latest/getstarted.html).

TODO: any Python needed for UI front end.

## Workflows component
The architecture of this toolbox is shown above, below are it's components:           

- [pnnl_preprocessor](docker/pnnl_preprocessor) dockerfile for [PNNL 
  Pre-Processor tool](https://pnnl-comp-mass-spec.github.
  io/PNNL-PreProcessor) and [hosted image](https://hub.docker.com/repository/docker/anubhav0fnu/pnnl_preprocessor).
- [proteowizard ](docker/proteowizard) dockerfile for [ProteoWizard tool]
  (https://proteowizard.sourceforge.io/) and [hosted image](https://hub.docker.com/repository/docker/anubhav0fnu/proteowizard).
- [mzmine](docker/mzmine) dockerfile for [MZMine Java Program](http://mzmine.
  github.io/) and [hosted image](https://hub.docker.com/repository/docker/anubhav0fnu/mzmine).
- [autoccs](docker/autoccs) dockerfile for  [AutoCCS Python script]
  (https://github.com/PNNL-Comp-Mass-Spec/AutoCCS) and [hosted image](https://hub.docker.com/repository/docker/anubhav0fnu/autoccs).
- [ccs_comparison](docker/ccs_comparison) dockerfile for  CCS calculation 
  with [hosted image](https://hub.docker.com/repository/docker/anubhav0fnu/ccs_comparison).

The workflows are:
[single_field.nf](./single_field.nf)
[slim.nf](./slim.nf)         
[stepped_field.nf](./stepped_field.nf)

```
./nextflow run single_field.nf \
-profile docker
```
### ion-mob-UI
This is the front-end for the entire workflow.  TODO: determine implementation and design.

## Summary
This framework will enable the end-to-end analysis of Ion Mobility MS-MS data.
