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

## How to Build

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
