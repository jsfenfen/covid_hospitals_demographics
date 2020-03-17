## CMS Cost reports

The raw cost reports come from CMS: https://www.cms.gov/Research-Statistics-Data-and-Systems/Downloadable-Public-Use-Files/Cost-Reports/Cost-Reports-by-Fiscal-Year 

They don't have header rows, you have to add your own. 

For the NMRC file I used 

	RPT_REC_NUM,WKSHT_CD,LINE_NUM,CLMN_NUM,ITM_VAL_NUM
	
For the RPT file I used

		RPT_REC_NUM,PRVDR_CTRL_TYPE_CD,PRVDR_NUM,Unknown,RPT_STUS_CD,FY_BGN_DATE,FY_END_DATE,PROC_DT,INITL_RPT_SW,LAST_RPT_SW,TRNSMTL_NUM,FI_NUM,ADR_VNDR_CD,FI_CREAT_DT,UTIL_CD,NPR_DT,SPEC_IND,FI_RCPT_DT

They are upwords of ~600MB unzipped, so aren't included in this repo. 

### Documentation

See [instructions for completing this form here](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/R15P240.pdf).

It refers to [42 CFR 412.105(b) ](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/CFR-2010-title42-vol2-sec412-105.pdf) which may be relevant. 

It also cites [69 FR 49093-49098 (August 11, 2004)](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/FR-2004-08-11.pdf)

In general more documentation for the cost reports is [here](https://github.com/jsfenfen/covid_hospitals_demographics/tree/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION).


### Hospital-level bed data

CSV: [hospital_data.csv](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/processed/hospital_data.csv) ;  Shapefile [hosp_geo](https://github.com/jsfenfen/covid_hospitals_demographics/tree/master/data/processed/hosp_geo) 

These files have basic hospital information and bed counts from the most recently filed hospital cost report received in 2017 or later. The source report number, fiscal year end date, and filing date is also included. These come from page 9 column 2 of this [original form](https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/Paper-Based-Manuals-Items/CMS021935) from 2017.  

There's an awesome [python notebook](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/analysis/HospitalICUBeds_2017.ipynb) written by [Erin Petenko](https://github.com/epetenko/) that makes a little clearer how to navigate this data.

The information in the downloadable file comes from the following lines. The documentation is a little hard to follow, see the instructions for completing this form on [p. 62 here](https://github.com/jsfenfen/covid_hospitals_demographics/blob/master/data/source/cost_reports/HOSPITAL2010-DOCUMENTATION/R15P240.pdf). 

Here are the bed numbers used, the variable names in **bold**

- **acute_beds** Adult/Pediatric Acute Care Beds 00700
- **icu_beds** Intensive Care Beds 00800
- **coronary_beds** Coronary Care Beds 00900
- **burn_beds Burn** Intensive Care Units 01000
- **surg\_icu_beds** Surgical ICU Beds 01100
- **oth\_spec\_beds** Other Specialty Beds 01200

The total of all of the above bed types is given, *roughly*, by:

- **subtotal\_acute\_beds** Subtotal of acute care beds 01400

Additional bed types

- **subprovider\_ipf\_beds** Subprovider Inpatient Psychiatric Facility beds 01600
- **subprovider\_irf\_beds**  Subprovider Inpatient Rehabilitation Facility 01700
- **subprovider\_oth\_beds**  01800
- **skilled\_nursing\_beds**  01900
- **nursing\_fac\_beds**  02000
- **oth\_longterm\_beds** 02100
- **hospice\_beds**  02400

The sum of total\_med\_beds and all additional bed types is given by

- **all\_beds** All Beds 02700


Military hospitals with an id ending in F are missing bed counts but are included here anyways. Many children's hospitals (e.g. hospital_type = childrens) do not report bed counts. Psychiatric hospitals are not included. Recently opened facilities that have not filed CMS reports yet also show zero bed counts.

The hospital's provider number should correspond to the provider number in the hosital info file.

