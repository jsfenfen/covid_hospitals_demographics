# Census data 
 
 Annual Estimates of the Resident Population for Selected Age Groups by Sex for the United States, States, Counties, and Puerto Rico Commonwealth and Municipios: April 1, 2010 to July 1, 2018 from the [2018 Population Estimates](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk).

Factfinder is schedule to be shut down at the end of this month, I'm not clear on how to grab this from the new site.

# Preprocess to only the columns we care about

The larger file isn't included in this distribution. Here's the columns we pull out. All population data are estimates as of July 1, 2018. 

- GEO_id	  [ full FIPs code ]
- GEO_id2	  [ county FIPs code ]
- GEO.display-label. [ County name ]
- est72018sex0_age999 [ County total pop ]
- est72018sex0_age50to54 [ County pop 50 to 54 years ]
- est72018sex0_age55to59 [ County pop 55 to 59 years ]
- est72018sex0_age60to64 [ County pop 60 to 64 years ]
- est72018sex0_age65to69 [ County pop 65 to 69 years ]
- est72018sex0_age70to74 [ County pop 70 to 74 years ]
- est72018sex0_age75to79 [ County pop 75 to 79 years ]
- est72018sex0_age80to84 [ County pop 80 to 84 years ]
- est72018sex0_age85plus [ County pop 85 year and over ]


		xsv select GEO_id,GEO_id2,GEO_display, est72018sex0_age999,est72018sex0_age0to4,est72018sex0_age5to9,est72018sex0_age10to14,est72018sex0_age15to19,est72018sex0_age20to24,est72018sex0_age25to29,est72018sex0_age30to34,est72018sex0_age35to39,est72018sex0_age40to44,est72018sex0_age45to49,est72018sex0_age50to54,est72018sex0_age55to59,est72018sex0_age60to64,est72018sex0_age65to69,est72018sex0_age70to74,est72018sex0_age75to79,est72018sex0_age80to84,est72018sex0_age85plus PEP_2018_PEPAGESEX_with_ann.csv > ../../../processed/2018_county_census_est.csv

## CBSA rollup

See NBER's csv-county fips crosswalk. 

http://data.nber.org/data/cbsa-fips-county-crosswalk.html

