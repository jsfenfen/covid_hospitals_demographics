from bs4 import BeautifulSoup
import csv
import glob
import os
import datetime
import re


"""
scp -i ~/accounts/jf2018.pem ubuntu@34.224.37.68:/home/webuser/covid_hacks/recent_backups.tar.gz ./
tar -xzvf recent_backups.tar.gz

"""

filebasestring = "backups/ohapage*.html"


def clean_header(header):
	""" OHA really likes putting weird chars in their column names """
	header = header.replace(",","")
	header = header.replace(" ","_")
	header = header.replace("✣","")
	header = header.replace("*","")
	header = header.replace("\ufeff","")
	header = header.replace("‡","")
	header = header.replace("†","")
	return header

def output_table(data_table, outputfile):
	""" Writes a csv of just the table to a file """

	header_names = []
	data_rows = []

	rows = data_table.find_all('tr')

	for i, row in enumerate(rows):
		if i==0:
			colheaders = row.find_all('th')
			header_names = [clean_header(i.text) for i in colheaders]
			print(header_names)

		else:
			data = row.find_all('td')
			data_fixed = [i.text for i in data]
			#print(data_fixed)
			data_rows.append(data_fixed)

	outfileh = open(outputfile, 'w')
	writer = csv.writer(outfileh, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	writer.writerow(header_names)
	for data_row in data_rows:
		writer.writerow(data_row)

def get_table_from_header(first_header, i):
	if first_header == 'County':
		return 'county'

	if first_header == 'Age group':
		return 'age_group'

	if first_header == 'Sex': 
		return 'sex'

	if first_header.upper().startswith('HOSPITAL CAPACITY'):
		return 'capacity'

	if re.search(r'Updated daily', first_header):
		return 'test'

	if first_header.upper().startswith('COVID-19 DETAILS'):
		return 'covid_details'

	# it's got a double dagger at the end? 
	if first_header.startswith('Hospitalized'): 
		return 'hospitalized'




files = (glob.glob(filebasestring))
for file in files:
	filename = os.path.basename(file)
	filebase = filename.replace("ohapage_", "ohapageread_")

	# allow an exception for the most current file, maybe? 
	if '_06_15.html' in filebase or '2020_04_20_20_02' in filebase:

	#if '_06_15.html' in filebase:

		print("\n\nProcessing file %s" % filebase)

		filebase_raw = filebase
		filebase = filebase.replace("_06_15.html","")
		
		filebase_parts = filebase.split('_')
		snapshot_date = datetime.datetime(int(filebase_parts[1]), int(filebase_parts[2]), int(filebase_parts[3]))
		prior_day = snapshot_date

		if '_06_15.html' in filebase_raw:
			prior_day = prior_day - datetime.timedelta(days=1)

		print("prior day %s" % prior_day)

		new_filebase = 'ohapageread_' + prior_day.strftime("%Y_%m_%d") + ".csv"

		filebase = new_filebase

		print("filebase: %s" % filebase)


		raw_page = open(file, 'r').read()
		soup = BeautifulSoup(raw_page, features="html.parser")
		tables = soup.find_all('table')

		for i,table in enumerate(tables):

			first_row = table.find_all('tr')[0]
			first_header = first_row.find_all('th')[0].text
			
			table_name = ''

			if i == 0:
				table_name = 'summary'
			else:
				table_name = get_table_from_header(first_header, i)

			print("%s -- %s --%s" % (i, first_header, table_name))

			if table_name:
				#print("Got table name %s" % table_name)

				outfile = "pages_parsed/" + table_name + "_" + filebase

				output_table(table,outfile)
			else:
				print("**No table for '%s'" % first_header)
				pass
		

