# Docker Module - Container Utilities

## Overview

The Docker module contains Docker image definitions, container configuration scripts, and preprocessing utilities used by CLI and GUI modules. These define the containerized execution environment for all IMDASH tools.

## Files

### Container Definitions

- **`Dockerfile`** - Primary IMDASH Docker image specification
  - Base image: Typically Ubuntu or CentOS with required system dependencies
  - Installs: Python runtime, tool executables, R environment
  - Environmental setup for mzML processing, CCS calculation, feature detection
  - Used by both CLI and Docker Compose workflows

### Tool Installation and Configuration

- **`autoccs/`** - AutoCCS installation directory
  - Compiled AutoCCS executable
  - Configuration templates and parameter files
  - Reference calibrant databases

- **`mzmine2/`** - MZmine2 installation directory
  - Feature detection executable
  - Batch processing module configuration
  - Default parameters for reproducible detection

- **`proteowizard/`** - ProteoWizard (msConvert) installation directory
  - Format conversion executable
  - Platform-specific binaries (Windows, Linux)
  - Vendor reader libraries for proprietary formats

- **`deimos/`** - Deimos persistent homology installation directory
  - Feature detection executable using topological methods
  - Alternative to traditional peak detection
  - Configuration for different data modalities

### Configuration Files

- **`autoCCS_single_config.xml`** - Configuration template for single-field workflows
  - Parameters for AutoCCS annotation in non-dispersive ion mobility setup
  - Standard mode (no additional separation)
  - Used by AC_cli.py and AC_gui.py

- **`autoCCS_step_config.xml`** - Configuration template for stepped-field workflows
  - Parameters for stepped electric field experiments
  - Allows field variation during analysis
  - Enhanced annotation with field variation information

- **`autoCCS_slim_config.xml`** - Configuration template for SLIM (Structures for Lossless Ion Mobility) workflows
  - Long ion path for enhanced separation
  - Extended analysis time parameters
  - High-resolution ion mobility separations

- **`MZmine_FeatureFinder-batch.xml`** - Batch processing configuration for MZmine
  - Feature detection parameters (mass range, retention time filters)
  - Peak shape requirements and intensity thresholds
  - Used for non-targeted feature discovery

### Utility Scripts

- **`deimos_feature_finder.py`** - Deimos topological feature detection wrapper
  - Python interface to Deimos command-line tools
  - Handles input/output file formatting
  - Configuration for topological parameter selection
  - Useful for datasets where peak-picking methods fail

- **`ccs_comparison.py`** - CCS value comparison and validation utility
  - Compares calculated CCS values against reference databases
  - Validation of AutoCCS annotation accuracy
  - Quality metrics and discrepancy reporting
  - Assists in identifying problematic features

- **`fix_metadata.py`** - Metadata correction and standardization
  - Repairs malformed metadata in raw data files
  - Ensures compatibility with downstream tools
  - Standardizes metadata format across different instruments
  - Critical preprocessing for heterogeneous data sources

- **`ccs_comparison/`** - Comparison tool directory (if separate)
  - CCS database files
  - Comparison scripts and analysis results
  - Validation output from feature annotation

- **`R_*.R`** - R scripts for specialized processing
  - **`R_Annotate_features_V.R`** - Feature annotation in R
  - **`R_Metadata_I.R`** - Metadata processing and integration
  - **`R_PARSE_II.R`** - Advanced parsing and processing
  - Integrated into Docker image for complete analysis pipeline

### Environment Configuration

- **`environment.yml`** - Conda environment specification
  - Python packages and versions for reproducible builds
  - R packages for data processing
  - System-level dependencies
  - Used in development and testing

## Container Execution

### Key Concepts

**Docker Client** → **Docker Daemon** → **Container Execution**
```
User Command
    ↓
Docker CLI
    ↓
Docker Daemon (background service)
    ↓
Container Isolation
    ↓
Tool Execution (in sandbox)
    ↓
Result Output
```

### Mounted Volumes

Containers need access to host filesystems:

```bash
# Example: Running container with mounted data volume
docker run -v /host/data:/container/data \
           -v /host/config:/container/config \
           imdash:latest python script.py
```

- Input data volumes (read-only recommended)
- Output directory volumes (write access required)
- Configuration file volumes
- Temporary processing space

### Environment Variables

Tools often require environment configuration:

```bash
# Common Docker environment settings
-e JAVA_OPTS="-Xmx8g"        # MZmine memory allocation
-e OMP_NUM_THREADS=8          # Parallel processing threads
-e WINE_CPU_TOPOLOGY=4:2      # Virtual CPU topology for Wine
```

## Building Containers

### Build From Dockerfile

```bash
# Basic build
docker build -t imdash:latest .

# Build with specific base image
docker build -t imdash:ubuntu22 \
             --build-arg BASE_IMAGE=ubuntu:22.04 .

# Build and tag multiple versions
docker build -t imdash:1.0 -t imdash:latest .
```

### Build Context

