# Directory and File Guide - Navigating the IMDASH Codebase

## Quick Reference

This guide helps you locate specific functionality and understand which files implement each feature.

## Feature-to-File Mapping

### Command-Line Execution

**Want to run IMDASH from the command line?**
- **Main Entry**: `CLI/CLI.py` - CLI orchestrator with argument parsing
- **JSON Config**: `CLI/sample.json` - Example configuration template
- **Tool CLIs**: `CLI/AC_cli.py`, `CLI/MZ_cli.py`, `CLI/PW_cli.py`, etc.
  - Each tool has its own CLI wrapper
  - Handles parameter validation and Docker invocation
- **Full Workflow**: `CLI/Pipeline_cli.py` - Coordinates all tools in sequence

**See**: [CLI/README.md](CLI/README.md)

### Graphical Interface

**Want to run IMDASH with GUI?**
- **Main Entry**: `GUI/GUI.py` - Main application window with tabs
- **Tool GUIs**: `GUI/AC_gui.py`, `GUI/MZ_gui.py`, etc.
  - Each tool has corresponding GUI tab
  - Input validation and parameter entry
- **Custom Widgets**: `GUI/tkButton.py`, `GUI/tkPDKViewer2.py`
  - Styled button component
  - PDF parameter viewer
- **Packaging**: `GUI/pyinstaller_script.py` - Build standalone executable

**See**: [GUI/README.md](GUI/README.md)

### High-Performance Computing

**Want to run on a compute cluster?**
- **Main Entry**: `HPC/CLI_hpc.py` - HPC command-line interface
- **Tool HPC Variants**: `HPC/AC_hpc.py`, `HPC/MZ_hpc.py`, etc.
  - Each tool adapted for cluster execution
  - Parallel processing configuration
  - SLURM integration
- **Pipeline for HPC**: `HPC/Pipeline_V2_hpc.py` - HPC workflow orchestrator
- **Container Definitions**: `HPC/*.def` files
  - Singularity container specifications
  - Build scripts: `HPC/singularity_builder.sh`

**See**: [HPC/README.md](HPC/README.md)

### Web Interface (In Development)

**Want a web-based interface?**
- **Backend**: `web_dev/drf/backend/`
  - Django REST API
  - `manage.py` - Django management
  - `imdash_api/` - API implementation
- **Frontend**: `web_dev/drf/backend/react_app_1/`
  - React TypeScript components
  - `src/components/` - UI widgets
- **Orchestration**: `docker-compose.yml` - Service composition

**See**: [web_dev/README.md](web_dev/README.md)

### Data Processing Tools

**Want to use specific processing tools?**

**Format Conversion (ProteoWizard/msConvert)**:
- CLI Wrapper: `CLI/PW_cli.py`
- GUI Wrapper: `GUI/PW_gui.py`
- HPC Variant: `HPC/PW_hpc.py`
- Container: `docker/proteowizard/` directory

**Feature Detection (MZmine)**:
- CLI Wrapper: `CLI/MZ_cli.py`
- GUI Wrapper: `GUI/MZ_gui.py`
- HPC Variant: `HPC/MZ_hpc.py`
- Config Template: `docker/MZmine_FeatureFinder-batch.xml`
- Parameter Modifier: `HPC/MZmine_FeatureFinder_Modifier.py`

**Ion Mobility Annotation (AutoCCS)**:
- CLI Wrapper: `CLI/AC_cli.py`
- GUI Wrapper: `GUI/AC_gui.py`
- HPC Variant: `HPC/AC_hpc.py`
- Config Templates: `docker/autoCCS_*.xml` (single, SLIM, stepped)

**Alternative Feature Detection (Deimos)**:
- CLI Wrapper: `CLI/DM_cli.py`
- GUI Wrapper: `GUI/DM_gui.py`
- Python Wrapper: `docker/deimos_feature_finder.py`

**Data Preprocessing (PNNL PreProcessor)**:
- CLI Wrapper: `CLI/PP_cli.py`
- GUI Wrapper: `GUI/PP_gui.py`
- Status: Experimental/limited functionality

