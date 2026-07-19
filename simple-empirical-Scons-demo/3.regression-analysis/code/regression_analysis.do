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
Output:            regression_results.txt, regression_output.dta
==================================================*/

/*==================================================
              0: Program set up
==================================================*/
version 19.5
clear all
set more off
set scheme s2mono


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
* Export regression table to text file (relative to project root)
esttab result1 using 3.regression-analysis/output/regression_results.txt, replace ///
	cells(b(star fmt(3)) se(par fmt(3))) ///
	stats(N r2, fmt(0 3)) ///
	label title("OLS Regression: y on x")

* Save regression output dataset (relative to project root)
save 3.regression-analysis/output/regression_output.dta, replace


exit
/* End of do-file */

><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><><

Notes:
1. All paths are relative to project root (simple-empirical-Scons-demo/)
2. Input data from step 2: 3.regression-analysis/input-data/clean_data.csv
3. Outputs saved to 3.regression-analysis/output/


Version Control:
19 Jul 2026 - Initial version following dotemplate.do structure

