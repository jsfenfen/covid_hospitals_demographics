## CMS Cost reports

The raw cost reports come from CMS: https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/Cost-Reports/Cost-Reports-by-Fiscal-Year 


They are upwords of ~600MB unzipped, so aren't included in this repo. 



### Hospital-level bed data

[hospital_data.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/hospital_data.csv)

This has basic hospital information, as well as bed counts from the 2017 hospital cost reports. The most recent filing was used (and the report number is available in the file). These come from page 9 column 2 of this [original form](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Paper-Based-Manuals-Items/CMS021935) from 2017.  

There's an awesome [python notebook](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/analysis/HospitalICUBeds_2017.ipynb) written by [Erin Petenko](https://github.com/epetenko/) that makes a little clearer how to navigate this data.

The information in the downloadable file comes from the following lines. The documentation is a little hard to follow, see the instructions for completing this form on [p. 62 here](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/R15P240.pdf). 

- acute_beds Adult/Pediatric Acute Care Beds 00700
- icu_beds Intensive Care Beds 00800
- coronary_beds Coronary Care Beds 00900
- burn_beds Burn Intensive Care Units 01000
- surg\_icu_beds Surgical ICU Beds 01100
- oth\_spec\_beds Other Specialty Beds 01200
- total\_beds Total Beds 01400

Military hospitals with an id ending in F are missing data.

The hospital's provider number should correspond to the provider number in the next file.

#