# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is the GSLab Python library repository combined with a template for reproducible research projects. The repository has two main components:

- **`gslab_python/`** — The GSLab Python library (packages for reproducible research workflows)
- **`template/`** — A sample GSLab project demonstrating the build system and directory structure

## Quick Commands

### Testing the gslab_python library

```bash
# Run all tests with coverage report
cd gslab_python
python setup.py test

# Run tests with coverage for specific files
cd gslab_python
python setup.py test --include=gslab_scons/*
```

### Building the template project

```bash
# Build analysis pipeline
cd template/analysis
python run.py

# Build paper/slides
cd template/paper_slides
python run.py

# Build specific target
cd template/analysis
python run.py build/path/to/file.txt

# Build with SCons caching (faster subsequent runs)
python run.py mode=cache
```

### Setting up the template

```bash
# Install dependencies
cd template
pip install -r config/requirements.txt

# Unzip SCons (one-time setup)
cd template/config
unzip scons.zip -d scons  # Manual step on Windows
```

## Repository Structure

### gslab_python/

Core library packages providing builders and utilities for SCons-based research workflows:

- **`gslab_make/`** — File management utilities (`make_links.py`, `make_log.py`) and external dependency tools
- **`gslab_fill/`** — Template filling for text and table files (`textfill.py`, `tablefill.py`)
- **`gslab_scons/`** — SCons integration:
  - `builders/` — Custom builders for Python, R, Stata, MATLAB, LyX, LaTeX, and shell commands
  - `release.py` — Release automation to GitHub and local destinations
  - `log.py`, `check_prereq.py` — Logging and prerequisite checking
- **`gslab_misc/`** — Miscellaneous utilities including `gencat` (concatenation tools) and `SaveData` modules

Testing uses `coverage` for unit tests. All packages define tests in subdirectories.

### template/

A minimal working example of a GSLab research project showing the recommended structure:

- **`analysis/`** — Data processing and statistical analysis
  - `source/` — Scripts (Python, R, Stata, MATLAB)
  - `build/` — Build artifacts (generated)
  - `release/` — Final outputs intended for release
  - `SConstruct` — Build definition
  - `run.py` — Wrapper around SCons
  
- **`paper_slides/`** — Paper and presentation generation (same structure as `analysis/`)
  
- **`config/`** — Shared configuration
  - `config_global.yaml` — Versioned config (gslab_python version, paths)
  - `config_user.yaml` — Local unversioned config (executables, cache paths) — auto-generated
  - `scons/` — Packaged SCons (scons-local-3.0.1)
  - `requirements.txt` — Python dependencies
  - `config_r.r`, `config_stata.do` — Language-specific setup

## Build System Architecture

### SCons Integration (gslab_scons)

The core build system uses SCons with custom builders. Understanding the flow:

1. **`run.py`** in analysis/ or paper_slides/ calls `config/scons/scons.py` (SCons Local)
2. **SConstruct** in each subdirectory defines the build environment and includes language-specific builders
3. **SConscript** files in each source/ subdirectory define build rules for individual targets
4. **Builders** (in gslab_scons/builders/) execute scripts and track dependencies
5. **Logging** — Each builder produces a log; all are merged to `release/sconstruct.log`
6. **MD5-timestamp decider** — Rebuilds only when content changes, not timestamps

### Supported Languages

Each builder is optional (uncomment in SConstruct to enable):
- Python via `BuildPython`
- R via `BuildR`
- Stata via `BuildStata`
- MATLAB via `BuildMatlab`
- LyX → PDF via `BuildLyx` (paper_slides)
- LaTeX → PDF via `BuildLatex`
- Arbitrary shell commands via "Anything builder"

### Configuration System

Two YAML files control the build:

- **`config_global.yaml`** (versioned) — gslab_python version, source/build paths, input directories to monitor, prerequisite checks
- **`config_user.yaml`** (local, unversioned) — Executable paths (python_executable, r_executable, stata_executable, latex_executable), SCons cache directory, release directory

If `config_user.yaml` is missing, SCons will copy from template on first run.

## Key Architecture Patterns

### Dependency coupling (analysis → paper_slides)

By design, `analysis/` and `paper_slides/` are decoupled. To use analysis outputs as paper inputs:

1. Manually copy desired files from `analysis/release/` to `paper_slides/input/`
2. This allows coauthors to build papers without re-running expensive analysis

Lighter alternatives (not recommended):
- Symlinks between `analysis/release` and `paper_slides/input` (not portable)
- Point to `analysis/release` in `paper_slides/config_global.yaml` (hard to parse in LyX/LaTeX)

