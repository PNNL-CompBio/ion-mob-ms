# Post-hoc Scripts - Analysis Templates

## Overview

The `Post-hoc-scripts` directory contains R Markdown templates for downstream statistical analysis and visualization of IMDASH results. These scripts perform advanced analysis on annotated features, comparing experiments and extracting biological insights.

## Files

### Analysis Templates

- **`Single_vs_Stepped_Analysis_template.Rmd`** - Comparative workflow analysis
  - Compares ion mobility feature results between Single Field and Stepped Field experiments
  - Statistical analysis of separation improvements
  - Feature overlap and unique ion identification
  - CCS value precision comparison

- **`Target_file_list_creator.Rmd`** - Target list curation tool
  - Creates curated target ion lists from analysis results
  - Selects high-quality targets based on statistical criteria
  - Generates formats compatible with targeted analysis tools
  - Confidence-based filtering for next-round targeting

## Usage

### Opening and Running Templates

R Markdown files are designed for R Studio:

```bash
# Open in R Studio
open Single_vs_Stepped_Analysis_template.Rmd

# Or run from command line
R -e "rmarkdown::render('Single_vs_Stepped_Analysis_template.Rmd')"
```

### Interactive Execution

Processing templates support interactive analysis:

1. **Knit to HTML**: Generates self-contained HTML report
2. **Knit to PDF**: Creates publication-ready PDF
3. **Interactive Chunks**: Execute individual code blocks for exploration

### Batch Processing

For automated report generation:

```bash
# Process all Rmd files
for file in *.Rmd; do
  R -e "rmarkdown::render('$file')"
done

# Generate HTML and PDF versions
R -e "rmarkdown::render('template.Rmd', 'all')"
```

## Single vs. Stepped Field Comparison

### Template Purpose

This analysis compares results between standard Single Field and advanced Stepped Field ion mobility workflows:

**Questions Addressed**:
- Does stepped field provide better feature separation?
- How much improvement in CCS value precision?
- Which features only detected in stepped field?
- Are conclusions consistent across replicates?

### Data Requirements

**Input Files**:
- Annotated features CSV from Single Field workflow
- Annotated features CSV from Stepped Field workflow
- Experimental metadata for both workflows
- Optional: Raw intensity matrices for statistical testing

### Analysis Steps

1. **Data Loading and Validation**
   - Load feature tables from both workflows
   - Verify data integrity and column structure
   - Handle missing values appropriately

2. **Feature Matching**
   - Match features across workflows by m/z and retention time
   - Account for retention time shifting between methodologies
   - Identify workflow-unique features

3. **Statistical Comparison**
   - Compare CCS value precision (CV analysis)
   - Test for differences in feature intensity distributions
   - Evaluate separation improvement metrics

4. **Visualization**
   - Scatter plots: Single vs. Stepped CCS values
   - Distribution comparisons (histograms, boxplots)
   - Venn diagrams of detected features
   - ROC curves for detection improvement

5. **Report Generation**
   - Summary statistics table
   - Quality metrics comparison
   - Workflow recommendation based on results
   - References to methods and parameters

### Example Output

Generated report includes:

```
Analysis: Single Field vs. Stepped Field Ion Mobility Workflows
Generated: 2024-01-15

SUMMARY STATISTICS:
  Single Field:     450 features detected, 420 annotated (93%)
  Stepped Field:    520 features detected, 505 annotated (97%)
  
  Shared Features:  410 (91% overlap)
  Unique to SF:     10 features
  Unique to ST:     110 features (additional separation capability)

CCS VALUE PRECISION:
  Single Field: mean CV = 1.8%
  Stepped Field: mean CV = 0.9% (50% improvement)

RECOMMENDATION:
  Stepped Field provides significant separation improvement and
  higher precision CCS values. Recommended for complex samples.
```

## Target List Creator

### Template Purpose

This tool creates optimized target ion lists from analysis results for use in targeted analysis workflows:

**Workflow**:
1. Run untargeted IMDASH analysis (generates feature list)
2. Apply statistical filtering and confidence assessment
3. Create curated target list maximizing detection probability
4. Use targets in next analytical run (targeted mode)
5. Validate and refine for future iterations

### Target List Criteria

Selection based on:

- **Statistical Significance**:
  - Intensity above noise threshold
  - Consistent detection across replicates
  - Low coefficient of variation

- **Quality Metrics**:
  - CCS annotation confidence > threshold
  - Database match quality score
  - Peak shape quality (peak width, symmetry)

- **Prioritization**:
  - Known compounds (database matches) ranked first
  - Unknown but high-quality features (candidates)
  - Low-confidence features (research targets)

### Output Formats

Creates target lists compatible with:

- **Agilent MassHunter**: CSV import format with m/z, retention time, CCS
- **MZmine**: Import format for targeted analysis
- **IMDASH CLI**: JSON format for subsequent IMDASH runs
- **Custom**: User-specified format via templates

### Example Target List

```csv
mz,rt,ccs,priority,confidence,annotation,ion_form
123.456,10.5,120.5,HIGH,0.95,Leucine,M+H
234.567,12.3,145.2,HIGH,0.92,Isoleucine,M+H
345.678,15.2,167.3,MEDIUM,0.78,Unknown-C12H20,M+H
456.789,18.1,189.5,LOW,0.52,Candidate,M+Na
```

### Confidence Scoring

Confidence composite metric includes:

```
confidence = √(ppm_error² × ccs_error² × intensity_consistency²) / max_score
```

- **ppm_error**: Database match accuracy (lower better)
- **ccs_error**: CCS annotation precision (lower better)
- **intensity_consistency**: Replicability across samples (higher better)

## Customizing Templates

### Template Structure

