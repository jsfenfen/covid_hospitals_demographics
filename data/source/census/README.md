# census data 
 
 Annual Estimates of the Resident Population for Selected Age Groups by Sex for the United States, States, Counties, and Puerto Rico Commonwealth and Municipios: April 1, 2010 to July 1, 2018  more information
 
[2018 Population Estimates](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk) <-- additional navigation is prob required




It seems like there's a limit to the number of columns you can download using the soon-to-be-mothballed American Factfinder, I had to hide some columns? 

# Preprocess to only the columns we care about

The larger file isn't included in this distribution. Here's the columns we pull out. 

- GEO.id2	
- GEO.display-label
- est72018sex0_age999 [ County total ]
- est72018sex0_age50to54
- est72018sex0_age55to59
- est72018sex0_age60to64
- est72018sex0_age65to69
- est72018sex0_age70to74
- est72018sex0_age75to79
- est72018sex0_age80to84
- est72018sex0_age85plus


xsv select GEO.id2,GEO.display-label,est72018sex0_age999,est72018sex0_age50to54,est72018sex0_age55to59,est72018sex0_age60to64,est72018sex0_age65to69,est72018sex0_age70to74,est72018sex0_age75to79,est72018sex0_age80to84,est72018sex0_age85plus > age_breakout



## CBSA rollup

See NBER's csv-county fips crosswalk. 

http://data.nber.org/data/cbsa-fips-county-crosswalk.html