### Large files

- **Versioned:** Track with git-lfs (add to `.gitattributes`, list under `look_in` in config_global.yaml)
- **Unversioned in release:** Store in `release/lg/` (in .gitignore by default); included in local releases but not GitHub

### Logging and diagnostics

- **Build logs:** `release/sconstruct.log` concatenates all builder logs
- **Repository state:** `release/state_of_repo.log` tracks file sizes and git-lfs usage
- **Input monitoring:** `release/state_of_input.log` records contents of directories listed under `input` key

## Testing and Quality

### gslab_python testing

```bash
cd gslab_python
# Run all tests
python setup.py test

# Coverage report omits setup.py and __init__.py
# Output written to test.log
```

The `TestRepo` build command in setup.py runs `coverage run` with branch coverage enabled, then generates a report.

### Troubleshooting

**`config_user.yaml` not found** — SCons will auto-generate from template on first run.

**Executable not found** — Check:
1. Executable is installed and in PATH
2. Listed in `config_user.yaml` under `executable_names` (only if not in PATH)
3. `prereq_checks` enabled in config_global.yaml

**SCons cache stale** — Different SCons versions (≥ 2.5.0) have different cache formats. Delete cache directory and rebuild.

**Build fails with dependency issues** — Run with `python run.py --debug` for full traceback. Verify all source files exist and SConscript rules are correct.

## Fixing Bugs in gslab_python

The `gslab_python/` directory is a git repo pointed at **your fork**:
- Remote: `https://github.com/andyzhou66/gslab_python.git`
- The template pulls from this fork via `template/config/requirements.txt`

**Workflow for fixing bugs or issues:**

1. Edit the relevant `.py` file(s) inside `gslab_python/` (e.g. `gslab_scons/builders/`, `gslab_fill/`, etc.)
2. Commit and push to `andyzhou66/gslab_python` on GitHub
3. Reinstall the updated package in the active venv:
   ```bash
   pip install --upgrade git+https://github.com/andyzhou66/gslab_python.git@master
   ```
4. Rebuild the template to verify the fix:
   ```bash
   cd template/analysis && python run.py
   ```

## Environment Notes

- **Venv location:** `.env/` (activate: `.env/Scripts/activate`). Root-level `Include/`, `Lib/`, `Scripts/` were removed.
- **WebFetch:** Requires `"skipWebFetchPreflight": true` in `.claude/settings.local.json` — without it, fetches hang indefinitely on external URLs.
- **Nested repos:** `gslab_python/` and `template/` are independent git repos, both gitignored from the main repo. Do not `git add` them.
- **Stata:** StataNow19 installed at `/g/StataNow19/StataSE-64.exe`. Use `-e do` syntax (not `/e do`) for command-line execution. Example: `StataSE-64 -e do script.do`. When writing `.do` files, use `simple-empirical-Scons-demo/dotemplatedo.do` as template for consistent structure and metadata.
- **Jupyter Notebooks:** Use `nbautoexport` to auto-export notebooks to Python `.py` files for cleaner git diffs and version control. Install: `pip install nbautoexport`. Configure in JupyterLab (Settings → Notebook → Auto Export) or via `.jupyterlab-settings/notebook.json`. Exported `.py` files track notebook logic while the `.ipynb` remains readable in Jupyter.

### Running Jupyter Notebook with Venv in VS Code

1. **Prerequisites:** Install VS Code extension: Jupyter (official Microsoft extension)
2. **Activate venv:** `.env\Scripts\activate` (Windows) or `source .env/bin/activate` (Mac/Linux)
3. **Install packages in venv:**
   ```bash
   pip install ipykernel jupyter notebook
   ```
4. **Select Python interpreter in VS Code:**
   - Press `Ctrl + Shift + P` (Windows/Linux) / `Cmd + Shift + P` (Mac)
   - Search: `Python: Select Interpreter`
   - Pick the python binary inside `.env\Scripts\python.exe` (Windows) or `.env/bin/python` (Mac/Linux)
5. **Create or open `.ipynb` notebook file:**
   - VS Code auto-detects the selected venv as the notebook kernel
   - If wrong kernel loads: Click kernel name (top right) → Select another kernel → Choose your `.env` kernel

### How to manually register kernel (if VS Code cannot find env)

Run this command inside activated virtual env:
```bash
python -m ipykernel install --user --name gslab_env --display-name "GSLab Virtual Env"
```

