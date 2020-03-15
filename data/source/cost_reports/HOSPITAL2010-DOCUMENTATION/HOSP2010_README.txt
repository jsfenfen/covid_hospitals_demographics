HCRIS PRODUCTION NOTES FOR HOSPITAL 2552-10 COST REPORT DATA

1.  OVERVIEW
2.  INTRODUCTION
3.  NOTES
4.  Subscripting of Lines and Columns on the Worksheet forms:
5.  Cost Center Codes
6.  Files and Contents
7.  SET UP GUIDANCE
8.  Provider Control Type Code
9.  DISCLAIMER OF WARRANTY



1. OVERVIEW: 

CMS now stores the HCRIS cost report files in a relational database.  

The foremost characteristic of this database is the fact that data 
elements will be distributed in flat files aligned with the database table 
in which they reside in our database.  

You will be able to access the entire set of HCRIS Cost Report data that
is submitted to HCRIS by a Fiscal Intermediary(FI)/ Medicare Contractor (MAC)
on behalf of a provider.  The major benefit for all users is the ability to use 
Relational Database Technology to quickly exclude certain fields of data or perform 
cross-sectional analysis.


The following website contains the cost reporting reimbursement manuals and 
electronic cost reporting specifications for provider cost reports:    
http://www.cms.hhs.gov/Manuals/
 


2. INTRODUCTION:  

All providers with full 12 months or greater cost reporting periods, which begin on or after 
May 1, 2010 (and end on or after April 30, 2011) should file on the CMS Form 2552-10.  
The 2552-10 data files contain the highest level of Medicare cost report status.  If HCRIS 
has both an as submitted report and a final settled report for a hospital for a particular year, 
the data files will only contain the final settled report.   If HCRIS has an as 
submitted, final settled, and reopened report for a hospital for a 
particular year, the data files will contain the reopened cost report. 

It is possible for 1 Hospital to submit 2 or more cost reports for a given year
for the same cost report status.  This may happen if a hospital changes
its FY, or if there is a CHOW (Change of Ownership) during the year.  We have
also found cost reports that were sent in error with an incorrect FYB or
FYE.  For the most part, HCRIS tries to eliminate these incorrect submissions by
contacting the FI/MAC and deleting a cost report that the FI/MAC identifies as incorrect. 

If you have any questions about this product, please contact the HCRIS staff via 
e-mail at HCRIS@cms.hhs.gov, and include the word "Hospital" in the subject line.



3. NOTES: 

The data included with this release includes all years (from FY 2010 through Current).    

To use the Hospital cost report data, you first need to determine the data that 
you are interested in by reviewing the cost report forms and the data specifications.
You will need to know the Worksheet code, line, and column from the cost report form.  
For example, if you wanted to extract the number of hospital beds, you will need to 
determine where this information is collected in the report and use these elements 
as parameters to pull the data from the HOSP_RPT_NMRC table.   The number of beds 
is collected on Worksheet S-3,Part I, Line 14, Column 2 so you would create the 
following condition:  
     Worksheet Code ='S300001' 
     Line Number ='01400'
     Column Number ='00200'    
 *Note: Refer to the file named Hosp2010_Worksheet_Codes.doc to determine worksheet 
codes.  Line Numbers are 5 positions, and Column Numbers are 5 positions.



4.  Subscripting of Lines and Columns on the Worksheet forms:

Many lines on the worksheet forms can be subscripted.  For example, Worksheet S-3, Part I, Line 22
(HHA) can be subscripted if the hospital has more than one HHA.  Keep that in mind when extracting data for a 
particular line.  Also lines that are described as Other are usually subscripted.  



5.  Cost Center Codes:

Refer to the file named CSTCDS.pdf to see the cost center code descriptions and the line numbers they should be reported
on in the cost report.  However, we have seen cases where the cost center codes are not always reported on these line 
numbers noted in this file.  
 
In the 2552-10 data files, the line number in the Hosp_Rpt_Nmrc file is the actual line number the data was reported.  
We did not change the line number to the cost center code as was done for the 2552-96 data files.  
To see the cost center code for the line number, you have to get that from the Hosp_Rpt_Alphnmrc file 
in Worksheet A000000, COlumn 00000.  

5.1.  Retrieving cost center coded data:  

Cost center coding allows all the numeric data on a particular line to be associated
with a cost center. The cost center is described in the alphanumeric data for worksheet A (A000000)
in column zero (00000). The text in that cell contains the cost center code and a description of the 
cost center. The associated line indicates the lines in the numeric table that contain data for that cost 
center. The following alphanumeric record indicates that data for cost center 02060 NeoNatal Intensive Care Unit
in report number 197 will appear on line 03501 in the numeric table.

RPT_REC_NUM	WKSHT_CD	LINE_NUM	CLMN_NUM	ALPHNMRC_ITM_TXT
197	        A000000	         03501	        00000	        02060NEONATAL INTENSIVE CARE UNIT 