### Data Processing Scripts (R)

**Want to use R processing scripts?**
- **Metadata Extraction**: `src/I_Extract-Agilent-d-file-metadata.R`
  - Called before main pipeline (metadata only)
  - Parses Agilent .d file structures
  
- **Drift Time Processing**: `src/II_Parse-DT-as-RT-mzML.R`
  - Converts drift time to retention time dimension
  - Enables compatibility with standard tools
  
- **Feature Annotation**: `src/V_Annotate-calibrated-features.R`
  - Final annotation step after AutoCCS
  - Matches features with CCS values
  - Generates publication-ready output

**See**: [src/README.md](src/README.md)

### Analysis Templates

**Want advanced statistical analysis?**
- **Comparison Analysis**: `Post-hoc-scripts/Single_vs_Stepped_Analysis_template.Rmd`
  - Compares Single Field and Stepped Field results
  - Statistical significance testing
  - Visualization of separation improvements

- **Target List Creator**: `Post-hoc-scripts/Target_file_list_creator.Rmd`
  - Curates high-quality features for targeted analysis
  - Confidence scoring
  - Export to various formats

**See**: [Post-hoc-scripts/README.md](Post-hoc-scripts/README.md)

### Test Data & Validation

**Want example data for testing?**
- **Single Field**: `test-data/SingleField/`
  - Simplest experimental setup
  - Good for quick validation
  
- **SLIM Workflow**: `test-data/SLIM/`
  - Long ion pathway
  - Enhanced resolution
  
- **Stepped Field**: `test-data/SteppedField/`
  - Multiple voltage stages
  - Most complex configuration

Each includes:
- Configuration files (XML, JSON)
- Calibrant references
- Example commands
- Expected results documentation

**See**: [test-data/README.md](test-data/README.md)

## Directory Organization

### Top-Level Directories

```
CLI/                      Command-line execution
GUI/                      Graphical interface
HPC/                      Cluster execution
docker/                   Container definitions
src/                      R processing scripts
test-data/                Example datasets
Post-hoc-scripts/         Analysis templates
web_dev/                  Django/React web framework
docs/                     Sphinx documentation
```

### Key Files

```
README.md                 Project overview
ARCHITECTURE_GUIDE.md     System design reference
DIRECTORY_GUIDE.md        This file
Makefile                  Build automation
requirements.txt          Python dependencies
LICENSE                   License information
```

## Execution Decision Tree

### I want to run IMDASH, how do I start?

**Is this a desktop/single-computer setup?**
```
YES → GUI preferred
     ↓
     python GUI/GUI.py
     
     OR CLI preferred
     ↓
     python CLI/CLI.py -j config.json
```

**Is this a compute cluster with SLURM?**
```
YES → Use HPC
     ↓
     python HPC/CLI_hpc.py -j config.json
     
     (or submit individual tool jobs with sbatch)
```

**Is this cloud/automated execution?**
```
YES → Use CLI
     ↓
     python CLI/CLI.py -j config.json
     
     (docker must be running)
```

**Do I want a web interface? (Future Option)**
```
YES → Use web_dev
     ↓
     cd web_dev/drf
     docker-compose up
     (visit http://localhost:3000)
```

## File Type Guide

### Python Files

**Tools and Utilities**:
- `*_cli.py`: Command-line interface wrapper for tools
- `*_gui.py`: GUI tab for tool configuration
- `*_hpc.py`: HPC variant with parallelization
- `*_web.py`: Web interface (in development)

**Special Files**:
- `CLI.py`: Main CLI entry point
- `GUI.py`: Main GUI entry point
- `CLI_hpc.py`: Main HPC entry point
- `Pipeline_cli.py`: Full workflow coordinator
- `Pipeline_V2_hpc.py`: HPC pipeline coordinator
- `manage.py`: Django management (web)

**Configuration and Utilities**:
- `sample.json`: Configuration template
- `fix_metadata.py`: Metadata repair utility
- `pyinstaller_script.py`: Windows executable builder
- `*_modifier.py`: Configuration file modifiers

### XML Configuration Files

