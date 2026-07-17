# simple-empirical-Scons-demo

A minimal SCons-based empirical research pipeline demonstrating a three-step workflow: data import, data cleaning, and regression analysis.

---

## Naming Conventions

### Folders — use hyphens

All folder names use lowercase words separated by hyphens.

```
good:  import-data
good:  clean-data
good:  regression-analysis
bad:   importData
bad:   import_data
```

### Files — use underscores

All file names use lowercase words separated by underscores.

```
good:  import_data.py
good:  clean_data.py
good:  regression_analysis.do
bad:   import-data.py
bad:   importData.py
```

### Step folders — prefix with sequential number and dot

Each pipeline step folder begins with a number followed by a dot, making the execution order immediately visible.

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
├── SConstruct
├── source/
│   ├── 1.import-data/
│   │   └── import_data.py
│   ├── 2.clean-data/
│   │   └── clean_data.py
│   └── 3.regression-analysis/
│       └── regression_analysis.do
└── build/
    ├── 1.import-data/
    │   └── raw_data.csv
    ├── 2.clean-data/
    │   └── clean_data.csv
    └── 3.regression-analysis/
        └── results.txt
```

---

## Pipeline Steps

| Step | Folder | Language | Input | Output |
|------|--------|----------|-------|--------|
| 1 | `1.import-data` | Python | — | `raw_data.csv` |
| 2 | `2.clean-data` | Python | `raw_data.csv` | `clean_data.csv` |
| 3 | `3.regression-analysis` | Stata | `clean_data.csv` | `results.txt` |

---

## How to Build

```bash
cd simple-empirical-Scons-demo
scons
```
