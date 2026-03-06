# Architecture Guide - IMDASH System Design

## System Overview

IMDASH (Ion Mobility Mass Spectrometry Dashboard) is a comprehensive analytical platform for processing and annotating ion mobility-coupled mass spectrometry data. The system is designed with modular architecture supporting multiple execution environments (desktop, cloud, and HPC clusters) while maintaining consistent workflow semantics across all platforms.

## Architectural Principles

### 1. Multi-Interface Design

IMDASH provides three execution interfaces serving different use cases:

**Command-Line Interface (CLI)**
- Target: Automated/scripted execution
- Environment: Cloud platforms, batch scripts, continuous integration
- Input: JSON configuration files
- Execution: Direct process invocation
- Container: Docker

**Graphical User Interface (GUI)**
- Target: Interactive workflow configuration
- Environment: Desktop computers (Windows, macOS, Linux)
- Input: GUI widgets and dialogs
- Execution: GUI event handlers
- Underlying: CLI modules called by GUI

**High-Performance Computing (HPC)**
- Target: Large-scale analysis on compute clusters
- Environment: SLURM-based clusters
- Input: JSON configuration files
- Execution: Job scheduler submission
- Container: Singularity  
- Parallelization: Multi-node resource allocation

### 2. Container-Based Isolation

All tool execution is containerized for reproducibility and dependency isolation:

**Docker (CLI/GUI)**
- Development and local testing
- Cloud provider integration
- Complete environment bundling
- Cross-platform compatibility

**Singularity (HPC)**
- Cluster compatibility without privileged daemon
- Immutable container guarantee
- Native integration with job schedulers
- Built from Docker images when needed

### 3. Consistent Configuration Format

All interfaces use JSON configuration files enabling:
- Human-readable workflow specification
- Machine-parseable parameter definition
- Version control compatibility
- Reproducibility across different execution contexts

### 4. Modular Tool Integration

Tools (MZmine, AutoCCS, ProteoWizard, Deimos) are wrapped in:
- Python CLI modules (tool-specific)
- GUI tab modules (GUI-specific)
- HPC variants (parallelized)
- Consistent parameter normalization

## Core Components

### Processing Pipeline

IMDASH implements a five-phase processing pipeline:

```
┌────────────────────────────────────────────────────────┐
│          Phase I: Data Quality Control                   │
│                                                          │
│  Extract metadata from raw vendor formats              │
│  Validate data structure and acquisition conditions   │
│  Output: Metadata CSV                                  │
└──────────────────────┬─────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────┐
│      Phase II: Format Conversion & Preprocessing        │
│                                                          │
│  ProteoWizard (msConvert): Convert to mzML format     │
│  Script II: Parse drift time as retention time         │
│  PNNL PreProcessor (optional): Filter/smooth data     │
│  Output: Standardized mzML with ion mobility data      │
└──────────────────────┬─────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────┐
│         Phase III: Feature Detection                    │
│                                                          │
│  Primary: MZmine 2 (peak picking & alignment)          │
│  Alternative: Deimos (topological methods)             │
│  Output: Feature CSV with m/z, RT, intensity           │
└──────────────────────┬─────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────┐
│    Phase IV: Ion Mobility Annotation (CCS)             │
│                                                          │
│  AutoCCS: Calculate collision cross-section values     │
│  Uses calibrant reference for calculation              │
│  Output: CCS values appended to features               │
└──────────────────────┬─────────────────────────────────┘
                       ↓
┌────────────────────────────────────────────────────────┐
│     Phase V: Annotation & Statistical Analysis          │
│                                                          │
│  Script V: Annotate features with CCS information      │
│  Post-hoc analysis: Statistical comparison              │
│  Output: Final annotated feature matrix                │
└────────────────────────────────────────────────────────┘
```

### Experiment Type Routing

Workflows adapted based on experimental setup:

```
Input Selection
    ↓
┌─────────────────────────────────────────────────┐
│     Experiment Type Determination                │
├─────────────────────────────────────────────────┤
│                                                   │
│  Single Field ─────→ Constant voltage            │
│  SLIM ─────────────→ Extended path ion mobility │
│  Stepped Field ────→ Variable voltage stages   │
│                                                   │
└────────────┬────────────────────────────────────┘
             ↓
    Workflow-Specific Configuration
    (AutoCCS parameter sets)
             ↓
    Pipeline Execution with Routing
```

