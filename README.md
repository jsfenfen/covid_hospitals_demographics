## Hospital, population, nursing center data

This repository is an ad-hoc project to join disparate datasets that may shed light on hospital capacity limits down to the county level.

In general this repo is trying to follow the datakit repo convention, it isn't *actually* a datakit repo but may become one at some point. 

A simplified state-level view of this with only population breakouts for 65+ is available [here](https://docs.google.com/spreadsheets/d/1XC0SfpPgYkhLPe4CeXDKs3sgVw8Cbcqa3MpEt8tUQcY/edit#gid=0). The source data for statewide hospital beds is [here](https://www.ahd.com/state_statistics.html).


## Data

Each of the datasets is documented by the readme file in it's respective folder. In general the output files are in /data/processed/. 

These are the main output files

### Hospital-level bed data

[hospital_data.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/hospital_data.csv)

This has basic hospital information, as well as bed counts from the 2017 hospital cost reports. The most recent filing was used (and the report number is available in the file). These come from page 9 column 2 of this [original form](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Paper-Based-Manuals-Items/CMS021935).  Reports for 2018 appear not to be complete yet. It may be better to use reports from a mix of years, but for simplicities sake we've stuck with 2017.


There's an awesome [python notebook](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/analysis/HospitalICUBeds_2017.ipynb) written by [Erin Petenko](https://github.com/epetenko/) that makes a little clearer how to navigate this data.

The information in the downloadable file comes from the following lines

- tot_beds 00700
- icu_beds 00800
- coronary_beds 00900
- burn_beds 01000
- surg_icu_beds 01100

Military hospitals with an id ending in F are missing data.

The hospital's provider number should correspond to the provider number in the next file.

### Geocoded hospital and nursing home locations 

These come from CMS hospital compare and nursing home compare.

[hospital\_gen\_info\_geocoded\_final.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/hospital_gen_info_geocoded_final.csv)

This file has one line per hospital. The file includes only formatted locations; these are broken out into lat and lng columns. 

CMS provides spatial data for most of these, but it was added to rows that were missing it (with google's geocoder). In these rows "geocode_flag" = 1 and the accuracy is as given by google. 

Todo: add the county fips codes. 

[nh\_gen\_info\_geocoded\_final.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/nh_gen_info_geocoded_final.csv) Is a file of CMS nursing home compare. Lat and lngs were added where they were missing; where this occurred geocode_flag = 1.

Todo: add the county fips codes. 


## Census Data


County-level population age data comes from the Annual Estimates of the Resident Population for Selected Age Groups by Sex for the United States, States: April 1, 2010 to July 1, 2018 from the [2018 Population Estimates](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk).

The full download is rather extensive, the file [age_breakout.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/age_breakout.csv) contains just the geographic info and a selection of ages relevant for modelling the virus:

- GEO_id [ full FIPs code ]
- GEO_id2 [ county FIPs code ]
- GEO.display-label. [ County name ]
-est72018sex0_age999 [ County total, both sexes ]
- est72018sex0_age50to54 [ 2018 est, age 50-54 ]
- est72018sex0_age55to59 [ etc. ]
- est72018sex0_age60to64
- est72018sex0_age65to69
- est72018sex0_age70to74
- est72018sex0_age75to79
- est72018sex0_age80to84
- est72018sex0_age85plus [Age 85 and older ]




There's also a django app for doing more in-depth geographic work, although it's incomplete. 


## Stories

This project is supported by data journalists volunteering their time, if you're able to use this in your work, or have relevant data to add, please let us know. 

Portland Tribune, 3/14 ["As number of virus cases grows, Oregon has lowest hospital bed rate in U.S."](https://pamplinmedia.com/pt/9-news/456432-372245-as-deluge-approaches-oregon-has-lowest-hospital-bed-rate-in-us).

## Contributors

Jacob Fenton, [PublicAccountability.org](https://publicaccountability.org); Erin Petenko  [VTDigger](https://vtdigger.org/)