Dockerfile uses context files for:
- Tool installers (if included)
- Configuration templates
- Initialization scripts
- Python requirements files

## Usage Patterns

### Development Testing

```bash
# Interactive container for debugging
docker run -it --rm \
           -v $PWD:/work \
           -w /work \
           imdash:latest bash

# Run single command
docker run --rm \
           -v $PWD:/data \
           imdash:latest python script.py --help
```

### Production Execution

```bash
# Background execution with result persistence
docker run -d \
           --name job_$(date +%s) \
           -v /project/data:/data \
           -v /project/results:/results \
           imdash:latest python CLI.py -j config.json

# Monitor execution
docker logs job_1234567890

# Retrieve results after completion
docker cp job_1234567890:/results /project/results
```

## Configuration Templates

### AutoCCS Configuration

The three AutoCCS templates correspond to experimental setups:

**Single Field** (`autoCCS_single_config.xml`):
- Constant electric field
- Standard ion mobility separation
- Simplest experimental configuration

**SLIM** (`autoCCS_slim_config.xml`):
- Long serpentine ion path
- Enhanced separation resolution
- Extended analysis time
- Higher resolution CCS values

**Stepped Field** (`autoCCS_step_config.xml`):
- Varying electric field
- Multiple separation stages
- Additional information content
- Complex but more powerful separation

### MZmine Feature Detection

`MZmine_FeatureFinder-batch.xml` contains:

```xml
<!-- Peak shape requirements -->
<min_height>500</min_height>
<min_symmetry>0.8</min_symmetry>

<!-- Retention time handling -->
<rt_tolerance>0.1</rt_tolerance>
<min_rt_duration>0.5</min_rt_duration>

<!-- Feature combination -->
<mz_tolerance>0.01</mz_tolerance>
<intensity_threshold>1000</intensity_threshold>
```

Modify these values based on your data characteristics.

## Integration Points

### With CLI Module
CLI modules mount Docker volumes and pass parameters to containerized tools:

```
CLI Script → Docker Engine → Container with Vol Mounts → Tool Execution
    ↓
  JSON Config File
    ↓
  Tool-specific parameters converted to CLI arguments
    ↓
  Mounted directories for input/output
```

### With GUI Module
GUI generates JSON → CLI modules use Docker containers:

```
GUI Validation → JSON Generation → CLI Wrapper → Docker Execution
```

### With HPC Module
HPC uses Singularity containers (built from Docker or standalone):

```
Docker Image → Singularity Conversion → Singularity .sif File → SLURM Execution
```

## Common Docker Operations

### Check Container Status
```bash
docker ps -a                      # List all containers
docker images                     # List available images
docker logs [container_id]        # View container output
docker inspect [container_id]     # Detailed container info
```

### Clean Up Resources
```bash
docker rm $(docker ps -aq)        # Remove all stopped containers
docker rmi imdash:old             # Remove specific image
docker system prune               # Clean unused objects
```

### Troubleshooting

```bash
# Check if image exists
docker image ls imdash

# Verify volume mounts
docker inspect --format='{{.Mounts}}' [container_id]

# Test tool in container
docker run -it imdash:latest mzmine --version
```

## Dependency Management

Tools included in Docker image:

- **MZmine2**: Feature detection for untargeted analysis
- **ProteoWizard (msConvert)**: Format conversion (mzXML, mzML, netCDF)
- **AutoCCS**: CCS calculation and ion mobility annotation
- **Deimos**: Persistent homology-based feature detection
- **PNNL PreProcessor**: Ion mobility data filtering (optional/experimental)
- **R Runtime**: Statistical analysis and metadata processing
- **Python 3.9+**: Wrapper scripts and automation

## Known Limitations

1. **Windows Format Support**
   - ProteoWizard requires Wine for reading proprietary Windows formats
   - Performance impact for format conversion

2. **GPU Acceleration**
   - Current containers do not support GPU execution
   - Feature detection and CCS calculation are CPU-bound

3. **Disk Space**
   - Container images can be large (2-5 GB typically)
   - Intermediate processing files require significant space

4. **Network Access**
   - Containers by default have limited network access
   - Restrict or enable based on security requirements

## Performance Tuning

### Memory Allocation

```bash
# Increase Docker memory limit
docker run --memory=16g imdash:latest python script.py
```

### CPU Resources

```bash
# Limit CPU usage
docker run --cpus=4 imdash:latest python script.py
```

### Temporary Storage

```bash
# Use fast SSD for temporary files
docker run -v /fast/ssd:/tmp imdash:latest python script.py
```

## Testing Containers

```bash
# Test with small dataset
docker run -v /test-data:/data imdash:latest \
           python /data/quick_test.py

# Validate all tools
docker run imdash:latest bash -c \
           "mzmine --version && autoccs --help && msconvert --version"
```

## Notes

- All container execution is isolated from host system
- No permanent data in containers (use volumes)
- Configuration files can be version-controlled outside containers
- Container images should be backed up or rebuilt from Dockerfile after updates
