# GUI Module - Graphical User Interface

## Overview

The GUI module provides a comprehensive Tkinter-based graphical interface for interactive configuration and execution of IMDASH workflows. The interface guides users through workflow setup with validation while hiding underlying Docker complexity.

## Files

### Main Entry Point
- **`GUI.py`** - Primary desktop application entry point
  - Creates main application window with tabbed interface
  - One tab per tool (AC, MZ, PW, PP, DM) plus integrated Pipeline tab
  - Handles user input validation and error reporting
  - Manages Docker container execution from GUI interactions
  - Generates JSON configuration and triggers CLI backend

### Tool-Specific GUI Modules
Each module corresponds to a CLI tool and presents its specific parameters:

- **`AC_gui.py`** - AutoCCS graphical configuration
  - Workflow type selection: Single Field, SLIM, or Stepped Field
  - Annotation mode selector (standard/enhanced)
  - Calibrant file selection
  - Feature and preprocessed data directory paths
  - Real-time validation of required inputs

- **`MZ_gui.py`** - MZmine graphical configuration
  - Input mzML directory specification
  - Output feature CSV directory path
  - Advanced parameter adjustment for MZmine batch XML
  - Data validation before execution

- **`PW_gui.py`** - ProteoWizard graphical configuration
  - Vendor data format selection
  - Input/output directory specification
  - Platform detection (Windows, Linux, macOS)
  - Conversion parameter customization

- **`PP_gui.py`** - PNNL PreProcessor graphical configuration
  - Filter and smoothing parameter selection
  - Input data directory specification
  - Output directory for preprocessed data
  - **Status**: Currently development/experimental due to DLL compatibility

- **`DM_gui.py`** - Deimos graphical configuration
  - Feature detection parameter adjustment
  - Data directory specification
  - Resource constraint settings (limited parallelization)
  - Performance tuning options

- **`Pipeline_gui.py`** - Complete workflow orchestration GUI
  - Tool selection checkboxes (which tools to execute)
  - Experiment type selector (Single, SLIM, Stepped)
  - Coordinated parameter passing between tools
  - Comprehensive status reporting and logging

### Custom GUI Components
- **`tkButton.py`** - Custom Tkinter button widget
  - Styled button implementation for consistent appearance
  - Enhanced click handling and visual feedback
  - Used throughout GUI for standardized button behavior

- **`tkPDKViewer2.py`** - PDF document viewer widget
  - Embeds PDF viewing capability in Tkinter windows
  - PDF parameter feedback display during configuration
  - Document preview without external viewer launch
  - Supports navigation and zooming

### Supporting Files
- **`pyinstaller_script.py`** - Executable packaging script
  - Converts Python GUI into standalone Windows executable
  - Uses PyInstaller to bundle Python runtime and dependencies
  - Executable runs without Python installation on end-user machines
  - Execute with: `pyinstaller pyinstaller_script.py`

- **`sample.json`** - Example workflow configuration
  - Reference template for programmatic workflow definition
  - Useful for automated/batch execution from saved configs

## Usage

### Starting the GUI Application

```bash
# Start GUI application
python GUI.py

# Alternative: Run a specific tool GUI directly
python MZ_gui.py
python AC_gui.py
```

### Creating a Standalone Executable (Windows)

```bash
# Install PyInstaller
pip install pyinstaller

# Generate executable
python pyinstaller_script.py

# Executable created in dist/ folder
```

## Workflow

A typical user workflow:

1. **Launch GUI** - `python GUI.py` opens tabbed interface
2. **Select Tool/Pipeline** - Choose which tools to execute
3. **Configure Parameters** - Fill in required directories and settings
4. **Validate Inputs** - GUI verifies all paths exist and formats are correct
5. **Review Configuration** - PDF viewer shows generated parameters
6. **Execute** - Click "Run" button to start Docker-based execution
7. **Monitor Progress** - Real-time logging displayed within GUI
8. **Review Results** - Output files available upon completion

## Key Features

- **Validation**: Comprehensive input validation with helpful error messages
- **Visual Feedback**: Status indicators, logging window, result summaries
- **PDF Integration**: View tool parameter documentation without external viewer
- **Configuration Persistence**: Save/load workflow configurations for reproducibility
- **No Docker Knowledge Required**: Docker details abstracted from user
- **Platform Aware**: Auto-detects Windows/Linux/macOS for appropriate tool selection

## GUI Architecture

### Data Flow
```
User Input in Tab
    ↓
Input Validation (dialog shows errors if invalid)
    ↓
Generate JSON Configuration
    ↓
Call Corresponding CLI Module
    ↓
Docker Container Execution
    ↓
Log Output Displayed in GUI
    ↓
Display Results/Completion Status
```

### Window Management
- **Main Window**: Parent container for all tabs
- **Tool Tabs**: Each tool gets one tab in tabbed interface
- **Pipeline Tab**: Special tab coordinating multiple tools
- **Dialog Windows**: File selectors, error messages, confirmations

## Tkinter Customization

The GUI uses custom Tkinter widgets:

- **tkButton.py** styles: Custom button appearance matching modern UX conventions
- **tkPDKViewer2.py** integration: Displays PDF preview of tool parameters

These can be extended by modifying the respective files to support additional styling or widgets.

## Docker Integration

GUI modules call CLI modules which handle Docker:

```
GUI Interface
    ↓ (JSON config)
CLI Module (AC_cli.py, MZ_cli.py, etc.)
    ↓ (parses JSON)
Docker Container
    ↓ (executes tool)
Result Files
```

## Testing

Test the GUI with sample configurations:

```bash
# Start GUI and manually configure a Single Field workflow
python GUI.py

# Use test data from ../test-data/SingleField/ for directory paths
```

## Common Issues

1. **"ImportError: No module named tkinter"**
   - Solution: Python 3 should have tkinter built-in. If missing, install via: `sudo apt-get install python3-tk` (Linux)

2. **PDF Viewer Not Working**
   - Solution: Ensure `tkPDKViewer2.py` dependencies are available (may require additional libraries)

3. **GUI Freezes During Execution**
   - Solution: Docker execution happens in GUI thread. Long-running processes will freeze UI (known limitation)

## Related Modules

- **CLI Module**: GUI generates JSON that CLI modules process
- **HPC Module**: Similar structure but with Singularity for cluster execution
- **Docker Utilities**: Underlying container management (see docker/ folder)

## Notes

- Container runtime logging with timestamps helps debug execution issues
- GUI window titles and status messages provide user feedback on execution state
- All tool parameters must be specified before execution can proceed
- Results preserved in specified output directories after execution completes
