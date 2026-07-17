# simple-empirical-Scons-demo

A minimal SCons-based empirical research pipeline demonstrating a three-step workflow: data import, data cleaning, and regression analysis. Uses plain SCons `Command()` — no gslab_scons builders.

---

## Naming Conventions

### Folders — use hyphens

```
good:  import-data
good:  clean-data
good:  regression-analysis
bad:   importData
bad:   import_data
```

### Files — use underscores

```
good:  import_data.py
good:  clean_data.py
good:  regression_analysis.do
bad:   import-data.py
bad:   importData.py
```

### Step folders — prefix with sequential number and dot

Each pipeline step is a top-level folder prefixed by its execution order:

```
1.import-data/
2.clean-data/
3.regression-analysis/
```

---

## Folder Structure

```
simple-empirical-Scons-demo/
├── README.md
├── SConstruct                          ← top-level SCons entry point
│
├── 1.import-data/
│   ├── SConscript                      ← SCons rules for this step
│   ├── code/
│   │   └── import_data.py              ← downloads / imports raw data
│   ├── raw-data/                       ← downloaded CSV files land here
│   └── temp/                           ← logs for this step
│
├── 2.clean-data/
│   ├── SConscript
│   ├── code/
│   │   └── clean_data.py               ← cleans and processes data
│   ├── input-data/                     ← copied from 1.import-data/raw-data/
│   ├── output/                         ← cleaned CSV files land here
│   └── temp/                           ← logs for this step
│
└── 3.regression-analysis/
    ├── SConscript
    ├── code/
    │   └── regression_analysis.do      ← Stata regression script
    ├── input-data/                     ← copied from 2.clean-data/output/
    ├── output/                         ← results.txt and tables land here
    └── temp/                           ← logs for this step
```

---

## Subdirectory Rules

| Subdir | Purpose | Present in step |
|--------|---------|-----------------|
| `code/` | Scripts executed by SCons | All steps |
| `SConscript` | SCons build rules for this step | All steps |
| `raw-data/` | Data downloaded from online source | Step 1 only |
| `input-data/` | Input copied from previous step's output | Steps 2 & 3 |
| `output/` | Processed/final data produced by this step | Steps 2 & 3 |
| `temp/` | Build logs for this step | All steps |

---

## Pipeline Steps

| Step | Folder | Language | Input | Output |
|------|--------|----------|-------|--------|
| 1 | `1.import-data` | Python | online source | `raw-data/*.csv` |
| 2 | `2.clean-data` | Python | `input-data/` (from step 1 raw-data) | `output/*.csv` |
| 3 | `3.regression-analysis` | Stata | `input-data/` (from step 2 output) | `output/results.txt` |

---

## SCons Build System

### Design Pattern: `env.Install()` for Inter-Step Dependencies

Each step's **SConscript** uses `env.Install()` to copy its outputs to the next step's `input-data/` directory. This makes the pipeline dependency graph explicit in SCons.

**Example from `1.import-data/SConscript`:**

```python
# Build rule: execute import_data.py to produce output/data.csv
cmd = env.Command(
    target='output/data.csv',
    source='code/import_data.py',
    action='python $SOURCE > $TARGET'
)

# Install output to next step's input directory
env.Install('../2.clean-data/input-data', 'output/data.csv')
```

**Important: Working Directory in SCons Commands**

When SCons executes `env.Command()`, scripts run from the **step directory** (where SConscript is located), NOT from the `code/` subdirectory. Therefore:

| File Path | Working Directory | Correct Path |
|-----------|-------------------|--------------|
| `input-data/` | step dir | `input-data/` (NOT `../input-data/`) |
| `output/` | step dir | `output/` (NOT `../output/`) |
| `raw-data/` | step dir | `raw-data/` (NOT `../raw-data/`) |
| `.env` | step dir | `../.env` (one level up to project root) |

**Example in Python script (import_data.py):**
```python
# CORRECT: paths relative to step directory
df.to_csv('output/data.csv', index=False)  # ✓
load_dotenv(dotenv_path='../.env')         # ✓

# WRONG: paths relative to code/ directory  
df.to_csv('../output/data.csv', index=False)  # ✗
load_dotenv(dotenv_path='../../.env')         # ✗
```

**Why this pattern?**

1. **Explicit dependencies** — SCons automatically manages the build order and file transfers
2. **Clean separation** — Each step "owns" its output and decides where to send it
3. **Scalable** — Adding steps requires only updating the SConscript, not the root SConstruct
4. **Verifiable** — SCons tracks which files are needed, not manual copying

**Root SConstruct** simply includes all step SConscripts in order:

```python
env = Environment()
SConscript('1.import-data/SConscript', exports='env')
SConscript('2.clean-data/SConscript', exports='env')
SConscript('3.regression-analysis/SConscript', exports='env')
```

---

## Version Control (.gitignore and .gitattributes)

### .gitignore — What NOT to track

The repository ignores generated and temporary files:

| Pattern | Reason |
|---------|--------|
| `*/temp/` | Build logs and temporary files |
| `*/input-data/` | Copied from prior step's output; regenerated by SCons |
| `*/output/` | Build artifacts; regenerated by SCons |
| `*.log` | Stata side-effect logs (e.g., `regression_analysis.log`) |
| `*.pyc`, `*.sconsign.dblite` | SCons and Python caches |
| `*.aux`, `*.toc`, `*.nav` | LaTeX build artifacts (if present) |

**What IS tracked:**
- `*/code/` — all scripts (`.py`, `.do`)
- `*/SConscript` — build rules
- `SConstruct` — root build file
- `*/raw-data/` — raw source data (use LFS for large files)
- `README.md`, `.gitattributes`, `.gitignore`

### .gitattributes — Large files via Git LFS

These file types are stored on Git LFS (not in the main repository):

```
*.csv       ← data files
*.dta       ← Stata datasets
*.pdf       ← output PDFs
*.png       ← output images
*.zip       ← archives
```

This keeps the repository lean while preserving full version history for large files.

---

## How to Build

### Setup: Configure API Key

Before building, set up your API key:

```bash
# Copy the template
cp .env.example .env

# Edit .env with your actual API key
nano .env
```

The `.env` file is gitignored and will never be committed to GitHub.

### Run the Pipeline

```bash
cd simple-empirical-Scons-demo
scons
```

### Stata Configuration

If running Stata scripts directly (outside SCons), use the `-e do` syntax:

```bash
StataSE-64 -e do path/to/script.do
```

**Note:** The gslab_python builder specifies `/e do` for Windows, but StataNow19 requires `-e do` (hyphen, not forward slash).

---

## Sensitive Data Management

### API Keys and Secrets

Step 1 (`import_data.py`) loads API keys via `python-dotenv`:

1. **`.env.example`** (committed) — Template showing required variables
2. **`.env`** (gitignored) — Local file with your actual API key

**Workflow:**
```bash
# Create your local .env from the template
cp .env.example .env

# Edit .env with your actual credentials
nano .env
```

The `.env` file is in `.gitignore` and will never be pushed to GitHub.

**In code:** API key is loaded at runtime:
```python
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='../../.env')
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise EnvironmentError("API_KEY not set. Copy .env.example to .env and fill in your key.")
```

---