Restart VS Code, then you can pick this kernel in notebook kernel list.

## Project Conventions (simple-empirical-Scons-demo)

- Folders: hyphen-case (`import-data`); Files: underscore_case (`import_data.py`)
- Step folders: numeric prefix + dot (`1.import-data/`, `2.clean-data/`, `3.regression-analysis/`)
- Build system: plain SCons `Command()`, not `gslab_scons` builders
- Each step folder contains: `SConscript`, `code/`, `temp/` (logs)
- Step 1 (`1.import-data`): also has `raw-data/` (downloaded CSVs)
- Steps 2–3: also have `input-data/` (copied from prior step) and `output/` (produced files)

### SCons Pattern: `env.Install()` for Inter-Step Data Flows

Each step's **SConscript** uses `env.Install()` to explicitly copy its outputs to the next step's `input-data/` directory. This makes the pipeline dependency graph transparent to SCons.

**🚨 CRITICAL: Working Directory in env.Command()**

When SCons executes `env.Command()`, **the action runs from the ROOT directory** (simple-empirical-Scons-demo/), NOT from the step directory.

```python
# In 1.import-data/SConscript
cmd = env.Command(
    target='raw-data/data.csv',
    source='code/import_data.py',
    action='python $SOURCE'  # Working directory: simple-empirical-Scons-demo/
)
```

**All relative paths in Python/Stata scripts must be relative to ROOT:**
- `1.import-data/raw-data/data.csv` ✓ (NOT `raw-data/data.csv`)
- `2.clean-data/input-data/data.csv` ✓ (NOT `input-data/data.csv`)
- `3.regression-analysis/output/regression_results.txt` ✓ (NOT `output/regression_results.txt`)
- `.env` ✓ (NOT `../.env`)

**Example from `1.import-data/SConscript`:**
```python
# Build: execute import_data.py → output/data.csv
cmd = env.Command(
    target='raw-data/data.csv',
    source='code/import_data.py',
    action='python $SOURCE'
)

# Install: copy to next step's input
env.Install('../2.clean-data/input-data', 'raw-data/data.csv')
```

**Alternative: Use `Path` and `__file__` for portable relative paths**

Instead of hardcoding root-relative paths, you can resolve paths relative to the script's location using `__file__` and Python's `pathlib.Path`. This is more portable and doesn't depend on SCons working directory:

```python
# In 1.import-data/code/import_data.py
from pathlib import Path

script_dir = Path(__file__).resolve().parent          # .../1.import-data/code/
root_dir = script_dir.parent.parent                  # .../simple-empirical-Scons-demo/
output_path = root_dir / "1.import-data/raw-data/data.csv"

df.to_csv(output_path, index=False)
```

**Benefits of this approach:**
- Works regardless of SCons working directory
- More explicit — intent is clear from the code
- Easier to test scripts independently outside of SCons
- More portable if scripts are moved to different locations

**Benefits:**
- SCons manages build order and file tracking automatically
- Each step "owns" its output distribution (scalable to N steps)
- No manual copying or pre-action hooks in the root SConstruct
- Clear, verifiable data lineage in the code

### Version Control Rules

**`.gitignore`** — Ignores build artifacts and temporary files:
- `*/output/`, `*/input-data/`, `*/temp/` — regenerated by SCons
- `*.log` — Stata side-effect logs
- `*.pyc`, `*.sconsign.dblite` — SCons/Python caches
- `.env` — environment variables with API keys (secrets)

**`.gitattributes`** — Routes large files to Git LFS:
- `*.csv`, `*.dta` — data files
- `*.pdf`, `*.png` — output images
- `*.zip` — archives

This keeps source code tracked while ensuring large data files use Git LFS for efficient storage and transfer.

### Sensitive Data with python-dotenv

The pipeline uses `python-dotenv` to manage API keys and other secrets:

1. **`.env.example`** — Template (committed to repo, contains placeholders)
2. **`.env`** — Local secrets file (gitignored, never committed)

Users copy `.env.example` to `.env` and fill in their actual credentials. At runtime, scripts load via:
```python
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path='../../.env')
API_KEY = os.getenv('API_KEY')
```

**Best practice:** Never hardcode credentials in scripts. Always use environment variables via `.env` for local development and CI/CD env vars for production.

## References

- [Your gslab_python fork](https://github.com/andyzhou66/gslab_python)
- [SCons documentation](http://scons.org/)
- [GSLab RA Manual](https://github.com/gslab-econ/ra-manual/wiki)
- [Original template repository](https://github.com/gslab-econ/template)