Step 1 : retrieve the correct label records from the A worksheet 
        

    Example : Finding data for NEONATAL INTENSIVE CARE UNITS
       
    For providers using standard and non-standard cost center coding,this can done by looking for
    A worksheet column 0 records which contain cost center codes in the range 
    '02060' to '02079'.
    
    Sample code 1a :
    
    select * from alpha
    where  alpha.wksht_cd = 'A000000'
    and alpha.clmn_num = '00000'
    and substr(alpha.alphnmrc_itm_txt,1,5) between '02060' and '02079'
    and rpt_rec_num = 197
    
    
    As an alternative, and especially for providers using provider specific(neither standard nor non-standard) cost center coding, this can be done by 
    retrieving worksheet A column 0 containing the text "NEO"
  
    Sample code 1b :

    select * 
    from alpha
    where alpha.alphnmrc_itm_txt like '%NEO%'
    and alpha.wksht_cd = 'A000000'
    and alpha.clmn_num = '00000'
    and rpt_rec_num = 197

Step 2: retrieve data from the numeric table whose lines match the lines returned from the alpha query
    
    This can be accomplished in two ways: 

    Sample code 2a :

    option 1) joining the nmrc table alpha tables by rpt_rec_num and line_num
    
      SELECT   alpha.rpt_rec_num,                                 -- alpha columns
           alpha.line_num,
           alpha.alphnmrc_itm_txt,
           SUBSTR (alpha.alphnmrc_itm_txt, 1, 5) CCC,
           nmrc.line_num,                                   -- numeric columns
           nmrc.clmn_num,
           nmrc.itm_val_num
    FROM   alpha, nmrc
   WHERE                                     -- column 0 labels for report 197
           alpha.wksht_cd = 'A000000' AND alpha.clmn_num = '00000'
           AND SUBSTR (alpha.alphnmrc_itm_txt, 1, 5) BETWEEN '02060'
                                                         AND  '02079'
           AND alpha.rpt_rec_num = 197
           AND nmrc.rpt_rec_num = alpha.rpt_rec_num -- matching nmrc records in worksheet A
           AND nmrc.wksht_cd = 'A000000'
           AND nmrc.line_num = alpha.line_num
      ORDER BY   rpt_rec_num, CCC, clmn_num
    
     or 

     option 2 ) using a subquery to retrieve only nmrc records matching the required lines
     
	SELECT   wksht_cd, line_num, clmn_num, itm_val_num
  	FROM   nmrc
	WHERE   wksht_cd = 'A000000'
         AND (rpt_rec_num, line_num) IN
                  (SELECT   rpt_rec_num, line_num
                     FROM   alpha
                    WHERE   alpha.wksht_cd = 'A000000'
                            AND alpha.clmn_num = '00000'
                            AND SUBSTR (alpha.alphnmrc_itm_txt, 1, 5) BETWEEN '02060'
                                                                          AND  '02079'
                            AND rpt_rec_num = 197)       


   Sample code 2a :

    option 1) joining the nmrc table alpha tables by rpt_rec_num and line_num
    
      SELECT   alpha.rpt_rec_num,                                 -- alpha columns
           alpha.line_num,
           alpha.alphnmrc_itm_txt,
           SUBSTR (alpha.alphnmrc_itm_txt, 1, 5) CCC,
           nmrc.line_num,                                   -- numeric columns
           nmrc.clmn_num,
           nmrc.itm_val_num
       FROM   alpha, nmrc
       WHERE                                     		-- column 0 labels for report 197
           alpha.wksht_cd = 'A000000' AND alpha.clmn_num = '00000'
           AND alpha.alphnmrc_itm_txt like '%NEO%'
           AND alpha.rpt_rec_num = 197
           AND nmrc.rpt_rec_num = alpha.rpt_rec_num 	-- matching nmrc records in worksheet A
           AND nmrc.wksht_cd = 'A000000'
           AND nmrc.line_num = alpha.line_num
      ORDER BY   rpt_rec_num, CCC, clmn_num
    
     or 

     option 2 ) using a subquery to retrieve only nmrc records matching the required lines
     
	SELECT   wksht_cd, line_num, clmn_num, itm_val_num
  	FROM   nmrc
	WHERE   wksht_cd = 'A000000'
         	AND (rpt_rec_num, line_num) IN
                  (SELECT   rpt_rec_num, line_num
                     FROM   alpha
                    WHERE   alpha.wksht_cd = 'A000000'
                            AND alpha.clmn_num = '00000'
                            and alpha.alphnmrc_itm_txt like '%NEO%'
                            AND rpt_rec_num = 197)       



5.2.  Extracting data for ICU; CCU: SICU; BICU; and Other ICU:  
The intensive care cost centers that are reported on Worksheets S-3, Part I; G-2; D-1; and D-6 are no 
longer cost center coded.  You extract the actual line number on the form.  For example, if you want ICU beds, you should extract Worksheet 
Code S300001, Line Numbers 00800 through 00899, Column 00200.  


6. FILES AND CONTENTS:   

