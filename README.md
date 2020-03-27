# Hospital, population, nursing center data

This repository is a project to present and join datasets pertinent to the COVID-19 pandemic at the county level: hospital location and capacity, nursing home location and capacity, and county-level population estimates by age.

A simplified state-level view of this with only population breakouts for 65+ is available [here](https://docs.google.com/spreadsheets/d/1XC0SfpPgYkhLPe4CeXDKs3sgVw8Cbcqa3MpEt8tUQcY/edit#gid=0). The source data for statewide hospital beds is [here](https://www.ahd.com/state_statistics.html).

In general this repo is trying to follow the datakit repo convention, it isn't *actually* a datakit repo but may become one at some point. 


# Data


The main output files are described below. In general the output files are in /data/processed/. 

## Hospital-level bed data

CSV: [hospital_data.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/hospital_data.csv) ;  Shapefile (contains fewer bed detail columns) [hosp\_geo\_final](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/hosp_geo_final.zip) 

### Fast answer: COVID ready ICU beds?

What's a COVID -ready ICU bed? We can't really say. Hospitals are full of creative brilliant folks who are hard at work ramping up capacity to care for patients with COVID. This data is to help understand the health system's prior baseline operations, as reported to CMS. 

One way of thinking about this could be all available emergency beds, roughly arrived at by `subtotal_acute_beds_1400 - acute_beds_0700` Again, we'd caution users not to assume too much, as hospitals have difficult decisions to make, room by room, in regards to separating out COVID patients, and maintaining the capability to treat non-COVID injuries. It may be better to think of a systemwide response rather than focusing too much on any particular hospital. The medical system is complex and shortages of PPE, ventilators, or staff to operate it may all play a larger role than beds. If you know of a good source in CMS data for ventilator charges, please let me know! 

Because the lines effected do not directly imply payment, they are possibly more prone to error. If you are concerned with a figure in a particular cost report, consider consulting reports from earlier periods. A file of all reports with extracted data from 2016 through 2019 [is available here](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/cost_report_extracts.csv). 

### Background


The hospital bed counts data come from the raw CMS cost reports database [here](https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/Cost-Reports/Cost-Reports-by-Fiscal-Year). They are upwards of ~600MB unzipped, so aren't included in this repo. A simple introduction to how they are structured is [here](https://www.resdac.org/articles/medicare-cost-report-data-structure).

They don't have header rows, if you want to process them you have to add your own. 

For the NMRC file I used 

	RPT_REC_NUM,WKSHT_CD,LINE_NUM,CLMN_NUM,ITM_VAL_NUM
	
For the RPT file I used

	RPT_REC_NUM,PRVDR_CTRL_TYPE_CD,PRVDR_NUM,Unknown,RPT_STUS_CD,FY_BGN_DATE,FY_END_DATE,PROC_DT,INITL_RPT_SW,LAST_RPT_SW,TRNSMTL_NUM,FI_NUM,ADR_VNDR_CD,FI_CREAT_DT,UTIL_CD,NPR_DT,SPEC_IND,FI_RCPT_DT
	
These files have basic hospital information and bed counts from the most recently filed hospital cost report received in 2017 or later. The source report number, fiscal year end date, and filing date is also included. These come from page 9 column 2 of this [original form](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Paper-Based-Manuals-Items/CMS021935) from 2017. 

The documentation is a little hard to follow, see the instructions for completing this form on [p. 62 here](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/R15P240.pdf).  It refers to [42 CFR 412.105(b) ](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/CFR-2010-title42-vol2-sec412-105.pdf) which may be relevant. It also cites [69 FR 49093-49098 (August 11, 2004)](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/FR-2004-08-11.pdf). In general more documentation for the cost reports is [here](https://github.com/jsfenfen/covid_hospitals_demographics/tree/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION).

 
There's an awesome [python notebook](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/analysis/HospitalICUBeds_2017.ipynb) written by [Erin Petenko](https://github.com/epetenko/) that makes a little clearer how to navigate this data.

Each of the hospital bed lines corresponds directly to a line in the column 2 of worksheet S-3 (except for the ICU total). 

A numeric breakdown of the minor lines, which do not end in '00' and are summed in their respective ext\_NN99 variables, are [available here](https://docs.google.com/spreadsheets/d/1nAIbiJ7LMPmHVcJvuceMKHTUn__Hly4LYMjeevMO1mc/edit?usp=sharing). 

### Major lines versus subscripted lines

CMS documentation describes major lines in Worksheet 3 part 1; they end in '00'. For instance, ICU beds in theory are given by line '00800'. However, CMS appears to tolerate "subscripted" lines with values other than '00800'. There's no standard as to what these mean; some hospitals might use 801 to mean neonatal intensive care unit beds, whereas others might use it to mean pediatric intensive care unit beds. After five emails with RESDAC, I believe there is no way to link the "subscripted" line descriptions with their values. 

To simplify summing beds, we've summed all additional units into 00N99 rows. In other words, 00800 is listed as icu\_beds\_800 but any other units matching 008\d\d will be summed into extra\_beds\_0899. This does allow the possibility of "overcounting"--neonatal beds are unlikely to be useful in fighting the coronavirus--but it appears that some hospitals have chosen to break out all of their 00800 lines into subscripts, so it's better to overcount than leave them out entirely.

The last caveat is that some hospitals report icu\_bed\_days despite not reporting icu beds. This could happen if icu beds are added late in the reporting period, although it could also be a mistake. If this flag is true, consider the possiblity that ICU beds are present, they just haven't been reported.

### Bed utilization

CMS requires hospitals to report overall bed utilization in the form of days for the same lines as beds. The same format of summation is used: 00800 for icu beds listed as 00800; and 00899 for the sum of 00801, 00802, 00803, etc. 

Bed utilization is given for all\_icu\_beds and subtotal\_acute\_beds. It's a percentage of days\_in\_period that the beds were full for each reported line. 

Observation bed days are not used in utilization calculations.



### CMS line numbers to column names

Here are the bed numbers used, the variable names appear in **bold**. In general, appended \_XXXX means that the variable appears on line XXXX in the original report, except for XX99 lines, which are summation of "other" values accepted for this bed type.

- **acute_beds\_0700** All Adult/Pediatric Acute Care Beds
- **icu\_beds\_0800** Intensive Care Beds 
- **extra\_0899** All other intensive care beds, including lines '00801','00802','00803','00804','00805','00806','00807','00808','00810','00820','00830','00850'

- **coronary\_beds\_0900** Coronary Care Beds
- **extra\_0999** All other Coronary Care Beds including '00901','00902','00903
- **burn\_beds\_1000** Burn Intensive Care Units
- **extra\_1099** Other Burn Intensive Care Units  including '01001','01002','01003','01004'

- **surg\_icu_beds\_01100** Surgical ICU Beds
- **extra\_1199** Other surgical ICU beds including '01101','01102','01103','01104','01105','01106','01107','01110'

- **oth\_spec\_beds\_1200** Other Specialty Beds
- '**extra\_1299** Other specialty units including '01201', '01202','01203','01204','01205','01206','01210'
 

The sum of the above lines is given by:

- **subtotal\_acute\_beds\_1400** Subtotal of acute care beds 01400

To make working with ICU data easier there's also a column of all 08XX lines:

- **all\_icu\_beds** A summation of **icu\_beds\_0800** and **extra\_0899**. This is used to calculate total ICU utilization. Be skeptical of ICU bed numbers that rely heavily on units described in extra\_0899, often a fraction of these are intended for children or infants and won't be useful for adults. 


Additional hospital bed types (not acute care beds)

- **subprovider\_ipf\_beds\_1600** Subprovider Inpatient Psychiatric beds
- **subprovider\_irf\_beds\_1700**  Subprovider Inpatient Rehabilitation beds
- **subprovider\_oth\_beds\_1800**  Subprovider Inpatitent Other beds
- **skilled\_nursing\_beds\_1900**  Skilled nursing beds
- **nursing\_fac\_beds\_2000**  Nursing Facility beds
- **oth\_longterm\_beds\_2100** Other Longterm beds
- **hospice\_beds\_2400**  Hospice beds

The sum of subtotal\_acute\_beds and all additional hospital bed types is given by

- **all\_beds\_2700** All Beds

- **labor\_delivery\_beds\_3200** Labor and Delivery Beds. These are *not* included in 02700 "All Beds," per CMS rules.


Military hospitals with an id ending in F are missing bed counts but are included here anyways. Many children's hospitals (e.g. hospital_type = childrens) do not report bed counts. Psychiatric hospitals are not included. Recently opened facilities that have not filed CMS reports yet also show zero bed counts.

(The shapefile leaves out [one hospital](https://data.medicare.gov/resource/xubh-q36u/row-hgvv.mh7i-bzfv) in Puerto Rico.)

The hospital's provider number should correspond to the provider number in the next file.

### Bed days

For each of the bed types described above, there is also a corresponding `_bed_days` variable. E.g. icu\_bed\_days\_0800 corresponds to icu\_beds\_0800 and 
extra\_days\_0899 corresponds to the number of beds given in extra\_0899

### Bed utilization

Utilization rate, as a percent, is calculated for all\_icu\_beds and for subtotal\_acute\_beds. To estimate the spare ICU bed capacity, you could use: 	
	`all_icu_beds * all_icu_utilization / 100`

### Unlisted ICU rooms

One of the major concerns data users have are unreported or missing ICU room beds. We found ~23 cost reports that reported ICU bed days without recording having any ICU beds. When that is the case, the field icu\_days\_no\_beds is set to true to warn that some ICU beds may have been omitted.

### Additional data files

The hospital data file uses only the most recent cost report data for reports received in 2017 or later. But you can download cost report data for [all years since 2016 here](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/cost_report_extracts.csv). The most_recent flag indicates if the report is the most recent used.

If you are really curious as to what the other bed units used by each hospital are, you can look at the [extra line data file](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/extra_line_data.csv). It gives the actual line number used by the hospitals in LINE\_NUM. These line designations do not have a consistent meaning--one hospital may use 801 to refer to pediatric ICU beds while another may use it to refer to neonatal ICU beds. 

## Census data by county by age

Downloadable [csv file](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/2018_county_census.csv) ; [shapefile](https://publicaccountability.s3.amazonaws.com/rawfiles/counties_final.zip)
 
County-level population age data comes from the Annual Estimates of the Resident Population for Selected Age Groups by Sex for the United States, States: April 1, 2010 to July 1, 2018 from the [2018 Population Estimates](https://factfinder.census.gov/faces/tableservices/jsf/pages/productview.xhtml?src=bkmk).

Population estimates are given in 5-year age ranges, e.g. 70-74. 



## Geocoded nursing home locations 

CSV File: [nh\_gen\_info\_geocoded\_final.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/nh_gen_info_geocoded_final.csv) 

Source: CMS' nursing home compare data. It contains the number of certified beds and average daily occupancy among other variables.  Lat and lngs were added where they were missing with google's geocoder; where this occurred the column geocode\_flag = 1. The geocode\_accuracy field uses google's terminology. 

Full documentation of the source file is [here](https://data.medicare.gov/Nursing-Home-Compare/Provider-Info/4pq5-n9py)



## Stories

If you're able to use this in your work, or have relevant data to add, please let us know. 

Portland Tribune, 3/14 ["As number of virus cases grows, Oregon has lowest hospital bed rate in U.S."](https://pamplinmedia.com/pt/9-news/456432-372245-as-deluge-approaches-oregon-has-lowest-hospital-bed-rate-in-us).

Monterey Weekly, 3/25 ["Long before coronavirus, local nursing homes were struggling with infection control rules"](https://www.montereycountyweekly.com/news/local_news/long-before-coronavirus-local-nursing-homes-were-struggling-with-infection/article_6e19cd74-6ee0-11ea-ae32-f3dab247856f.html)

## Suggested reading: 
["COVID-19 story recipe: Analyzing nursing home data for infection-control problems"](https://source.opennews.org/articles/covid-19-story-recipe-analyzing-nursing-home-data/), Source, Mike Stucka, 3/16/20

## Contributors

Jacob Fenton, [PublicAccountability.org](https://publicaccountability.org); Erin Petenko  [VTDigger](https://vtdigger.org/); Justin Mayo, [Big Local News](http://biglocalnews.org). Additional resources are available on the Big Local News platform. 


## License and Attribution

This data is freely available for public use.




