# GSLab Template with Stata

This template has been modified to use **Stata** for data generation and descriptive analysis instead of Python.

## What's Changed

### Data Generation (`analysis/source/prepare_data/create_data.do`)
- Generates 10,000 observations with:
  - `id`: Sequential ID (1 to 10,000)
  - `age`: Random values between 20 and 65
  - `income`: Random values between $30,000 and $100,000
  - `education_years`: Random values between 8 and 21 years
- Saves to `build/prepare_data/data.txt`

### Descriptive Analysis (`analysis/source/descriptive/descriptive.do`)
- Calculates summary statistics for age, income, and education
- Saves summary statistics to `build/descriptive/summary.txt`
- Calculates correlation matrix and saves to `build/descriptive/correlation.txt`

## Configuration

### 1. Update Stata Executable Path

Edit `analysis/config_user.yaml` and set your Stata executable:

```yaml
executable_names:
  stata: StataMP-64.exe    # or: stata-mp, stata, StataBE, etc.
```

**Common options by OS:**
- **Windows**: `StataMP-64.exe`, `StataMP.exe`, `StataIC.exe`, `StataBE.exe`
- **macOS**: `stata-mp`, `stata-ic`, `stata-se`
- **Linux**: `stata-mp`, `stata-ic`, `stata-se`

You can verify your Stata executable name by checking where Stata is installed or running `stata --version` in your terminal.

### 2. (Optional) Adjust Random Seed

To make results reproducible, add this to the top of each `.do` file:
```stata
set seed 12345
```

## Running the Build

**Using the virtual environment:**

```bash
# Activate the venv
venv-gslab-template\Scripts\activate.bat

# Navigate to analysis
cd venv-gslab-template\template\analysis

# Run SCons
python run.py
```

Or use scons directly:
```bash
..\Scripts\scons.exe
```

**Or double-click the batch file:**
```
RUN_WITH_VENV.bat
```

## Build Outputs

After running the build, you'll find:

- **Data**: `analysis/build/prepare_data/data.txt` — The generated dataset
- **Summary Statistics**: `analysis/build/descriptive/summary.txt` — Summary statistics
- **Correlations**: `analysis/build/descriptive/correlation.txt` — Correlation matrix
- **Release**: `analysis/release/` — Copies of all final outputs
- **Build Log**: `analysis/release/sconstruct.log` — Details of the build process

## Next Steps

### Modify the Data Generation Script
Edit `analysis/source/prepare_data/create_data.do` to:
- Change the number of observations: `set obs 10000`
- Add new variables
- Import real data files

### Modify the Analysis Script
Edit `analysis/source/descriptive/descriptive.do` to:
- Add regression analysis
- Create plots
- Perform hypothesis tests
- Generate tables for the paper

### Add More Analysis Steps
Create additional `.do` files in `analysis/source/` and add corresponding entries to the SConscript files to expand your analysis pipeline.

## Troubleshooting

**Error: "Cannot find executable for stata"**
- Verify Stata is installed and in your PATH
- Check the executable name in `config_user.yaml`
- Try specifying the full path: `C:\Program Files\Stata17\StataMP-64.exe`

**Error: "invalid mode: 'rU'"**
- This is a Python 3 compatibility issue in template files
- Already fixed in this setup

**Build fails but no error message**
- Check the log files: `analysis/release/sconstruct.log`
- Check the individual step logs: `analysis/build/*/sconscript_*.log`

## SCons Basics

- `python run.py` — Build everything that's changed
- `python run.py -c` — Clean (remove all build artifacts)
- `python run.py --debug` — Show detailed error messages
- `python run.py mode=cache` — Use caching for faster rebuilds

See CLAUDE.md for more details on the SCons build system.
