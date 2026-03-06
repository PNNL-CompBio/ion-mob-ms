# HPC Module - High-Performance Computing

## Overview

The HPC module provides Singularity container variants of IMDASH tools optimized for execution on high-performance computing systems. These are designed to run on compute clusters with SLURM job schedulers, providing parallelization and resource management capabilities.

## Files

### Main Entry Points

- **`CLI_hpc.py`** - HPC command-line interface orchestrator
  - Similar interface to `CLI.py` but uses Singularity containers
  - Submits jobs to SLURM scheduler instead of direct Docker execution
  - Supports batch job configuration and monitoring
  - Reads same JSON format as desktop CLI for compatibility

### Tool-Specific HPC Modules

Each module corresponds to a CLI tool, adapted for HPC with parallelization:

- **`AC_hpc.py`** - AutoCCS for HPC execution
  - Distributes CCS calculation across multiple compute nodes
  - SLURM resource specification supported
  - Parallelizes feature annotation using process pools
  - Handles large-scale ion mobility datasets

- **`MZ_hpc.py`** - MZmine feature detection for HPC
  - Batch processing of large sample sets
  - Parallelization of feature detection across multiple cores
  - Output aggregation from multiple parallel runs
  - Optimized for memory efficiency on shared systems

- **`PW_hpc.py`** - ProteoWizard data conversion for HPC
  - Parallel conversion of multiple vendor data files
  - Batch mzML output generation
  - Resource-efficient format conversion
  - Supports various input formats simultaneously

- **`DM_hpc.py`** - Deimos feature detection for HPC
  - Topological feature detection with parallelization
  - Distributed computation across cluster nodes
  - Memory-conscious implementation for shared systems
  - Maintains process limits to prevent resource contention

- **`Pipeline_V2_hpc.py`** - Full pipeline orchestration (HPC version)
  - Coordinates tool execution with proper sequencing
  - Intermediate file management across compute nodes
  - Resource-aware scheduling of tool chains
  - Archival and cleanup of temporary files

### Web Modules (In Development)

The following modules implement a web-based interface for remote job submission:

- **`MZ_web.py`** - Web interface for MZmine task submission
  - **Status**: In development - subject to architectural changes
  - REST API endpoints for batch job submission
  - Job status monitoring and result retrieval
  - Asynchronous processing with callback notifications

- **`PW_web.py`** - Web interface for ProteoWizard task submission
  - **Status**: In development - subject to architectural changes
  - Simplifies complex batch configuration via web forms
  - Tracks multiple concurrent conversion tasks
  - JSON-based task submission and status reporting

- **`pipeline.py`** - Web-based complete workflow interface
  - **Status**: In development - architectural refactoring in progress
  - Integrated task submission for full workflow chains
  - Real-time progress monitoring via WebSocket
  - Historical execution tracking and result browsing
  - Note: Recent architectural changes, see source for current implementation

### Job Scheduler Support

- **`MZmine_FeatureFinder-batch.xml`** - MZmine parameters for batch processing
  - Configuration template for feature detection module
  - Tuned for reproducible results across large datasets
  - Used by both CLI and HPC execution paths

- **`MZmine_FeatureFinder_Modifier.py`** - XML batch file modification utility
  - Dynamically adjusts batch XML parameters
  - Allows parameter variation across job replicates
  - Enables sweep studies across parameter space

### Singularity Container Definitions

Each tool has an associated Singularity definition file for container building:

- **`autoccs.def`** - AutoCCS container specification
- **`mzmine.def`** - MZmine container specification
- **`mzmine_updated.def`** - Updated MZmine variant
- **`proteowizard.def`** - ProteoWizard container specification
- **`proteowizard_updated.def`** - Updated ProteoWizard variant
- **`pipeline.def`** - Complete pipeline container
- **`imd_django.def`** - Django backend for web interface
- **`imd_react.def`** - React frontend for web interface
- **`imd_redis.def`** - Redis cache for web services
- **`imd_minio.def`** - MinIO object storage service

### SLURM Job Templates

Job submission templates for cluster execution:

- **`singularity-compose.yml`** - Singularity Compose orchestration (cloud deployment)
- **`docker-compose.yaml`** - Docker Compose for local testing of containerized environment

### Utility Scripts

- **`singularity_builder.sh`** - Builds Singularity containers from definition files
  - Requires Singularity to be installed on build system
  - Creates container images for cluster submission
  - Handles version management and caching

- **`fix_metadata.py`** - Metadata correction utility
  - Repairs malformed metadata in raw files
  - Ensures compatibility with downstream tools
  - Automated metadata standardization

- **`test.py`** / **`py_test.py`** - Testing/validation scripts
  - Verifies container functionality before cluster deployment
  - Tests tool integration points
  - Validates data format assumptions

### Configuration Files

- **`sample.json`** - Example HPC job configuration
  - Same format as CLI module for compatibility
  - Specifies SLURM resource requirements
  - Documents parallel execution parameters
- **`requirements.txt`** - Python dependencies for HPC modules

## Usage

### Basic HPC Execution

