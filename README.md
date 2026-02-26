# Ion Mobility Dashboard (IMDash)

IMDash is a containerized workflow for analyzing Ion Mobility–Mass Spectrometry (IMS-MS) data and generating collision cross-section (CCS) outputs. It packages a sequence of community tools behind a GUI and command-line interfaces, and uses container orchestration (Docker or Singularity) to reduce installation and dependency burden.

The most up-to-date documentation (usage, file specifications, troubleshooting) is located at our [Documentation site](https://ionmobility.readthedocs.io/en/latest/background/info.html).

## Repository Cloning

At this point, when cloning the repository, it is highly reccomended to use a shallow clone using the following command:
```
git clone --depth 1 https://github.com/PNNL-CompBio/ion-mob-ms.git
```


## Availability

**Graphical User Interface:**
- **Desktop GUI (Windows)**: Available (recommended for smaller datasets; see docs for known Docker stability limitations).  
  Download: `GUI/GUI_windows.exe` in this repository.
- **Desktop GUI (macOS)**: Archived on Zenodo (Intel/x86 Macs are the primary supported target; see docs for Apple Silicon notes).  
  Zenodo DOI (v1.1): https://doi.org/10.5281/zenodo.6941767
  
**Command line:**
- **Cloud (AWS) CLI**: Available (Docker-based).
- **HPC CLI**: Available (Singularity-based; SLURM-oriented templates).

## Supported IMS workflows

IMDash supports multiple IMS acquisition/processing modes (see docs for exact input requirements and required accessory files):

- **DTIMS single-field** (calibrated CCS)
- **DTIMS stepped-field / multifield** (primary CCS determination workflow)
- **SLIM / TWIMS-style workflows** (calibration-driven CCS workflows)

## Tools (high-level)

IMDash links multiple command-line tools into a single end-to-end run, with containers handling dependencies:

- **(Recommended) PNNL PreProcessor**: smoothing/QC and multifield file handling; currently run separately from IMDash (not fully integrated).
- **ProteoWizard (msConvert)**: vendor format → open format conversion (e.g., mzML)
- **MZmine 2**: feature detection
- **AutoCCS**: CCS calculation and reporting
- **Optional/experimental**: DEIMoS feature extraction support (see docs for current caveats)

## Architecture

IMDash is designed so users can run:
1) end-to-end workflows via the **GUI**, or  
2) automated runs via the **CLI** (Cloud/HPC), while still allowing individual steps to be executed separately when needed.
3) a future implementation may use nextflow.
<img src="architecture.png" width="500">

### Containerized framework
IMDash uses **Docker** for Desktop/Cloud execution and **Singularity** for HPC execution where Docker is restricted.

### Task framework
Wrapper scripts run each containerized tool and pass outputs between stages (conversion → feature detection → CCS).

### Orchestration
A Python backend coordinates tool execution, manages intermediate files, and selects the appropriate workflow path (e.g., single-field vs stepped-field).

### User interface
A desktop GUI supports interactive configuration, file selection, and execution (Docker Desktop must be running before launching the GUI).

## Installation

For full, step-by-step instructions, follow the documentation:
- https://ionmobility.readthedocs.io/en/latest/index.html

Quick pointers (see docs for details and troubleshooting):

### Desktop GUI (macOS)
1. Install Docker Desktop  
2. Download and unzip the macOS app from Zenodo (v1.1): https://doi.org/10.5281/zenodo.6941767  
3. Start Docker Desktop, then start the IMDash macOS app

### Desktop GUI (Windows)
1. Install Docker Desktop (+ WSL2 as required)  
2. Download `GUI/GUI_windows.exe` from this repository  
3. Start Docker Desktop, then start the Windows GUI executable

### Cloud (AWS) CLI
The docs include a working template for EC2 setup and running the CLI with a JSON run configuration:
- https://ionmobility.readthedocs.io/en/latest/getting_started/AWS.html

### HPC CLI (Singularity)
The docs include Singularity + SLURM-oriented templates for running with a JSON run configuration:
- https://ionmobility.readthedocs.io/en/latest/getting_started/HPC.html

## Repository layout (common entry points)

- `GUI/` — desktop executables and GUI assets
- `CLI/` — cloud/desktop command-line entry points
- `HPC/` — Singularity + scheduler templates
- `docs/` — documentation source
- `test-data/` — example inputs for validating installation / ensuring that user data matches the expected inputs.

## Contributing

Contributions are welcome:
- Please open an issue for bugs, feature requests, or tool-integration proposals.
- Pull requests are encouraged for documentation improvements, workflow extensions, and bug fixes.

## Citation

If you use IMDash in academic work, please cite the IMDash manuscript (and software archive where appropriate):

**Ion Mobility-mass spectrometry Dashboard (IMDash): an automated, multi-platform computational pipeline to support production of robust and large-scale experimental collision cross-section libraries**
- Note, submission/publication is currently in progress.

Software archive (macOS GUI v1.1):
- https://doi.org/10.5281/zenodo.6941767

## License

BSD-2-Clause (see `LICENSE`).