- `*_config.xml`: Tool-specific parameter sets
- `MZmine_FeatureFinder-batch.xml`: MZmine feature detection config

**AutoCCS Variants**:
- `autoCCS_single_config.xml`: Single field configuration
- `autoCCS_slim_config.xml`: SLIM workflow configuration
- `autoCCS_step_config.xml`: Stepped field configuration

### R Scripts

- `I_*.R`: Phase I processing (metadata extraction)
- `II_*.R`: Phase II processing (format conversion)
- `V_*.R`: Phase V processing (annotation)

**Analysis Templates** (R Markdown):
- `*.Rmd`: Interactive analysis templates (Post-hoc-scripts/)

### Container Definition Files

**Singularity**:
- `*.def`: Singularity container specifications

**Docker**:
- `Dockerfile`: Main container specification
- `*.xml`: Tool batch configurations
- `environment.yml`: Conda environment spec

### Configuration and Documentation

- `requirements.txt`: Python package dependencies
- `*.json`: Configuration files and samples
- `*.csv`: Data and parameter lists
- `.env`: Environment variables (web_dev/)
- `docker-compose.*.yml`: Service orchestration

## File Search Quick Reference

### Finding Code by Functionality

**"I want to modify the MZmine feature detection parameters"**
- ✓ Configuration: `docker/MZmine_FeatureFinder-batch.xml`
- ✓ CLI implementation: `CLI/MZ_cli.py`
- ✓ GUI implementation: `GUI/MZ_gui.py`
- ✓ Parameter modifier: `HPC/MZmine_FeatureFinder_Modifier.py`

**"I want to add a new R processing script"**
- ✓ Existing scripts: `src/` directory
- ✓ Integration point: Called by CLI tool wrappers
- ✓ Example: `src/V_Annotate-calibrated-features.R` shows pattern
- ✓ Installation: Add to `docker/Dockerfile` or `requirements.txt`

**"I want to modify the CCS calculation workflow"**
- ✓ Configuration: `docker/autoCCS_*.xml` (choose variant)
- ✓ CLI wrapper: `CLI/AC_cli.py` (parameter passing)
- ✓ GUI wrapper: `GUI/AC_gui.py` (user input)
- ✓ Container: `docker/autoccs/` (executable location)

**"I want to customize output file formats"**
- ✓ Feature detection: `CLI/MZ_cli.py` (output CSV structure)
- ✓ Annotation: `src/V_Annotate-calibrated-features.R` (output schema)
- ✓ Post-hoc analysis: `Post-hoc-scripts/*.Rmd` (result formatting)

**"I want to add parallel processing on HPC"**
- ✓ HPC wrapper: `HPC/*_hpc.py` files (parallelization pattern)
- ✓ Container: `HPC/*.def` (Singularity spec with parallel libs)
- ✓ SLURM template: Comments in `HPC/*_hpc.py` show examples

## Testing and Validation

### Running Tests

**Validate installation**:
- Use test data: `test-data/SingleField/`
- Command: `python CLI/CLI.py -j test-data/SingleField/sample.json`

**Test individual tool**:
- MZmine: `python GUI/MZ_gui.py` (interactive testing)
- CLI: `python CLI/MZ_cli.py --help` (check parameters)

**Verify R scripts**:
- Run: `Rscript src/I_Extract-Agilent-d-file-metadata.R --help`

**Test HPC execution** (if cluster available):
- Submit: `sbatch HPC/submit_test.sh` (if template exists)
- Monitor: `squeue -u $USER`

## Module Dependencies

### CLI Module Dependencies

```
CLI.py
├── AC_cli.py (imports shared utilities)
├── MZ_cli.py
├── PW_cli.py
├── DM_cli.py
├── PP_cli.py
└── Pipeline_cli.py (coordinates above)

All depend on:
- Docker installation
- Python 3.7+ with standard libs
```

### GUI Module Dependencies

