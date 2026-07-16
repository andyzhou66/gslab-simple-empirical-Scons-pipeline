version 14
set more off

* Load data with proper delimiter settings
import delimited "build/prepare_data/data.txt", delimiter("|") clear

* Run descriptive stats and save to file
log using "build/descriptive/summary.log", text replace
display " "
display "DESCRIPTIVE STATISTICS SUMMARY"
display " "
describe
summarize age income education_years
log close

* Create correlation file
log using "build/descriptive/correlation.log", text replace
display " "
display "CORRELATION ANALYSIS"
display " "
correlate age income education_years
log close

display "All analyses complete!"