```bash
# Submit job to SLURM with JSON configuration
python CLI_hpc.py -j configuration.json

# Specify SLURM parameters
python CLI_hpc.py -j config.json \
                  --slurm-nodes 4 \
                  --slurm-ntasks 16 \
                  --slurm-time 04:00:00
```

### Building Containers

```bash
# Build Singularity containers from definition files
bash singularity_builder.sh

# Build specific container
singularity build autoccs.sif autoccs.def

# Build with remote builder (if local build not available)
singularity build --remote autoccs.sif autoccs.def
```

### Running Individual Tool HPC Variants

```bash
# Submit MZmine HPC job
python MZ_hpc.py --samples /path/to/raw_data \
                 --output /path/to/features \
                 --parallel 8

# Submit AutoCCS HPC job
python AC_hpc.py --features /features.csv \
                 --output /autoccs_results \
                 --slurm-nodes 2
```

### Web-Based Submission (In Development)

```bash
# Start web service (requires Django/React)
python manage.py runserver

# Submit job via REST API
curl -X POST http://localhost:8000/api/submit-job \
     -H "Content-Type: application/json" \
     -d @job_config.json
```

## Container Architecture

### Single Container Model
Each Singularity definition file creates a standalone container with:
- Tool executable and all dependencies
- Python runtime for wrapper scripts
- Required system libraries and drivers

### Multi-Container Orchestration
For complex workflows, multiple containers work together:
- **pipeline.def** - Orchestrates AC, MZ, PW tool containers
- **imd_django.def** + **imd_react.def** - Web interface for job submission
- **imd_redis.def** - Caches job status and intermediate results

## SLURM Job Submission

### Key Parameters

```bash
# Resource allocation
#SBATCH --nodes=2           # Number of compute nodes
#SBATCH --ntasks-per-node=8 # Tasks per node
#SBATCH --time=06:00:00     # Wall clock time (6 hours)
#SBATCH --mem=32G           # Memory per node

# Job naming and output
#SBATCH --job-name=mzmine_batch
#SBATCH --output=logs/mzmine_%j.out
```

### Example Job Script

```bash
#!/bin/bash
#SBATCH --nodes=4
#SBATCH --ntasks-per-node=8
#SBATCH --time=06:00:00
#SBATCH --mem=32G

module load singularity

# Run workflow via HPC CLI
python CLI_hpc.py -j /path/to/config.json \
                  --singularity-image /path/to/pipeline.sif \
                  --output-dir /project/results
```

## Key Features

- **Parallelization**: Automatic distribution across cluster resources
- **Resource Awareness**: Respects node memory and processor counts
- **Scalability**: Performance scales from single-node to multi-node jobs
- **Job Monitoring**: Real-time progress tracking and resource utilization
- **Isolation**: Singularity containers eliminate dependency conflicts
- **Cloud Deployment**: Docker Compose enables cloud provider execution

## Differences from CLI Module

| Feature | CLI | HPC |
|---------|-----|-----|
| Execution Model | Docker (local) | Singularity (cluster) |
| Job Submission | Direct execution | SLURM queue |
| Parallelization | Single node only | Multi-node possible |
| Resource Management | Docker limits | SLURM allocation |
| Container Type | Docker image | Singularity .sif |
| Typical Execution | Minutes to hours | Hours to days |

## Testing

```bash
# Test container builds
bash singularity_builder.sh --test-only

# Run on login node (small test)
python MZ_hpc.py --test-mode \
                 --samples /test-data/SingleField/I_Raw \
                 --output /tmp/test_output

# Submit test job to queue
sbatch test_job.sh
```

## Web Interface (In Development)

The web modules (`MZ_web.py`, `PW_web.py`, `pipeline.py`) provide:

- REST API for programmatic job submission
- Real-time job monitoring dashboard
- Parameter configuration forms
- Historical job tracking
- Result download interface

**Status**: These modules are in active development. Architectural changes are ongoing; refer to source code for current implementation details.

## Common Issues

1. **"Singularity not found"**
   - Solution: Load Singularity module: `module load singularity`

2. **"Container build fails"**
   - Solution: Use remote builder: `singularity build --remote container.sif def.def`

3. **Job times out**
   - Solution: Increase `--time` parameter or reduce dataset size for initial test

4. **"Permission denied" on output directory**
   - Solution: Ensure output directory is writable by your user account

5. **Memory errors during execution**
   - Solution: Increase `--mem` parameter or reduce parallel task count with `--ntasks-per-node`

## Related Modules

- **CLI Module**: Provides desktop/cloud interface; HPC module implements similar functionality for clusters
- **GUI Module**: Desktop interface; uses CLI under the hood which HPC module mirrors
- **Docker Module**: Container utilities shared between CLI and HPC execution
- **Web Dev Module**: Web interface for remote job submission (in development)

## Notes

- Container runtime logging with timestamps helps identify execution bottlenecks
- Singularity containers are immutable after build; modifications require rebuild
- Job arrays can parallelize multiple independent runs: `#SBATCH --array=1-100`
- Resource constraints should be tuned based on cluster capabilities and dataset size
- Web modules are actively developed; current production use should be validated before deployment