Type selection determines:
- Configuration template selection
- AutoCCS parameter settings
- Calibrant matching
- Data interpretation methodology

### File Organization Model

The system maintains consistent organization across execution contexts:

**Input Structure**
```
project/
├── raw_data/              # Original vendor format
├── config/                # Workflow JSON and tool configs
└── metadata/              # Instrument parameters
```

**Processing Pipeline**
```
project/
├── I_Raw/                 # Original data (reference)
├── II_Preprocessed/       # ProteoWizard output (mzML)
├── III_mzML/              # Script II DT processing
├── IV_Features_csv/       # MZmine feature detection
├── IV_ImsMetadata/        # Extracted metadata
└── IV_Results/            # Final annotated features
```

## Execution Models

### Desktop/CLI Model

```
User Command (CLI/JSON)
    ↓
Python Wrapper (CLI module)
    ↓
Docker Daemon Check
    ↓
Container Preparation
    ├── Volume Mounts
    ├── Environment Variables
    └── Parameter Injection
    ↓
Container Execution
    ├── Tool Execution
    ├── Standard Output/Error Capture
    └── Exit Code Tracking
    ↓
Result Retrieval
    └── Output Files from Mounted Volumes
```

**Characteristics**:
- Synchronous execution (user waits for completion)
- Direct file system access
- Real-time output monitoring
- Single-node parallelization (thread-level only)

### GUI Model

```
User Interaction (GUI Widgets)
    ↓
Input Validation
    ├── File Path Verification
    ├── Parameter Range Checking
    └── Format Validation
    ↓
JSON Generation
    └── GUI → JSON Configuration
    ↓
CLI Module Invocation
    └── Call underlying CLI with JSON config
    ↓
Output Display
    ├── Logging Window
    ├── Status Indicators
    └── Result Summary
```

**Characteristics**:
- User-friendly parameter entry
- Real-time input validation
- Asynchronous task execution (with GUI responsiveness challenge)
- Abstraction of Docker complexity

### HPC/Cluster Model

```
User Configuration (JSON)
    ↓
SLURM Job Script Generation
    ├── Resource Allocation
    ├── Container Specification
    └── Output Redirection
    ↓
Job Queue Submission
    ├── Dependency Resolution (if chained jobs)
    └── Priority Queuing
    ↓
Scheduler Handling
    └── Automatic Resource Allocation
    ↓
Container Execution (Parallel)
    ├── Multiple Compute Nodes
    ├── Task Distribution via MPI/Process Pools
    └── Intermediate File Management
    ↓
Result Aggregation
    ├── Partial Result Combination
    ├── Consistency Verification
    └── Cleanup of Temporary Files
```

**Characteristics**:
- Asynchronous execution (user submits and checks later)
- Multi-node parallelization
- Resource scheduling and allocation
- Long-running workflow support

## Module Interaction Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                    User Interface Layer                      │
├──────────────────────┬──────────────────┬──────────────────┤
│      CLI.py          │     GUI.py       │   CLI_hpc.py     │
│   (JSON Config)      │  (GUI Widgets)   │  (HPC Submission)│
└──────────┬───────────┴────────┬─────────┴─────────┬────────┘
           │                    │                   │
           └────────────────────┼───────────────────┘
                                ↓
                   ┌────────────────────────┐
                   │  Tool CLI Modules      │
                   ├────────────────────────┤
                   │ AC_cli, MZ_cli, etc.  │
                   │ Parameter Normalization │
                   │ Tool Invocation        │
                   └──────────────┬─────────┘
                                  ↓
                   ┌────────────────────────┐
                   │  Container Runtime     │
                   ├────────────────────────┤
                   │ Docker (CLI/GUI)       │
                   │ Singularity (HPC)      │
                   │ Volume Management      │
                   └──────────────┬─────────┘
                                  ↓
                   ┌────────────────────────┐
                   │  Tool Executables      │
                   ├────────────────────────┤
                   │ MZmine, AutoCCS, etc. │
                   │ R Scripts (src/)       │
                   │ Proteowizard, Deimos │
                   └────────────────────────┘
