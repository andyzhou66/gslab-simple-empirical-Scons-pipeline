* Step 3: Regression analysis
* Reads clean_data.csv and runs OLS regression

clear all
set more off

program main
	* Import cleaned data (relative to code/ → ../input-data/)
	import delimited ../input-data/clean_data.csv, clear

	* Run simple OLS regression: y = a + b*x
	regress y x

	* Display results to log
	eststo result1
	esttab result1 using ../output/regression_results.txt, replace ///
		cells(b(star fmt(3)) se(par fmt(3))) ///
		stats(N r2, fmt(0 3)) ///
		label title("OLS Regression: y on x")

end

main


