# gslab-simple-empirical-Scons-pipeline

This repository contains a small reproducible empirical research pipeline built with SCons. It demonstrates a four-step workflow that imports data, cleans it, runs a Stata regression, and compiles a LaTeX paper from the generated results.

## Repository layout

- `simple-empirical-Scons-demo/` — the working demo project
- `coding_guidelines4social_science.md` — notes on reproducible research practices
- `gslab_scons_architecture.png` — architecture diagram for the build pattern

## Demo pipeline

The demo lives in `simple-empirical-Scons-demo/` and is organized into four ordered steps:

1. `1.import-data/` — Python data import
2. `2.clean-data/` — Python data cleaning
3. `3.regression-analysis/` — Stata regression analysis
4. `4.build-paper-and-slides/` — LaTeX paper build through a Python wrapper

Each step is wired together through SCons so downstream outputs rebuild when upstream inputs change.

## Prerequisites

- Python 3
- `pip`
- Stata (`StataSE-64` on `PATH` for the demo regression step)
- `pdflatex`

Install Python dependencies:

```bash
cd simple-empirical-Scons-demo
pip install -r requirements.txt
```

If your import step needs credentials, copy the example environment file:

```bash
cd simple-empirical-Scons-demo
cp .env.example .env
```

Then edit `.env` and fill in the required values.

## Running the demo

Build the full pipeline from the demo root:

```bash
cd simple-empirical-Scons-demo
scons
```

Typical generated outputs include:

- `1.import-data/raw-data/data.csv`
- `2.clean-data/output/clean_data.csv`
- `3.regression-analysis/output/regression_results.tex`
- `3.regression-analysis/output/regression_macros.tex`
- `4.build-paper-and-slides/output/paper.pdf`

## Documentation

- Detailed demo documentation: `simple-empirical-Scons-demo/README.md`
- Project conventions and agent notes: `CLAUDE.md`
