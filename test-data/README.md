# Test Data - Example Workflows and Validation

## Overview

The `test-data` directory contains example datasets representing three distinct ion mobility experimental setups. These datasets are designed for testing IMDASH functionality, validating new features, and demonstrating proper workflow execution.

## Experimental Workflows

IMDASH supports three distinct ion mobility separation modalities:

### 1. Single Field Workflow

**Directory**: `test-data/SingleField/`

**Experimental Setup**:
- Constant electric field ion mobility separation
- Standard commercial instrumentation (e.g., Agilent 6560)
- Single ion mobility dimension
- Simplest configuration; shortest analysis time

**Data Files**:

- **`RawFiles_Metadata.csv`** - Experimental metadata
  - Sample identifications and parameters
  - Acquisition settings (electric field voltage)
  - Temperature and pressure conditions
  - Comments on sample preparation

- **`TargetList-IONS_test.csv`** - Target ion list for analysis
  - m/z values of ions of interest
  - Expected retention times (if applicable)
  - Minimum intensity thresholds
  - For targeted feature analysis

- **`I_Raw/`** - Raw instrument output
  - Agilent .d directories containing vendor format data
  - Contains MS data with ion mobility separation results
  - Pre-acquisition metadata and calibration info
  - **Not included in repository** (large files; use as reference structure)

- **`II_Preprocessed/`** - ProteoWizard converted data
  - mzML format output from msConvert
  - Ion mobility data preserved in DT dimension
  - Ready for feature detection
  - Smaller file size than raw format

- **`III_mzML/`** - Processed mzML with RT mapping
  - Drift time converted to retention time dimension
  - Script II output (Parse-DT-as-RT-mzML.R)
  - Compatible with traditional metabolomics tools
  - Alternative to II_Preprocessed for tools requiring RT

- **`IV_Features_csv/`** - Feature detection results
  - MZmine output from feature detection
  - Peak picking and alignment results
  - CSV format: m/z, retention time, intensity by sample
  - Input for AutoCCS annotation

- **`IV_ImsMetadata/`** - Ion mobility metadata
  - Extracted from raw data (Script I output)
  - Instrument parameters and acquisition conditions
  - Reference for reproducibility

- **`IV_Results/`** - Final analysis output
  - AutoCCS ion mobility annotation
  - CCS values for detected features
  - Statistical summaries
  - Publication-ready tables and figures

- **`Calibrants-CCS_AgilentTuneMix.txt`** - CCS calibrant reference
  - Standard mixture for CCS calculation
  - Agilent Tune Mix composition
  - Known CCS values for calibration
  - Required by AutoCCS for reference

- **`autoCCS_config.xml`** - AutoCCS configuration
  - Parameter settings for Single Field workflow
  - Adapted for constant voltage operation
  - Can be customized for other calibrants

- **`MZmine_FeatureFinder-batch.xml`** - Feature detection configuration
  - Batch processing settings for MZmine
  - Peak shape and intensity requirements
  - Mass and time tolerance parameters
  - Reproducible across different samples

- **`Command_run_autoccs.txt`** - Example command sequence
  - Shell commands for running analysis pipeline
  - Step-by-step workflow execution
  - Parameter values for reproducibility
  - Reference for automated scripting

- **`SofwareTools-and-Params.csv`** - Tool and parameter documentation
  - Software versions used in sample analysis
  - Key parameters for each tool
  - References to method publications
  - Metadata for method reproducibility

### 2. SLIM Workflow

**Directory**: `test-data/SLIM/`

**Experimental Setup**:
- Structures for Lossless Ion Mobility Separations
- Long serpentine ion pathway (extended length)
- Very high ion mobility resolution
- Extended analysis time; enhanced separation

**Data Organization**: Same structure as Single Field but adapted for SLIM:

- Enhanced resolution in DT dimension
- Longer analysis times (40-60 minutes typical)
- Higher CCS value precision
- Configuration specifically for SLIM electric field operation

**Key Differences from Single Field**:
- `autoCCS_slim_config.xml` - SLIM-specific parameter settings
- Longer drift times (higher values in data)
- Tighter CCS value clustering
- May show additional features due to separation power

### 3. Stepped Field Workflow

**Directory**: `test-data/SteppedField/`

**Experimental Setup**:
- Multiple electric field strengths during analysis
- Stepping pattern provides additional dimensionality
- Complex but powerful separation technique
- Highest information content

**Data Organization**: Same structure adapted for stepped-field:

- Configuration for multiple voltage stages
- DT values converted with field-step accounting
- Enhanced ion mobility resolution with field variation
- Most complex calibration procedure

**Key Differences**:
- `autoCCS_step_config.xml` - Stepped field configuration
- DT dimension accounts for multiple voltage settings
- Additional metadata describing stepping pattern
- Requires specialized calibration mixture

## Using Test Data

### Quick Start Validation

```bash
# Test IMDASH installation with Single Field data
cd test-data/SingleField

# Check data integrity
ls -R
# Verify all expected directories exist

# Run minimal feature detection test
mzmine /test-data/SingleField/II_Preprocessed/converted.mzML \
       --config MZmine_FeatureFinder-batch.xml \
       --output test_features.csv
```

### Full Workflow Testing

```bash
# Option 1: Using CLI
cd /path/to/ion-mob-ms
python CLI/CLI.py -j test-data/SingleField/sample.json

# Option 2: Using GUI
python GUI/GUI.py
# <- Navigate to GUI and point to test-data/SingleField directories

# Option 3: Using HPC (if available)
python HPC/CLI_hpc.py -j test-data/SingleField/sample.json
```

