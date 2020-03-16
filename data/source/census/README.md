# Census data 
 
 Annual Estimates of the Resident Population for Selected Age Groups by Sex for the United States, States, Counties, and Puerto Rico Commonwealth and Municipios: April 1, 2010 to July 1, 2018 from the [2018 Population Estimates](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk).

Factfinder is schedule to be shut down at the end of this month, I'm not clear on how to grab this from the new site.

# Preprocess to only the columns we care about

The larger file isn't included in this distribution. Here's the columns we pull out. 

- GEO_id	  [ full FIPs code ]
- GEO_id2	  [ county FIPs code ]
- GEO.display-label. [ County name ]
- est72018sex0_age999 [ County total ]
- est72018sex0_age50to54
- est72018sex0_age55to59
- est72018sex0_age60to64
- est72018sex0_age65to69
- est72018sex0_age70to74
- est72018sex0_age75to79
- est72018sex0_age80to84
- est72018sex0_age85plus


		xsv select GEO_id,GEO_id2,GEO_display,est72018sex0_age999,est72018sex0_age50to54,est72018sex0_age55to59,est72018sex0_age60to64,est72018sex0_age65to69,est72018sex0_age70to74,est72018sex0_age75to79,est72018sex0_age80to84,est72018sex0_age85plus PEP_2018_PEPAGESEX_with_ann.csv > age_breakout.csv


## CBSA rollup

See NBER's csv-county fips crosswalk. 

http://data.nber.org/data/cbsa-fips-county-crosswalk.html

