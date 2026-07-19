# simple-empirical-Scons-demo

A minimal SCons-based empirical research pipeline demonstrating a four-step workflow: data import, data cleaning, regression analysis, and LaTeX paper compilation. Uses plain SCons `Command()` — no gslab_scons builders.

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
4.build-paper-and-slides/
```

### Step folders — start with a verb

The name after the numeric prefix should begin with a **verb** describing
the action performed by that step, followed by a noun or object:

```
good:  1.import-data          ← verb "import" + object "data"
good:  2.clean-data           ← verb "clean" + object "data"
good:  4.build-paper-and-slides  ← verb "build" + object "paper-and-slides"
bad:   3.regression-analysis  ← "regression" is a noun, not a verb
```

The verb makes the step's role immediately clear: what does this step
*do*? Import, clean, build, merge, plot, etc.

---

## Folder Structure

```
simple-empirical-Scons-demo/
├── README.md
├── SConstruct                          ← top-level SCons entry point
├── modules/
│   └── scons_log.py                    ← logging helper (timestamps + Sconstruct.log merge)
├── Sconstruct.log                      ← top-level build log (generated, gitignored)
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
    ├── output/                         ← regression_results.tex and tables land here
    └── temp/                           ← logs for this step

└── 4.build-paper-and-slides/
    ├── SConscript                      ← SCons rules for this step
    ├── code/
    │   ├── paper.tex                   ← LaTeX paper that \input{}s regression results
    │   └── build_paper_and_slides.py   ← Python wrapper: 2-pass pdflatex compilation
    ├── input-data/                     ← copied from 3.regression-analysis/output/
    ├── output/                         ← paper.pdf and LaTeX auxiliary files land here
    └── temp/                           ← logs for this step
