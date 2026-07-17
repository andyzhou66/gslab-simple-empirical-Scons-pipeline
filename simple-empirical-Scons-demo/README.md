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

### 🚨 Critical: Working Directory for env.Command()

When SCons executes `env.Command()`, **the action runs from the root directory** (simple-empirical-Scons-demo/), NOT from the step directory.

**Example:**
```python
# In 1.import-data/SConscript
cmd = env.Command(
    target='raw-data/data.csv',
    source='code/import_data.py',
    action='python $SOURCE'  # Executes: python code/import_data.py
)
# Working directory: simple-empirical-Scons-demo/
```

**All paths in Python/Stata scripts must be relative to the root** (simple-empirical-Scons-demo/):

| Script Location | Working Dir | Correct Paths |
|---|---|---|
| `1.import-data/code/import_data.py` | Root | `'1.import-data/raw-data/data.csv'`, `'.env'` |
| `2.clean-data/code/clean_data.py` | Root | `'2.clean-data/input-data/data.csv'`, `'2.clean-data/output/clean_data.csv'` |
| `3.regression-analysis/code/regression_analysis.do` | Root | `'3.regression-analysis/input-data/clean_data.csv'`, `'3.regression-analysis/output/regression_results.txt'` |

**Code Examples:**
```python
# 1.import-data/code/import_data.py
df.to_csv('1.import-data/raw-data/data.csv', index=False)  # ✓
load_dotenv(dotenv_path='.env')  # ✓ At root, not ../

# 2.clean-data/code/clean_data.py
df = pd.read_csv('2.clean-data/input-data/data.csv')  # ✓
df.to_csv('2.clean-data/output/clean_data.csv', index=False)  # ✓
```

---

### Design Pattern: `env.Install()` for Inter-Step Dependencies

Each step's **SConscript** uses `env.Install()` to copy its outputs to the next step's `input-data/` directory.

**Example from `1.import-data/SConscript`:**

```python
cmd = env.Command(
    target='raw-data/data.csv',
    source='code/import_data.py',
    action='python $SOURCE'
)

# Install output to next step's input
env.Install('../2.clean-data/input-data', 'raw-data/data.csv')
```

**Benefits:**
1. Explicit dependencies — SCons manages build order automatically
2. Clean separation — Each step owns its output
3. Scalable — Adding steps only requires updating SConscript
4. Verifiable — SCons tracks all dependencies

---

## Version Control (.gitignore and .gitattributes)

### .gitignore — What NOT to track

The repository ignores generated and temporary files:

| Pattern | Reason |
|---------|--------|
| `*/temp/` | Build logs and temporary files |
| `*/input-data/` | Copied from prior step's output; regenerated by SCons |
| `*/output/` | Build artifacts; regenerated by SCons |
| `*.log` | Stata side-effect log files (e.g., regression_analysis.log in code/) |
| `*.pyc`, `*.sconsign.dblite` | SCons and Python caches |
| `*.aux, *.toc, *.nav, *.snm, *.fls, *.lot, *.lof, *.out` | LaTeX artifacts (if present) |
| `*.DS_Store` | macOS metadata |
| `.env` | Environment variables with API keys (secrets) |

**What IS tracked:**
- `*/code/` — all scripts (.py, .do)
- `*/SConscript` — per-step build rules
- `SConstruct` — root build file
- `*/raw-data/` — raw source data (in step 1 only)
- `README.md`, `.gitignore`, `.gitattributes`, `.env.example`

### .gitattributes — Large files via Git LFS

These file types are stored on Git LFS (not in the main repository):

```
*.csv       ← data files
*.dta       ← Stata datasets
*.pdf       ← output PDFs
*.png       ← output images
*.zip       ← archives
```

This keeps the repository lean while preserving version history for large files.

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

load_dotenv(dotenv_path='.env')  # Load from root directory
API_KEY = os.getenv('API_KEY')

if not API_KEY:
    raise EnvironmentError("API_KEY not set. Copy .env.example to .env and fill in your key.")
```

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
