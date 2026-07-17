# Empirical Research Best Practices: A Unified Reference

This document synthesizes best practices from two authoritative sources on reproducible empirical research: **Cookiecutter Data Science (CCDS)**, a widely-adopted project template and opinion guide for data science work (https://cookiecutter-data-science.drivendata.org/opinions/), and the **Gentzkow & Shapiro Lab Manual (GSW)**, the internal RA manual of the Gentzkow-Shapiro lab at Stanford, grounded in their practitioner's guide *Code and Data for the Social Sciences* (https://web.stanford.edu/~gentzkow/research/CodeAndData.pdf). Together they cover the full lifecycle of a research project, from directory layout to pre-submission production checklists.

---

## 1. Project Structure

**Organize your project as a directed acyclic graph (DAG): raw inputs flow through clearly defined stages to final outputs, with no cycles.** [CCDS] [GSW]

- Separate raw, intermediate, and final data into distinct directories (e.g., `data/raw/`, `data/interim/`, `data/processed/`). The names matter less than the enforced flow. [CCDS]
- Mirror this separation in code: acquisition scripts, cleaning scripts, and analysis scripts belong in distinct stages. [GSW]
- Keep `analysis/` and `paper_slides/` decoupled. Copy release outputs from one to the other manually; do not create implicit runtime dependencies between pipelines. [GSW]
- Structure the repository so that a new team member can understand the pipeline by reading directory names alone. [CCDS] [GSW]
- Adapt the default structure liberally for your project (flatten when small, expand when complex, add a `research/` folder for long-running experiment sub-trees), but change the default template conservatively so all projects remain consistent. [CCDS]
- Place exploratory notebooks in `notebooks/exploratory/` and polished report notebooks in `notebooks/reports/`. Use the naming convention `<step>-<ghuser>-<description>.ipynb` (e.g., `0.3-bull-visualize-distributions.ipynb`). [CCDS]
- Store supplemental project information (wiki pages, project outlines, to-do items not yet assigned) in the repository's GitHub wiki, not in the main codebase. [GSW]

---

## 2. Data Management

### Immutability of Raw Data

**Never edit raw data. Never overwrite it. Never save multiple versions of it.** [CCDS] [GSW]

- Raw data is read-only. Transform it programmatically into new output files; do not modify it in place. [CCDS]
- Every raw data directory must have a `readme.md` documenting: the data source, when and how it was obtained, and any information needed to understand its provenance and meaning. [GSW]
- Place codebooks, data use agreements, and other documentation in a `docs/` subdirectory of the raw data directory. Store enough documentation that, if access to the original source were lost, you could still understand, reference, and comply with the data. [GSW]
- Raw directories may contain preprocessing code (file conversions, appending files) if needed; in that case, store the original form in an `orig/` subdirectory and preprocessed outputs in `output/` or `data/`. [GSW]

### Data Integrity

- **Store all data in tables with unique, non-missing keys.** [GSW]
- Keep data normalized as far into the pipeline as possible; eliminate redundant cleaning steps that are executed more than once. [GSW]
- Use `save_data` (GSLab's custom save command for R, Stata, and Python) whenever saving data files. It requires an explicit key, checks uniqueness and non-missingness, optionally sorts by key, and outputs a data manifest log. Use the built-in save only in rare, documented exceptions. [GSW]
- After any data merge to main, the assignee and reviewer must confirm: total observation count, missing value counts, and mean/min/max of each variable match expectations shown in the manifest. [GSW]

### Storage Tiers

- Small, diffable files under 5 MB (`.txt`, `.csv`, `.R`, `.do`): store directly in Git. [GSW]
- Non-diffable binaries (`.pdf`, `.dta`, `.rds`) and diffable files over 5 MB: store with Git LFS. [CCDS] [GSW]
- Keep regular GitHub storage under 1 GB per repository (including history); total repository size including LFS under 5 GB. [GSW]
- Large data shared across projects, or data too large for GitHub even with LFS: store on Dropbox, Amazon S3, Azure Blob Storage, or Google Cloud Storage. [CCDS] [GSW]
- **Think carefully before committing any large binary — once committed, its impact on repository size is permanent and nearly impossible to undo.** [GSW]
- The `data/` folder should be in `.gitignore` by default. Include data in the repository only when it is small and rarely changes. [CCDS]

### Intermediate and Final Outputs

- Serialize or cache the outputs of long-running pipeline steps in an `interim/` or analogous directory so they do not need to be recomputed unnecessarily. [CCDS]
- Final processed outputs belong in a `processed/` or `release/` directory. [CCDS] [GSW]
- When tasks are complete, all related files must be either fully completed and stored in shared locations, or fully deleted. Never leave files indefinitely in a half-finished state. [GSW]

---

## 3. Code Quality

**The most important features of analysis code are correctness and reproducibility.** [CCDS]

### General Principles

- Be a good code citizen: improve code you modify even if you did not write it. Refactor regularly to maintain logical structure as the codebase grows. At minimum, leave code quality at least as good as you found it. [GSW]
- No line of code should exceed 100 characters. Break long logical lines using language-appropriate continuations (`///` in Stata, `...` in MATLAB, standard Python line continuation). [GSW]
- Functions should not typically exceed 200 lines. [GSW]
- Use 4-space indentation consistently, per PEP 8. [GSW]

### Python

- Follow PEP 8. [GSW]
- Use docstrings for functions whose purpose may be unclear or that will be used outside their own module. [GSW]
- When opening text files for writing or appending, use `mode="wb"` or `mode="ab"` (binary mode) for portability across operating systems. [GSW]
- When opening text files for reading, use `mode="rU"` to enable universal newline support. [GSW]

### R

- Follow Google's R Style Guide, with exceptions: naming conventions are flexible (underscores or camelCase, no dots), and function comment blocks are encouraged but not required unless the purpose would be unclear. [GSW]

### Stata

- Use linear format (comment headers for major blocks) for short or simple scripts; use functional style (`program...end` blocks with a `main` program) for longer or more complex scripts. [GSW]
- For merges: always specify merge type (1:1, m:1, 1:m); never do m:m merges without strong justification; always use `assert()` and `keep()` options; use `keepusing()` when possible; use `nogen` unless you explicitly need `_merge` later. [GSW]
- Always use forward slashes in file paths for cross-platform compatibility. [GSW]
- Use `preserve/restore` sparingly; explicit save/load of data files is often clearer. [GSW]
- **Always use `save_data` instead of the built-in `save` when saving datasets to `/output/`.** [GSW]

### Notebooks

- Notebooks are for exploration and communication; source files are for repetition and replication. **Source code is superior for replicability because it is more portable, more testable, and easier to code review.** [CCDS]
- Refactor notebook code into source modules when you find yourself duplicating notebooks, copy-pasting functions between notebooks, or building object-oriented classes inside notebooks. [CCDS]
- Do not collaborate directly with others on Jupyter notebooks (diffs are not human-readable; merging is near impossible). Use tools like `nbautoexport` to make reviewing notebook changes easier. [CCDS]

---

## 4. Version Control

### Commits

- **Every commit message must have the form `#X Description of commit` where X is the GitHub issue number** (e.g., `#123 Add first appendix figure`). [GSW]
- Commit messages should describe the purpose of the change, not be redundant with what Git records. "Update code" is bad; "Refactor estimate() function" is good. [GSW]
- Use sentence case, imperative mood, no trailing period. [GSW]
- Any commit that will be merged to main, or that defines an issue deliverable, must follow a complete run of the relevant build scripts (SCons, `make.py`, etc.). [GSW]

### Branches and PRs

- Follow GitHub Flow: open an issue, open a linked issue branch, work, open a pull request when goals are complete. [GSW]
- Pull request title: `PR for #X: original_issue_title`. [GSW]
- If the work affects the main paper draft, include a PDF diff comparing before and after. [GSW]
- Squash-merge issue branches back to main; then delete the issue branch. [GSW]
- Prioritize work in the order: older PRs > newer PRs > older issues > newer issues (by GitHub number). [GSW]

### Large Files

- Track large files with Git LFS (add to `.gitattributes`). [CCDS] [GSW]
- Alternatively, sync large data files with cloud storage (S3, Azure, GCS) using `awscli`, `azcopy`, `gcloud`, `rclone`, or `cloudpathlib`/`fsspec`. [CCDS] [GSW]

---

## 5. Reproducibility

**The best way to ensure reproducibility is to treat your data analysis pipeline as a DAG. Anyone should be able to re-run your analysis using only your code and raw data and produce the same final products.** [CCDS]

- Make it possible — and ideally documented and automated — for anyone to reproduce all final data products from only source code and raw data. [CCDS]
- All figures, tables, and in-text values must be generated programmatically. **Never hard-code values in papers or slides.** [GSW]
- Use `save_data` manifests to make data diffs reviewable in Git without opening data files. [GSW]
- Export plots in both PDF (for papers and slides, high-quality scalable) and PNG (for development, diffable in Git). Specify size and resolution explicitly when exporting. [GSW]
- Use autofill (LaTeX `\newcommand` scalars generated by code) to include regression coefficients and other computed values in paper text, so values never become stale. [GSW]
- Document modeling experiments with at minimum: data provenance, code version used, and metrics. For smaller projects, structured JSON is sufficient; graduate to MLflow or similar if warranted. [CCDS]
- Before any release or submission, confirm that bootstraps and simulations use a sufficiently high number of draws, solver exit flags indicate convergence, and quadrature accuracy is set appropriately. [GSW]

### Replication Packages

When preparing a replication package for submission: [GSW]
1. Remove all files except `code/`, `external.txt`, `input.txt`, and `make.py` (retain `paper_slides/output/` for the final paper and slides).
2. Remove all LyX comments.
3. Delete unused code files.
4. Replace git submodules with directly committed directories.
5. Provide a well-documented README for obtaining any data you cannot share.
6. Remove git history (`rm -rf .git/`), reinitialize with `git init`.
7. Zip the folder and run the full pipeline (`python run_all.py`) to verify end-to-end reproducibility.

---

## 6. Automation (Build Systems and DAG Tools)

**Use a build system to manage pipeline steps so that outputs are only rebuilt when their inputs change.** [CCDS] [GSW]

- CCDS prefers `make` for managing DAG steps, especially long-running ones. [CCDS]
- GSW uses SCons with custom builders (`gslab_scons`) integrated through a `run.py` wrapper and `SConstruct`/`SConscript` build definitions. [GSW]
- Other Python-based DAG tools are acceptable: Airflow, Luigi, Snakemake, Prefect, Dagster, Joblib. [CCDS]
- Use MD5-timestamp deciders (or equivalent) so rebuilds are triggered by content changes, not timestamps alone. [GSW]
- Keep `analysis/` and `paper_slides/` as separate SCons pipelines; do not create cross-pipeline runtime dependencies. [GSW]
- Build logs should be merged into a single `release/sconstruct.log`; repository state should be recorded in `release/state_of_repo.log`. [GSW]
- Run the full pipeline after every commit to main or after every PR merge to verify the build is clean. [GSW]

---

## 7. Documentation

### Code Documentation

- All functions whose purpose is not immediately obvious, or that are used outside their defining module, should have docstrings or comment blocks. [GSW] [CCDS]
- Comment headers are required for every major logical block at the same level in Stata scripts (if you comment one block, comment all blocks at that level). [GSW]
- Include a comment in any code that uses a built-in save command instead of `save_data`, explaining the exception. [GSW]

### Data Documentation

- **Every raw data directory must have a `readme.md`** covering source, acquisition method and date, and any information needed to understand provenance and comply with data use agreements. [GSW]
- Data manifests from `save_data` serve as machine- and human-readable documentation of every saved dataset's structure. [GSW]

### Project Documentation

- Maintain a GitHub wiki for the project with supplemental information, project outlines, and to-do items not yet active. [GSW]
- Issue descriptions must be written in imperative mode and be precise enough that a third party can judge whether the issue was completed. Include enough context for someone returning to the issue months or years later. [GSW]
- Every completed issue must have exactly one summary comment beginning with **Summary**, briefly recapping what was accomplished and containing or linking to the deliverable. [GSW]
- Meeting notes, seminar comments, and external correspondences should be documented (with date and title) in the repository wiki or a linked Google Doc. [GSW]
- When mothballing a project, add a wiki page summarizing what was done, why work is paused, and the state of the repository. [GSW]

### Papers

- Every quantitative or factual claim in a paper must be either autofilled or supported by a citation, table, figure, or a result in a supporting PDF in the drafts directory. [GSW]
- In-text citation format follows AER; unresolved questions follow CMOS. Key rules: serial comma; no comma before year in parenthetical references; "et al." for four or more authors; separate multiple references with semicolons; no nested parentheses. [GSW]
- Titles of sections, tables, and figures use title caps; axis labels and table row/column headers capitalize only the first word. [GSW]
- Numbers 10 and above use numerals; numbers below 10 are written out (break this rule only for parallelism). Numbers above 999 use a thousands-separator comma. [GSW]

---

## 8. Collaboration

### Issues

- Open an issue before beginning any discrete unit of work. Issues should not be more than a couple of weeks of work and should not stay open longer than a month or two. [GSW]
- Issues that grow too broad should be carved into sub-issues; the original issue should be closed with an interim summary. [GSW]
- Do not open issues until the assignee is ready to work on them actively. Future to-do items go on the project wiki outline. [GSW]
- Issue titles use imperative mood, no trailing period; descriptive enough that the purpose and context are clear when read months later. [GSW]

### Communication

- Comment on an issue whenever: you have a question (tag the person), you complete a discrete chunk of work, you have spent at least one day on the issue since the last update, you have not worked on it for five or more business days, or you have a substantive offline interaction about it. [GSW]
- When asking for feedback on results, confirm the results are correct and make sense before posting. [GSW]
- When referencing files, directories, or other objects, include permanent URLs. [GSW]
- Keep email notifications for `@` references enabled; team members assume that comments not `@`-referencing them do not require their attention. [GSW]

### Code Review

- Any issue involving substantial code changes must be reviewed by at least one other lab member. [GSW]
- The reviewer's job is to verify: deliverable is clear and complete; files conform to organizational and style rules; results are clear and appear correct; saved data meet integrity criteria. The reviewer does not need to check every line of code. [GSW]
- Do not collaborate directly on Jupyter notebooks; use source files for shared, version-controlled work. [CCDS]

### Overleaf / Paper Collaboration

- For text edits, collaborate on Overleaf. Do not make local `.tex` edits without syncing to Overleaf. [GSW]
- To upload new tables or figures, replace them in the Dropbox-synced directory. [GSW]
- When ready to commit, export from Overleaf to the local clone of the issue branch, replace files in `paper_slides/code/`, and commit. [GSW]
- Always rebase a collaborator's commits before syncing to Dropbox to avoid conflicts. [GSW]

---

## 9. Environment Management

**The first step in reproducing any analysis is replicating the computational environment: same tools, same libraries, same versions.** [CCDS]

- For data science work, prefer `conda` (via Miniforge or Miniconda) because it manages non-Python dependencies including system libraries common in data science. [CCDS]
- Python-only alternatives are also fine: `virtualenv`, `virtualenvwrapper`, `Poetry`, `Pipenv`. [CCDS]
- For complex or heterogeneous environments, use Docker or Vagrant, defined in `Dockerfile` or `Vagrantfile` committed to source control. [CCDS]
- Use `pip-tools` or `conda-lock` to pin dependencies precisely for full reproducibility. [CCDS]
- **Keep secrets and configuration out of version control.** Store credentials in a `.env` file that is listed in `.gitignore`, and load them at runtime with `python-dotenv`. [CCDS]
- For AWS credentials, use `~/.aws/credentials` with named profiles rather than environment variables, especially when working across multiple projects. [CCDS]
- Store project-level configuration in two files: a versioned `config_global.yaml` (shared settings, version numbers, paths) and an unversioned `config_user.yaml` (local executable paths, cache directories). [GSW]
- On computing clusters (e.g., Sherlock/SLURM): test scripts on a data subset or in an interactive session (`sdev`) before submitting full jobs; explicitly set `PYTHONPATH` or activate conda environments in `~/.bashrc` (not only `~/.bash_profile`) so the environment is available to batch jobs. [GSW]
- Install miniconda to your personal `$HOME` directory on shared clusters; do not load conflicting system Python or R modules. [GSW]
- Preferred cluster storage workflow: clone repo to `$OAK`, rsync to `$SCRATCH`, run job on `$SCRATCH`, commit results, rsync back to `$OAK`. Use `$L_SCRATCH` for jobs with many small file reads/writes. [GSW]

---

## Quick Reference: Most Important Rules

| Rule | Source |
|---|---|
| **Never edit raw data** | CCDS + GSW |
| **Treat the pipeline as a DAG** | CCDS + GSW |
| **Never hard-code values in papers; autofill everything** | GSW |
| **Always use `save_data` with an explicit key** | GSW |
| **Every commit references a GitHub issue number** | GSW |
| **Any commit to main must follow a complete build run** | GSW |
| **Keep secrets out of version control** | CCDS |
| **Refactor notebook code into source modules** | CCDS |
| **Think before committing large binaries — it is permanent** | GSW |
| **Every completed issue has exactly one summary comment** | GSW |
| **First step in reproduction is replicating the environment** | CCDS |
| **Export plots in both PDF and PNG** | GSW |