```

---

## Subdirectory Rules

| Subdir | Purpose | Present in step |
|--------|---------|-----------------|
| `code/` | Scripts executed by SCons | All steps |
| `SConscript` | SCons build rules for this step | All steps |
| `raw-data/` | Data downloaded from online source | Step 1 only |
| `input-data/` | Input copied from previous step's output | Steps 2, 3 & 4 |
| `output/` | Processed/final data produced by this step | Steps 2, 3 & 4 |
| `temp/` | Build logs for this step | All steps |

---

## Pipeline Steps

| Step | Folder | Language | Input | Output |
|------|--------|----------|-------|--------|
| 1 | `1.import-data` | Python | online source | `raw-data/*.csv` |
| 2 | `2.clean-data` | Python | `input-data/` (from step 1 raw-data) | `output/*.csv` |
| 3 | `3.regression-analysis` | Stata | `input-data/` (from step 2 output) | `output/regression_results.tex` |
| 4 | `4.build-paper-and-slides` | LaTeX (Python wrapper) | `input-data/` (from step 3 output) + `code/paper.tex` | `output/paper.pdf` |

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
| `3.regression-analysis/code/regression_analysis.do` | Root | `'3.regression-analysis/input-data/clean_data.csv'`, `'3.regression-analysis/output/regression_results.tex'` |
| `4.build-paper-and-slides/code/build_paper_and_slides.py` | Step dir¹ | `'code/paper.tex'`, `'input-data/regression_results.tex'`, `'output/'` |

**Code Examples:**
```python
# 1.import-data/code/import_data.py
df.to_csv('1.import-data/raw-data/data.csv', index=False)  # ✓
load_dotenv(dotenv_path='.env')  # ✓ At root, not ../

# 2.clean-data/code/clean_data.py
df = pd.read_csv('2.clean-data/input-data/data.csv')  # ✓
df.to_csv('2.clean-data/output/clean_data.csv', index=False)  # ✓

# 4.build-paper-and-slides/code/build_paper_and_slides.py
# ¹ This wrapper changes its own working directory to the step dir
# so that \input{} paths in the .tex file resolve step-relatively.
# The SCons action still runs from ROOT, but the wrapper does:
#   os.chdir('4.build-paper-and-slides')
# This keeps .tex paths clean (input-data/... not 4.build-paper-and-slides/input-data/...)
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

**Alternative: Use `Path` and `__file__` for portable relative paths**

Instead of relying on root-relative paths in scripts, you can resolve paths relative to the script's location using `__file__` and `pathlib.Path`. This approach is more portable and works regardless of SCons working directory:

```python
# In 1.import-data/code/import_data.py
from pathlib import Path
from dotenv import load_dotenv
import pandas as pd

script_dir = Path(__file__).resolve().parent          # .../1.import-data/code/
root_dir = script_dir.parent.parent                  # .../simple-empirical-Scons-demo/

# Load .env from root
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

# Save output to root-relative path
output_path = root_dir / "1.import-data/raw-data/data.csv"
df.to_csv(output_path, index=False)
```

**Benefits of this approach:**
- Works regardless of SCons working directory
- More explicit — paths are clearly relative to the script location
- Easier to test scripts independently outside of SCons
- More portable if scripts are moved or reused elsewhere

---

## Logging

The pipeline produces two layers of logs, mirroring the gslab_scons approach
(`gslab_python/gslab_scons/builders/gslab_builder.py` for per-builder
timestamps, and `gslab_python/gslab_scons/log.py` for the top-level build log):

1. **Per-step logs** — one per SConscript, capturing that step's script output
   with start/end timestamps.
2. **Top-level `Sconstruct.log`** — records the overall SCons build process:
   a "New build" start line, the merged per-step logs, and a "Build completed"
   end line.

### File naming and location

| Log | Path | Produced by |
|-----|------|-------------|
| Step 1 | `1.import-data/temp/Sconscript_import_data.log` | SConscript action |
| Step 2 | `2.clean-data/temp/Sconscript_clean_data.log` | SConscript action |
| Step 3 | `3.regression-analysis/temp/Sconscript_regression_analysis.log` | Stata `log using` in the `.do` file |
| Step 4 | `4.build-paper-and-slides/temp/Sconscript_build_paper_and_slides.log` | SConscript action (shell redirection) |
| Top-level | `Sconstruct.log` (project root) | `SConstruct` (parse time + `atexit`) |

**Naming convention:** `Sconscript_<step_name>.log`, where `<step_name>` is the
step folder's suffix with hyphens replaced by underscores
(`import-data` → `import_data`). All step logs live in that step's `temp/`
folder; the top-level log lives next to `SConstruct`.

All logs are build artifacts — `*/temp/` and `*.log` are gitignored, so they
are never committed.

### Timestamp convention

Every log uses the gslab `{YYYY-MM-DD HH:MM:SS}` timestamp format so that
`Sconstruct.log`'s merge step can identify them uniformly, just as
`gslab_scons/log.py` does:

```
*** Builder log created: {2026-07-19 17:29:03}
<script output>
*** Builder log completed: {2026-07-19 17:29:05}
```

### How Python steps log (shell redirection)

Python steps redirect the script's stdout/stderr into the log with `>`/`>>`
inside the `env.Command()` action, and bracket it with start/end timestamp
calls to the `modules/scons_log.py` helper:

```python
# In 1.import-data/SConscript (action runs from project ROOT)
LOG = '1.import-data/temp/Sconscript_import_data.log'
cmd = env.Command(
    target='raw-data/data.csv',
    source='code/import_data.py',
    action='python modules/scons_log.py start %s && '
           'python $SOURCE >> %s 2>&1 && '
           'python modules/scons_log.py end %s' % (LOG, LOG, LOG)
)
```

- `scons_log.py start <log>` — truncates the log and writes the `created` line.
- `python $SOURCE >> <log> 2>&1` — appends the script's stdout **and** stderr.
- `scons_log.py end <log>` — appends the `completed` line.
- `&&` chains the three so that if the script fails, the `completed` line is
  skipped (a log with a `created` line but no `completed` line signals a
  failed step). `&&`, `>>`, and `2>&1` are all supported by SCons's default
  Windows shell (`cmd.exe`).

> Note on timestamps: we deliberately use a Python helper (`datetime.now()`)
> rather than shell `$(date ...)`. SCons on Windows executes actions via
> `cmd.exe`, which does not support Bash command substitution.

### How the Stata step logs (Stata's inherent `log` command)

The Stata step uses Stata's own `log using` command inside the `.do` file —
**no shell redirection**. Start/end timestamps are emitted with `display` so
they appear in the captured log:

```stata
* Build a YYYY-MM-DD HH:MM:SS timestamp string (gslab convention)
local _sd = date(c(current_date), "DMY")
local _ts_start = string(year(`_sd'), "%04.0f") + "-" ///
    + string(month(`_sd'), "%02.0f") + "-" ///
    + string(day(`_sd'), "%02.0f") + " " + c(current_time)
log using "3.regression-analysis/temp/Sconscript_regression_analysis.log", replace text
display "*** Builder log created: {`_ts_start'}"

* ...analysis...

display "*** Builder log completed: {`_ts_end'}"
log close
```

Stata runs from the project ROOT (inherited from the SCons action), so the
`log using` path is root-relative. Stata also auto-creates a side-effect
`regression_analysis.log` (from `-e do`) at the root — this is gitignored and
harmless; the canonical log is the named `Sconscript_*.log`.

### How the LaTeX step logs (Python wrapper + shell redirection)

Step 4 uses the same shell-redirection pattern as Python steps 1–2, but
the action invokes a Python wrapper script (`build_paper_and_slides.py`)
instead of a data-processing script:

```python
# In 4.build-paper-and-slides/SConscript (action runs from project ROOT)
LOG = '4.build-paper-and-slides/temp/Sconscript_build_paper_and_slides.log'
cmd = env.Command(
    target='output/paper.pdf',
    source=['code/paper.tex', 'code/build_paper_and_slides.py', 'input-data/regression_results.tex'],
    action='python modules/scons_log.py start %s && '
           'python 4.build-paper-and-slides/code/build_paper_and_slides.py >> %s 2>&1 && '
           'python modules/scons_log.py end %s' % (LOG, LOG, LOG)
)
```

**Key differences from Python data-processing steps:**

1. **Working directory** — The wrapper calls `os.chdir('4.build-paper-and-slides')`
   so that `\input{input-data/regression_results}` in `paper.tex` resolves
   relative to the step directory (not the project root). This keeps `.tex`
   paths clean and step-relative.

2. **2-pass compilation** — The wrapper runs pdflatex twice:
   - Pass 1: generates `.aux` (cross-reference data) and `.toc` (table of contents)
   - Pass 2: reads `.aux` and `.toc` to resolve `\ref{}`, `\tableofcontents`, etc.

3. **Windows path handling** — pdflatex on Windows rejects backslash paths.
   The wrapper converts the output directory to forward slashes via
   `output_dir.replace('\\', '/')`, matching the pattern from the `Scons-Test`
   reference project.

4. **Dependency tracking** — The `source` list includes `paper.tex`, the wrapper
   script, AND `input-data/regression_results.tex`. This ensures the PDF is
   rebuilt if the paper source, build logic, or upstream regression output changes.

The `&&` chaining ensures that if pdflatex fails (non-zero exit), the
`completed` timestamp is never written — a log with `created` but no
`completed` signals a failed step.

### Top-level `Sconstruct.log`

`SConstruct` records the overall build process, mirroring
`gslab_scons/log.py`'s `start_log` / `end_log`:

- **Parse time** — writes `*** New build: {time} ***` to `Sconstruct.log`
  before any build action runs.
- **`atexit` handler** — after the build completes, appends each step log
  (separated by a header with the step-log path) and writes
  `*** Build completed: {time} ***`.
- **Dry-run guard** — when SCons is invoked with `-n` / `--dry-run` /
  `--recon` / `--just-print`, no log is written (mirrors
  `log.py`'s `is_scons_dry_run`).

The helper is imported in-process at parse time. Because `scons_log.py` lives
in `modules/` (not a package, not on `sys.path`), `SConstruct` prepends that
folder to `sys.path` so the bare `import scons_log` resolves — this lets the
start line be written at parse time and the end line via `atexit`, without
spawning a subprocess. (The per-step SConscripts instead invoke it as a shell
script: `python modules/scons_log.py ...`.)
```python
sys.path.insert(0, os.path.join(os.getcwd(), 'modules'))
import scons_log
scons_log.sconstruct_start(SCONSTRUCT_LOG)         # parse time
atexit.register(lambda: scons_log.sconstruct_end(  # build end
    SCONSTRUCT_LOG, STEP_LOGS))
```

### The `modules/scons_log.py` helper

A small stdlib-only module providing four CLI subcommands:

| Command | Purpose |
|---------|---------|
| `start <log>` | Truncate `<log>`, write `*** Builder log created: {time}` |
| `end <log>` | Append `*** Builder log completed: {time}` |
| `sconstruct_start <log>` | Truncate `<log>`, write `*** New build: {time} ***` |
| `sconstruct_end <log> <step_log>...` | Merge step logs into `<log>`, then write `*** Build completed: {time} ***` |

Invoke from the project root as `python modules/scons_log.py <command> ...`
(SCons actions run from the root, so the relative path resolves correctly).

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

**Note:** The demo's SConscript uses `StataSE-64 /e do script.do`. Both `-e` and `/e` reach Stata correctly when spawned via cmd.exe (which is how SCons runs actions), so `/e` works in SCons. **Caveat:** do NOT type `StataSE-64 /e do ...` directly in Git Bash / MSYS — MSYS auto-translates the leading `/e` into a Windows path (`E:/`), so Stata never receives the batch flag and silently does nothing. For direct terminal use in Git Bash, use `-e do` (or prefix `MSYS_NO_PATHCONV=1`). Verified 2026-07-19.

**Do-File Template:** When creating `.do` files, use `dotemplatedo.do` as a template for consistent structure, metadata headers, and section organization.

---

## Development Setup

### Running Jupyter Notebook with Venv in VS Code

1. **Prerequisites:** Install VS Code extension: Jupyter (official Microsoft extension)

2. **Activate venv:**
   ```bash
   # Windows
   .venv\Scripts\activate
   
   # Mac / Linux
   source .venv/bin/activate
   ```

3. **Install packages in venv:**
   ```bash
   pip install ipykernel jupyter notebook
   ```

4. **Select Python interpreter in VS Code:**
   - Press `Ctrl + Shift + P` (Windows/Linux) / `Cmd + Shift + P` (Mac)
   - Search: `Python: Select Interpreter`
   - Pick the python binary inside `.venv\Scripts\python.exe` (Windows) or `.venv/bin/python` (Mac/Linux)

5. **Create or open `.ipynb` notebook file:**
   - VS Code auto-detects the selected venv as the notebook kernel
   - If wrong kernel loads: Click kernel name (top right) → Select another kernel → Choose your venv kernel

### How to manually register kernel (if VS Code cannot find env)

Run this command inside activated virtual env:
```bash
python -m ipykernel install --user --name scons_demo_env --display-name "SCons Demo Virtual Env"
```

Restart VS Code, then you can pick this kernel in notebook kernel list.