```
GUI.py (imports)
├── AC_gui.py (each tool tab)
├── MZ_gui.py
├── PW_gui.py
├── DM_gui.py
├── PP_gui.py
├── tkButton.py (custom widgets)
├── tkPDKViewer2.py (PDF viewer)
└── Pipeline_gui.py (integrated workflow)

Depends on:
- Tkinter (built-in Python)
- Docker installation
- GUI.py event loop
```

### HPC Module Dependencies

```
CLI_hpc.py
├── AC_hpc.py (tool implementations)
├── MZ_hpc.py
├── PW_hpc.py
etc.
└── Pipeline_V2_hpc.py (orchestrator)

Container dependencies:
├── Singularity *.def files
├── python requirements.txt
└── Tool executables (AutoCCS, MZmine, etc.)

SLURM dependencies:
- SLURM scheduler
- Singularity container system
- Shared network storage (optional)
```

## Development and Customization

### Adding a New Tool

1. **Create CLI wrapper**: `CLI/NewTool_cli.py`
   - Follow pattern of `AC_cli.py`
   - Parse parameters, validate, invoke Docker
   
2. **Create GUI wrapper**: `GUI/NewTool_gui.py`
   - Follow pattern of `AC_gui.py`
   - Call underlying CLI wrapper
   
3. **Create HPC variant**: `HPC/NewTool_hpc.py`
   - Add parallelization logic
   - SLURM parameter configuration
   
4. **Add configuration template**: `docker/newtool_config.xml`
   - Tool-specific parameters
   
5. **Update container**: `docker/Dockerfile` or `HPC/*.def`
   - Install tool executable
   
6. **Update pipeline**: `CLI/Pipeline_cli.py` and `HPC/Pipeline_V2_hpc.py`
   - Add tool sequencing if needed
   - Parameter coordination

### Modifying Existing Workflow

**Change AutoCCS parameters**:
1. Edit `docker/autoCCS_*.xml` (appropriate variant)
2. Update help text in `GUI/AC_gui.py` if needed
3. Test with `test-data/` examples
4. Update documentation: `CLI/README.md`, `GUI/README.md`

**Add new processing step**:
1. Create R script: `src/NewPhase_*.R`
2. Create wrapper: `CLI/NewPhase_cli.py` (if needed)
3. Update pipeline: `CLI/Pipeline_cli.py`
4. Document in `ARCHITECTURE_GUIDE.md`

## Documentation Locations

### User Documentation
- How to use CLI: [CLI/README.md](CLI/README.md)
- How to use GUI: [GUI/README.md](GUI/README.md)
- How to use HPC: [HPC/README.md](HPC/README.md)
- How to use web interface: [web_dev/README.md](web_dev/README.md)

### System Documentation
- Architecture overview: [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) (this file's companion)
- Directory guide: [DIRECTORY_GUIDE.md](DIRECTORY_GUIDE.md) (you are here)
- Main README: [README.md](README.md)

### Tool Documentation
- Tool parameters: Comments in `docker/*.xml` files
- Tool usage: Comments in `CLI/*.py` files
- Method details: See academic publications referenced in source comments

## Quick Command Reference

| Task | Command | File |
|------|---------|------|
| Start GUI | `python GUI/GUI.py` | GUI/GUI.py |
| Run CLI | `python CLI/CLI.py -j config.json` | CLI/CLI.py |
| Submit HPC job | `python HPC/CLI_hpc.py -j config.json` | HPC/CLI_hpc.py |
| Start web interface | `cd web_dev/drf && docker-compose up` | docker-compose.yml |
| Test with sample data | `python CLI/CLI.py -j test-data/SingleField/sample.json` | CLI/CLI.py |
| Build executable | `python GUI/pyinstaller_script.py` | GUI/pyinstaller_script.py |
| View R script help | `Rscript src/I_Extract*.R --help` | src/I_*.R |

## Notes

- This guide describes the current file organization; refer to [ARCHITECTURE_GUIDE.md](ARCHITECTURE_GUIDE.md) for design principles
- File paths are relative to repository root
- Python file imports generally follow: tool -> CLI -> container -> executable
- GUI/CLI interfaces are designed to be feature-equivalent (CLI is fundamental)
- All container-based tools require Docker/Singularity installation