```

## Data Flow

### Complete Analysis Workflow

```
Raw Vendor Data (.d files)
    ↓
ProteoWizard (PW_cli.py in Docker)
    ├── Input: Raw data directory
    ├── Process: Format conversion to mzML
    └── Output: mzML file with ion mobility preserved
    ↓
Script II (II_Parse-DT-as-RT-mzML.R in Docker)
    ├── Input: mzML file
    ├── Process: Drift time parsed as retention time
    └── Output: mzML with RT dimension
    ↓
MZmine (MZ_cli.py in Docker)
    ├── Input: Preprocessed mzML
    ├── Process: Non-targeted feature picking/alignment
    └── Output: Feature CSV (m/z, RT, intensity)
    ↓
AutoCCS (AC_cli.py in Docker)
    ├── Input: Feature CSV + calibrants
    ├── Process: CCS calculation with calibration
    └── Output: Features with CCS values
    ↓
Script V (V_Annotate-calibrated-features.R in Docker)
    ├── Input: Features with CCS + Reference databases
    ├── Process: Feature annotation with confidence scores
    └── Output: Fully annotated feature matrix
    ↓
Post-hoc Analysis (Post-hoc-scripts/*.R)
    ├── Input: Annotated features from multiple samples
    ├── Process: Statistical analysis, visualization
    └── Output: Results, figures, target lists
```

### Configuration Propagation

```
User Input (JSON file or GUI)
    ↓
Configuration Validation
    ├── Path verification
    ├── Parameter range checking
    ├── File format validation
    └── Dependency resolution
    ↓
Workflow Type Selection
    ├── Single, SLIM, or Stepped Field
    └── Tool selection (MZmine or Deimos)
    ↓
Container Preparation
    ├── Tool-specific env vars
    ├── Config file injection
    ├── Volume mount specification
    └── Resource allocation
    ↓
Tool-Level Configuration
    ├── XML batch files (MZmine)
    ├── Configuration objects (AutoCCS)
    └── Environment variables (Deimos)
    ↓
Consistent Execution
    └── All interfaces produce identical results
```

## State Management

### Job Lifecycle

```
SUBMITTED
    ↓
QUEUED (HPC only)
    ↓
RUNNING
    ├── Tool 1: Running
    ├── Tool 1: Complete
    ├── Tool 2: Running
    ├── Tool 2: Complete
    └── ... (Tool N)
    ↓
COMPLETED / FAILED
    ↓
ARCHIVED (optional)
```

### State Persistence

**CLI/Desktop**: 
- No persistent state (single execution)
- Output files serve as completion indicator
- Logs deleted after execution (optional preservation)

**GUI**: 
- In-memory state during execution
- Results persisted to output directories
- Optional job history (future enhancement)

**HPC**: 
- Database tracking of job states (planned)
- Checkpoint/restart capability
- Result archival and retrieval

## Tool Integration Points

### Tool Wrapper Pattern

Each tool follows consistent wrapping pattern:

```python
# Generic tool wrapper (AC_cli.py, MZ_cli.py, etc.)
class ToolWrapper:
    def __init__(self, config):
        self.config = config
        self.validate_inputs()
        
    def validate_inputs(self):
        # Check required files exist
        # Verify parameter ranges
        # Test Docker connectivity
        pass
    
    def prepare_container(self):
        # Build docker run command
        # Prepare volume mounts
        # Set environment variables
        pass
    
    def execute(self):
        # Run container
        # Stream output
        # Capture exit code
        pass
    
    def validate_outputs(self):
        # Check expected output files
        # Verify file formats
        # Log completion status
        pass
```

### Tool Configuration Normalization

Common parameter mapping across tools:

```python
# User provides (JSON)
{
    "ExpName": "MyExperiment",
    "ExpType": "Single",
    "Calibrant File": "/path/calibrants.txt"
}

# CLI converts to tool-specific format
CLI_config = {
    "name": "MyExperiment",
    "workflow_type": "single",
    "calibrant_path": "/path/calibrants.txt"
}

# GUI generates same JSON structure
# HPC uses same JSON for container execution
```

## Scalability Considerations

### Single Node (Desktop/CLI)

**Limits**:
- CPU cores: System-dependent (typically 4-16)
- Memory: System-dependent (8-64 GB typical)
- Storage: System-dependent
- Processing time: Hours to days for large datasets

**Optimization**:
- Parameter tuning for available resources
- Disk caching vs. memory trade-offs
- Sequential vs. parallel tool execution

### Multi-Node (HPC)

**Capabilities**:
- Distributed processing across compute nodes
- Automatic resource allocation via scheduler
- Job parallelization (task arrays)
- Storage scaling with parallel I/O

**Optimization**:
- Optimal task granularity selection
- Communication overhead minimization
- Load balancing across nodes
- I/O bottleneck avoidance

## Security Model

### Container-Level Isolation

- Tools run in container sandbox
- Limited host file system access (via mounts)
- No container-to-container communication (unless specified)
- Temporary files in container cleaned after execution

### Access Control (Planned - Web Interface)

- User authentication (JWT tokens)
- Role-based access (admin, user, viewer)
- Project-level permissions
- Audit logging of all operations

### Data Protection

- Sensitive parameters never logged to stdout
- Temporary intermediate files cleaned up
- Result files inherit user permissions
- Configuration files should not contain secrets (use env vars)

## Error Handling Strategy

### Validation Layers

```
User Input Validation (GUI/CLI)
    ↓
Configuration Format Validation
    ↓
File System Validation (paths exist, writable)
    ↓
Docker/Singularity Connectivity Check
    ↓
Container Execution Error Handling
    ├── Timeout detection
    ├── Exit code checking
    └── Output parsing for errors
    ↓
Result Validation
    └── Output file structure check
```

### Error Recovery

**Recoverable Errors**:
- Missing input files → Clear error message, suggest fix
- Invalid parameter ranges → Validation feedback
- Temporary Docker connection issues → Retry mechanism
- Timeout on long-running task → Checkpoint and resume (planned)

**Non-Recoverable Errors**:
- Corrupt input data → Abort with diagnostic
- Incompatible tool versions → Suggest container rebuild
- Permanent storage failures → Recommend data recovery

## Performance Characteristics

### Typical Execution Times (Single Node)

| Task | Duration | Memory | Storage |
|------|----------|--------|---------|
| ProteoWizard (100 MB raw) | 5-10 min | 2 GB | 100 MB output |
| MZmine (100 MB mzML) | 10-30 min | 4 GB | 10 MB features |
| AutoCCS (1000 features) | 5-15 min | 2 GB | 1 MB CCS |
| Complete pipeline | 30-60 min | 8 GB | 200 MB total |

### Parallelization Gains (HPC)

- 4-node execution: ~3x speedup (communication overhead)
- 8-node execution: ~6x speedup (increasing overhead)  
- 16-node execution: ~9x speedup (diminishing returns)

**Limiting Factors**:
- I/O bottlenecks (network storage)
- Data serialization overhead
- Inter-process communication costs

## Future Architecture Enhancements

### Planned Improvements

1. **Streaming Data Processing**
   - Process large files without full memory loading
   - Reduce memory requirements
   - Enable processing of multi-GB raw data

2. **Advanced Scheduling**
   - Workflow dependency management
   - Automatic resource optimization
   - Cost-aware execution (cloud environments)

3. **Distributed Database**
   - Reference database replication
   - Local caching of frequently used data
   - Faster annotation lookups

4. **Real-time Monitoring**
   - WebSocket-based live progress updates
   - Resource utilization dashboards
   - Advanced job management

5. **Machine Learning Integration**
   - Automated parameter optimization
   - Feature quality prediction
   - Anomaly detection in results

## Related Documentation

- [DIRECTORY_GUIDE.md](DIRECTORY_GUIDE.md) - File-by-file navigation
- [README.md](README.md) - Project overview
- CLI/README.md - Command-line usage
- GUI/README.md - GUI interface guide
- HPC/README.md - Cluster execution guide
- docker/README.md - Container details

## Notes

- This architecture prioritizes modularity and reproducibility over performance
- Multi-interface design supports diverse user workflows
- Container isolation ensures result reproducibility across platforms
- Tool-agnostic design allows plugging in new analytical methods
- Consistent configuration format enables workflow portability
