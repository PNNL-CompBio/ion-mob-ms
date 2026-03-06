# CLI Module - Command Line Interfaces

## Overview

The CLI module provides command-line interfaces for executing IMDASH workflows without the graphical user interface. All tools in this module support batch processing and are suitable for automated/scripted execution on desktop computers and cloud environments.

## Files

### Entry Points
- **`CLI.py`** - Main CLI entry point for desktop/local execution
  - Parses command-line arguments for all tools and workflows
  - Supports JSON configuration files for batch/reproducible runs
  - Integrates with Docker for containerized tool execution
  - Supports all experiment types: Single Field, SLIM, Stepped Field

- **`sample.json`** - Example JSON configuration file
  - Template for specifying workflow parameters
  - Use as reference for creating your own workflow configurations

### Tool-Specific Modules
Each of the following modules handles execution for a specific tool within Docker containers:

- **`AC_cli.py`** - AutoCCS (Collision Cross-Section) calculator
  - Determines CCS values from ion mobility data
  - Supports standard and enhanced annotation modes
  - Handles single-field, SLIM, and stepped-field workflows

- **`MZ_cli.py`** - MZmine feature detection
  - Performs non-targeted feature detection on mzML data
  - Uses batch-mode XML configuration for consistency
  - Generates feature CSV files for downstream analysis

- **`PW_cli.py`** - ProteoWizard (msConvert) data conversion
  - Converts vendor mass spectrometry formats to mzML
  - Supports platform-aware execution (Windows, macOS, Linux)
  - Critical preprocessing step before feature detection

- **`PP_cli.py`** - PNNL PreProcessor
  - Filters and smooths raw ion mobility data
  - Note: Currently incomplete due to DLL compatibility issues in Wine
  - See documentation for known limitations and workarounds

- **`DM_cli.py`** - Deimos persistent homology feature detection
  - Alternative feature detection approach using topological methods
  - Resource-constrained (limited to 3 parallel processes)
  - Useful for complex datasets where traditional methods struggle

- **`Pipeline_cli.py`** - Complete workflow orchestration
  - Coordinates execution of multiple tools in proper sequence
  - Automatically selects workflow based on experiment type
  - Manages intermediate file transfers between tools
  - Provides timestamped logging for debugging and auditing

## Usage

### Basic Command-Line Execution

```bash
# Display help
python CLI.py --help

# Run with JSON configuration (recommended)
python CLI.py -j configuration.json

# Specify individual parameters
python CLI.py -n "MyExperiment" \
              -e "Single" \
              -t PW MZ AC \
              -m /path/to/mzML \
              -f /path/to/features \
              -c /path/to/calibrants.txt
```

### JSON Configuration Format

```json
{
  "ExpName": "MyExperiment",
  "ExpType": "Single",
  "ToolType": ["PW", "MZ", "AC"],
  "Calibrant File": "/path/to/calibrants.txt",
  "mzML Data Folder": "/path/to/mzML",
  "Feature Data Folder": "/path/to/features"
}
```

### Running Individual Tools

```bash
# Run only MZmine on pre-converted mzML data
python MZ_cli.py -m /path/to/mzML -f /output/features

# Run only AutoCCS (requires feature CSV)
python AC_cli.py single standard False /calibrants.txt False /features /none False /preprocessed /autoccs_config
```

## Key Features

- **Reproducibility**: JSON-based configuration ensures identical results across runs
- **Batch Processing**: Process multiple experiments programmatically
- **Timestamped Logging**: Automatic timestamp annotation for all print statements
- **Cross-Platform**: Docker containerization eliminates platform-specific dependencies
- **Experiment Type Aware**: Automatically selects appropriate workflow path

## Docker Requirements

All CLI tools require Docker to be installed and the Docker daemon to be running:

```bash
# Start Docker daemon (varies by platform)
# macOS: Docker Desktop application
# Linux: sudo systemctl start docker
# Windows: Docker Desktop application
```

## Common Issues

1. **Docker Connection Error**
   - Solution: Ensure Docker daemon is running and user has Docker permissions
   
2. **File Permission Errors**
   - Solution: Ensure source data folders are readable and output folders are writable
   
3. **Insufficient Memory**
   - Solution: Increase Docker memory allocation in Docker preferences (minimum 8GB recommended)

## Integration with Other Modules

- **GUI Module**: GUI calls CLI modules under the hood for tool execution
- **HPC Module**: Similar structure but uses Singularity containers instead of Docker
- **Pipeline Orchestration**: Pipeline_cli.py coordinates all tool modules

## Testing

Use the example configurations and test datasets in `test-data/` to validate CLI functionality:

```bash
# Test with SingleField workflow
python CLI.py -j ../test-data/SingleField/sample.json
```

## Notes

- All timestamp comments and logging are meant for debugging and audit trails
- Intermediate files are preserved (see specific tool modules for cleanup strategies)
- Tool execution order is: PW → MZ → DM → AC (with optional PP preprocessing)
