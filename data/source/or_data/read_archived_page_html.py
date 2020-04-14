from bs4 import BeautifulSoup
import csv
import glob
import os
import re

date_re = r'(2020)(03)(\d\d)'


def output_table(data_table, outputfile):
	""" Writes a csv of just the table to a file """

	header_names = []
	data_rows = []

	rows = data_table.find_all('tr')

	for i, row in enumerate(rows):
		if i==0:
			colheaders = row.find_all('th')
			header_names = [i.text for i in colheaders]
			print(header_names)

		else:
			data = row.find_all('td')
			data_fixed = [i.text for i in data]
			print(data_fixed)
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


	if first_header == 'Hospital Capacity':
		return 'capacity'

	if '﻿AS OF' in first_header.upper():
		return 'summary'

	if first_header == 'COVID-19 Details':
		return 'covid_details'

	# it's got a double dagger at the end? 
	if first_header.startswith('Hospitalized'): 
		return 'hospitalized'

files = (glob.glob("pages_from_archivedotorg/*.html"))
for file in files:
	filename = os.path.basename(file)
	print('processing %s '% file)

	result = re.search(date_re, filename)
	if result:
		
		date = str(result.group(1)) + '_' + str(result.group(2)) + '_' +  str(result.group(3))
		filebase = 'ohapageread_' + date + '.csv'
		print(date)


		raw_page = open(file, 'r').read()
		soup = BeautifulSoup(raw_page, features="html.parser")
		tables = soup.find_all('table')

		for i,table in enumerate(tables):

			# The first two table are added by archive.org, ignore 'em
			if i < 3:
				continue
			first_row = table.find_all('tr')[0]
			first_header = first_row.find_all('th')[0].text
			#print("%s -- %s" % (i, first_header))

			table_name = get_table_from_header(first_header, i)
			if table_name:
				print("Got table name %s" % table_name)

				outfile = "pages_parsed/" + table_name + "_" + filebase

				output_table(table,outfile)
			else:
				print("**No table for '%s'" % first_header)
		

