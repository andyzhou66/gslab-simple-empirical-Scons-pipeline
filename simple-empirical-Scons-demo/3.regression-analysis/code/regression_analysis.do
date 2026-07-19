/*==================================================
project:       Simple Empirical SCons Pipeline
Author:        Andy Zhou
E-mail:        andy.zhou@example.com
url:           https://github.com/andyzhou66/gslab-simple-empirical-Scons-demo
Dependencies:  clean_data.csv (from step 2)
----------------------------------------------------
Creation Date:    19 Jul 2026
Modification Date:
Do-file version:    01
References:        OLS regression on cleaned data
Output:            regression_results.tex, regression_output.dta
==================================================*/

/*==================================================
              0: Program set up
==================================================*/
version 19.5
clear all
set more off
set scheme s2mono

* ── Logging (mirrors gslab_scons/builders/gslab_builder.py) ────────────────
* Use Stata's inherent log command. The log is written to this step's temp/
* folder as Sconscript_regression_analysis.log, with start/end timestamps in
* the gslab '{YYYY-MM-DD HH:MM:SS}' convention. Stata runs from the project
* ROOT, so the path is root-relative.
capture mkdir "3.regression-analysis/temp"
local _sd = date(c(current_date), "DMY")
local _ts_start = string(year(`_sd'), "%04.0f") + "-" ///
    + string(month(`_sd'), "%02.0f") + "-" ///
    + string(day(`_sd'), "%02.0f") + " " + c(current_time)
log using "3.regression-analysis/temp/Sconscript_regression_analysis.log", replace text
display "*** Builder log created: {`_ts_start'}"


/*==================================================
              1: Load and prepare data
==================================================*/
* Import cleaned data (relative to project root)
import delimited 3.regression-analysis/input-data/clean_data.csv, clear

* Display summary statistics
summarize


/*==================================================
              2: Run regression analysis
==================================================*/
* Run simple OLS regression: y = a + b*x
regress y x

* Store results for export
eststo result1


/*==================================================
              3: Save results
==================================================*/
* Export regression table to LaTeX file (relative to project root)
* The `tex` option wraps the table in a tabular environment, intended to be
* \input{} from a LaTeX document.
esttab result1 using 3.regression-analysis/output/regression_results.tex, replace ///
	cells(b(star fmt(3)) se(par fmt(3))) ///
	stats(N r2, fmt(0 3)) ///
	label title("OLS Regression: y on x") ///
	tex

* Save regression output dataset (relative to project root)
save 3.regression-analysis/output/regression_output.dta, replace


* ── Close log with completion timestamp (mirrors gslab_builder.timestamp_log) ─
local _ed = date(c(current_date), "DMY")
local _ts_end = string(year(`_ed'), "%04.0f") + "-" ///
    + string(month(`_ed'), "%02.0f") + "-" ///
    + string(day(`_ed'), "%02.0f") + " " + c(current_time)
display "*** Builder log completed: {`_ts_end'}"
log close


exit
/* End of do-file */

><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

Notes:
1. All paths are relative to project root (simple-empirical-Scons-demo/)
2. Input data from step 2: 3.regression-analysis/input-data/clean_data.csv
3. Outputs saved to 3.regression-analysis/output/


Version Control:
19 Jul 2026 - Initial version following dotemplate.do structure

