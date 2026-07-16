version 14
set more off

* Generate sample data
set obs 10003
gen id = _n
gen age = 20 + int(45 * runiform())
gen income = 30000 + int(70000 * runiform())
gen education_years = 8 + int(13 * runiform())

* Save to text file
export delimited using "build/prepare_data/data.txt", delimiter("|") replace