6.1 HOSP2010 Data File(s) : HOSPYYYY_DATA.ZIP 

	Compressed files with the raw data for each fiscal year YYYY with text(.csv) files to be loaded into the 
	HOSP2010_RPT table,the HOSP2010_RPT_NMRC table, and the HOSP2010_RPT_ALPHNMRC table.  

6.2 HOSP2010 Report File(s) : HOSP2010_REPORTS.ZIP

	HOSP2010_RECORD_COUNTS.csv - A csv file containing a list of the record counts per fiscal year.  

	HOSP2010_COST_REPORT_STATUS_COUNTS.csv - A csv file containing the counts of cost reports per type and fiscal year.  

	HOSP2010_provider_id_info.csv  - A csv file containing one line of identifying data for each provider.

	IME_GMEYYYY.csv - csv files containing IME and GME data for the fiscal year yyyy.

	CSTS_CHRGSYYYY.CSV - csv files containing cost charges for the fiscal year yyyy.



6.3 HOSP2010 Documentation Files : HOSP2010_DOCUMENTATION.ZIP

	HOSP2010_README.txt - This readme file. 

	HOSP2010_CROSSWALK.PDF - Lists of old form (2552-1996) cells with corresponding location in the new form (2552-2010).

	HOSP2010_WORKSHEET_CODES.PDF - Lists of possible worksheet codes for the new form.

	HOSP2010_COST_CODES.PDF - Lists of possible cost center codes for the new form.

	HOSP2010_IME_DSH_EXPLANATION.pdf - A .pdf file listing the sources of the data in the IME DSH files.


6.4 HCRIS Documentation Files : HCRIS_DOCUMENTATION.ZIP

	HCRIS_FACILITY_NUMBERING.csv:  A csv file containing information on how to identify the type of facility by the last four positions of the provider number.  

	HCRIS_STATE_CODES.csv:  A csv file contains all the state codes for each state.

	HCRIS_TABLE_DESCRIPTIONS_AND_SQL.txt - A text file containing the descriptions of the tables, 
	and an ANSI SQL Program (non-Database specific) Containing the DDL scripts to create the 3 tables that comprise the HCRIS Hospital Database.

	HCRIS_DATA_DICTIONARY.csv:  A csv file that contains the meanings of the 
	data elements in the HOSP2010_RPT file, the HOSP2010_Alphnmrc file, and the HOSP2010_Nmrc file.   

	HCRIS_DATA_MODEL.pdf - A .pdf file that contains a diagram of the tables.  
	The columns are listed in the exact order they appear in the files.


6.5 HOSP2010 SAS files: HOSP10-SAS.ZIP

	PRDS_HOSP10_YRyyyy.sas7bdat - SAS file containing data for the fiscal year yyyy.

	HOSP10_SAS_FILE_RECORD_LAYOUT.PDF - .pdf file with details about the field names, data types and worksheet source of each column.

	HOSP10_SAS_FILE_ROLLUP_FIELDS_DEFINED.pdf - .pdf file defining which fields are summed into the SAS rollup columns.	

	The Office of the Actuary requested that HCRIS post the CMS internal Hosp10 SAS files to our website.  CMS determined how to rollup the data fields on the A, B, C, D, E, G and S series of worksheet forms.  Please refer to the Hosp10 Rollups Defined.pdf for the definition of the rolled up fields. 

	Please note: The methods of combining reported data as published in the 2552-96 forms have proven to be unreliable. Users are encouraged to develop their own methods of summarizing HCRIS data.   



7. SET UP GUIDANCE:  

It is important to note that the datafiles you will be provided are not restricted 
for use in one given database platform or even a database management system for 
that matter.  
You will likely be able to use your existing tools or utilities to access the data, 
given the ability of those tools to handle files up to the size of the largest 
datafile 
and files containing data arranged in CSV or Comma Separated value format.  
You will, however, need to re-program, re-direct, or adjust any programs, 
utilities or 
other automated routines previously used with HCRIS files, to the new data 
specifications.  

If you choose to modify your existing programs, please be certain to examine the 
individual datafile and corresponding database table structure carefully or else 
you may not achieve valid results or even be able to access the data. If you 
choose to use a relational or desktop database management system, please be 
mindful of the sizes of the various datafiles.   



8.  PROVIDER CONTROL TYPE CODE

The provider control type codes are in 2 places in the file, and they are as follows:

The Hosp_Rpt file contains the column called Provdr_Ctrl_Type_Cd. 
It is also in the Hosp_Rpt_Nmrc file.  You have to extract the following:
Worksheet Code = S200001
Line_Num = 02100
Col_Num = 0100



9.  DISCLAIMER OF WARRANTY:    

The Centers for Medicare & Medicaid Services shall retain no responsibility for 
the data recipients inability to load, examine, or otherwise use the published data 
for 
the HCRIS system.  

The information in these files is subject to change, and should be reviewed for 
each release.  

(c) 2013 Centers for Medicare & Medicaid Services, All rights reserved.  
www.cms.hhs.gov

---------------------------------------------------------------------------------




	