### Working with Individual Tools

```bash
# Test ProteoWizard conversion (if raw .d files available)
msconvert test-data/SingleField/I_Raw/*.d \
          -o test-data/SingleField/II_Preprocessed/ \
          --mzML

# Test MZmine feature detection
# (MZmine requires GUI or batch command)

# Test AutoCCS on existing features
python CLI/AC_cli.py single standard False \
                     test-data/SingleField/Calibrants-CCS_AgilentTuneMix.txt \
                     False \
                     test-data/SingleField/IV_Features_csv \
                     /none \
                     False \
                     test-data/SingleField/II_Preprocessed \
                     test-data/SingleField/autoCCS_config.xml
```

## File Structure Reference

### Per-Workflow Directory

```
TestWorkflow/
├── I_Raw/                              # Original instrument output
│   └── *.d/                            # Agilent .d directories (if available)
├── II_Preprocessed/                    # ProteoWizard mzML output
│   └── sample_converted.mzML
├── III_mzML/                           # Script II drift time processed
│   └── sample_with_rt.mzML
├── IV_Features_csv/                    # MZmine feature detection
│   └── features.csv
├── IV_ImsMetadata/                     # Extracted metadata
│   └── metadata.csv
├── IV_Results/                         # Final annotated features
│   └── annotated_features.csv
├── RawFiles_Metadata.csv               # Experimental parameters
├── TargetList-IONS_test.csv            # Target ions for analysis
├── Calibrants-CCS_AgilentTuneMix.txt   # CCS calibrant reference
├── autoCCS_config.xml                  # CCS calculation config
├── MZmine_FeatureFinder-batch.xml      # Feature detection config
├── Command_run_autoccs.txt             # Execution example
└── SofwareTools-and-Params.csv         # Methods reproducibility
```

## Data Sets

### Available Datasets

- **SingleField**: Minimal dataset for quick validation
  - Small number of samples
  - Short analysis times
  - ~50 features detected
  - ~30 features successfully annotated with CCS

- **SLIM**: Extended resolution demonstration
  - Shows enhanced separation capability
  - Higher CCS value precision
  - ~80 features detected
  - Complex ion assignments possible

- **SteppedField**: Complex workflow example
  - Most sophisticated technique
  - Highest information content
  - ~100 features detected  
  - Advanced CCS matching required

### Data Sizes

```
SingleField:
  II_Preprocessed (mzML):    ~50-100 MB per file
  IV_Features_csv:           ~1-5 KB (few samples)
  IV_Results:                ~5-10 KB (annotated)

SLIM:
  Similar structure, ~2x file size
  
SteppedField:
  Similar structure, ~3x file size
```

## Reproducibility

### Expected Results

Running IMDASH on SingleField test data should produce:

- Feature detection: 40-60 features per sample
- CCS annotation: >80% of features matched
- Retention time reproducibility: < 5% CV
- m/z accuracy: < 5 ppm
- CCS accuracy: < 2% difference from reference

### Method Parameters

Key parameters documented in software metadata:

```csv
# From SofwareTools-and-Params.csv
Tool,Version,KeyParameter,Value
ProteoWizard,3.0.20175,--mzML,yes
ProteoWizard,3.0.20175,--64,yes
MZmine,2.53,MassAccuracy,0.01
MZmine,2.53,RtTolerance,0.5
AutoCCS,2.0,CalibrationMixture,TuneMix
AutoCCS,2.0,FieldType,Single
```

### Reproducibility Checklist

- [ ] Software versions match documentation
- [ ] Configuration XML files unchanged from provided templates
- [ ] Calibrant reference file matches experimental setup
- [ ] Input data directories accessible
- [ ] Output directories have write permissions
- [ ] Expected feature counts within reasonable range

## Integration with CI/CD

### Automated Testing

Test data enables CI/CD pipeline integration:

```yaml
# Example: GitLab CI pipeline
test_single_field:
  script:
    - python CLI/CLI.py -j test-data/SingleField/sample.json
    - python tests/validate_output.py test-data/SingleField/IV_Results
  artifacts:
    paths:
      - results/

test_slim:
  script:
    - python CLI/CLI.py -j test-data/SLIM/sample.json
    - python tests/validate_output.py test-data/SLIM/IV_Results
```

### Expected Artifacts

- Feature CSV files with consistent column structure
- Annotation results with >80% success rate
- Timing logs for performance validation
- Log files showing no critical errors

## Large File Management

### Data Not Included in Repository

Raw .d files and large mzML files are too large for Git:

```bash
# To obtain full test data:
1. Document requested on project wiki/issue tracker
2. Download from shared storage (specify location)
3. Extract to test-data subdirectory
4. Verify with: ls -R test-data/SingleField/I_Raw
```

### Minimal Test Set Included

Repository includes sufficient files for:
- Configuration validation
- Workflow path verification
- Tool integration testing
- Parameter documentation review

### Adding Your Own Data

```bash
# To use your own test data:
1. Create directory: test-data/MyExperiment/
2. Copy configuration files from SingleField template
3. Place your raw/mzML data in appropriate subdirectories
4. Update configuration files with your parameters
5. Run workflow as documented above
```

## Notes

- Test datasets are provided "as-is" for IMDASH validation
- Results may vary with different software versions
- Calibrant reference files are for Agilent TuneMix only (change if using different calibrant)
- Large files (.d directories) should be handled separately due to repository size constraints
- Configuration XML files can be customized for different instruments/parameters