R Markdown templates follow standard format:

```rmd
---
title: "Analysis Title"
author: "Your Name"
date: "`r Sys.Date()`"
output: html_document
---

# Section 1: Data Loading
[R code chunk]

# Section 2: Analysis
[R code chunk with visualization]

# Results
Summary and interpretation
```

### Adapting for Custom Data

1. **Modify data loading paths**:
   ```r
   sf_features <- read.csv("path/to/single_field_features.csv")
   st_features <- read.csv("path/to/stepped_field_features.csv")
   ```

2. **Update configuration parameters**:
   ```r
   CONFIDENCE_THRESHOLD <- 0.70  # Adjust based on requirements
   PPM_TOLERANCE <- 5             # Mass accuracy
   RT_TOLERANCE <- 0.2            # Retention time matching
   ```

3. **Customize filtering logic**:
   ```r
   # Filter features by custom criteria
   high_quality <- features %>%
     filter(intensity > 1000,
            annotation_confidence > 0.7,
            ppm_error < 5)
   ```

4. **Extend analysis sections**:
   - Add new statistical tests
   - Include additional visualizations
   - Incorporate external data sources
   - Create custom comparison metrics

## Required Packages

Templates require R packages:

```r
# Install required packages
install.packages(c("tidyverse", "rmarkdown", "ggplot2"))
install.packages("plotly")       # For interactive visualizations

# Load in template
library(tidyverse)
library(ggplot2)
library(rmarkdown)
```

## Output Products

### Generated Reports

By default, templates generate:

- **HTML Report**: Interactive, self-contained, browser-viewable
  ```bash
  Single_vs_Stepped_Analysis.html  # Full analysis with interactive plots
  ```

- **PDF Report**: Static format, suitable for printing/archival
  ```bash
  Single_vs_Stepped_Analysis.pdf   # Publication-ready tables and figures
  ```

### Accessory Outputs

Additional files created during processing:

- **CSV Tables**: Summary statistics exported to CSV
  ```bash
  comparison_statistics.csv
  target_list_final.csv
  ```

- **Plots**: High-resolution graphics (PNG, PDF)
  ```bash
  figures/scatter_ccs_comparison.png
  figures/feature_venn_diagram.pdf
  ```

### Saving Results

Within Rmd templates:

```r
# Export tables
write.csv(summary_stats, "output/comparison_summary.csv", row.names=FALSE)

# Save plots
ggsave("output/ccs_scatter.png", width=8, height=6)

# Archive report
file.copy("report.html", paste0("archive/report_", Sys.Date(), ".html"))
```

## Integration with IMDASH Workflow

### Data Pipeline

```
IMDASH CLI/GUI Analysis
    ↓ (generates annotated features)
Annotated Features CSV
    ↓ (input to post-hoc analysis)
R Markdown Template Processing
    ↓ (statistical analysis and visualization)
HTML/PDF Report + Target Lists
```

### Connecting Templates

1. **Run IMDASH** to completion
2. **Load results** in Single_vs_Stepped template
3. **Generate comparison report** (HTML/PDF)
4. **Review results** and select targets
5. **Run Target_list_creator** on high-quality features
6. **Export target lists** for next iteration

## Advanced Usage

### Batch Analysis Across Multiple Experiments

```r
# Process multiple experiment pairs
experiments <- list(
  c("SingleField_e1.csv", "SteppedField_e1.csv"),
  c("SingleField_e2.csv", "SteppedField_e2.csv"),
  c("SingleField_e3.csv", "SteppedField_e3.csv")
)

for (exp_pair in experiments) {
  # Load and analyze each pair
  # Generate individual reports
}
```

### Database Integration

Enhance annotations with external databases:

```r
# Query PubChem for additional compound info
library(rcdk)
compound_info <- get.formula.mass("C12H20O")

# Check against known metabolite databases
kegg_match <- query_kegg(mz_value, ppm_tolerance=5)

# Integrate into annotations
annotated_summary <- annotated %>%
  left_join(kegg_match, by="kegg_id")
```

### Custom Confidence Scoring

Implement domain-specific confidence calculations:

```r
# Weighted confidence combining multiple factors
calculate_confidence <- function(ppm_error, ccs_error, intensity_consistency, 
                                 database_match) {
  weights <- c(ppm=0.3, ccs=0.3, consistency=0.25, db=0.15)
  normalization <- c(5, 2, 0.2, 1)  # Domain-specific thresholds
  
  scores <- c(
    1 - ppm_error/weights["ppm"]/normalization["ppm"],
    1 - ccs_error/weights["ccs"]/normalization["ccs"],
    intensity_consistency/weights["consistency"]/normalization["consistency"],
    as.numeric(database_match)/weights["db"]/normalization["db"]
  )
  
  sum(pmin(scores, 1))  # Weighted sum, capped at 1.0
}
```

## Common Issues

### Issue: "Package 'tidyverse' not found"
- **Solution**: `install.packages("tidyverse")` before running

### Issue: "CSV file not found"
- **Solution**: Update file paths to match actual locations
- **Check**: Use absolute paths or `setwd()` to set working directory

### Issue: "Plots look incorrect/too small"
- **Solution**: Adjust figure dimensions in R chunk options
  ```r
  {r plot, fig.width=10, fig.height=8}
  ```

### Issue: "Report generation very slow"
- **Solution**: Cache expensive computations
  ```r
  {r expensive_calc, cache=TRUE}
  ```

## Notes

- Templates are starting points; customize for specific research questions
- Can be integrated into R Shiny apps for interactive analysis
- Automation scripts can run templates on schedule for monitoring studies
- Version control templates in Git for reproducibility and change tracking
- Documentation within templates explains each analysis step
