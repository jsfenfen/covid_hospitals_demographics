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

## We may need to enter data retrospectively, but this is the simplest approach
# for dealing with occasional data issues--don't reimport the problematic files.

filebasestring = "backups/ohapage_2020_11*"


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

def output_table(data_table, outputfile, verbose=False):
	""" Writes a csv of just the table to a file """

	header_names = []
	data_rows = []

	rows = data_table.find_all('tr')

	for i, row in enumerate(rows):
		if i==0:
			colheaders = row.find_all('th')
			header_names = [clean_header(i.text) for i in colheaders]
			if verbose:
				print(header_names)

		else:
			data = row.find_all('td')
			data_fixed = [i.text for i in data]
			if verbose:
				print(data_fixed)
			data_rows.append(data_fixed)

	outfileh = open(outputfile, 'w')
	print ('writing to %s' % outputfile)
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

files.sort()

print(files[-1])

current_file = files[-1]
most_recent = False





for file in files:
	filename = os.path.basename(file)
	

	# allow an exception for the most current file, maybe? 
	if '_06_15.html' in filename or file == current_file:

		if file == current_file:
			most_recent = True
			print("\n\nProcessing most current ")
		else:
			most_recent = False

		filebase = filename.replace("ohapage_", "ohapageread_")


		

		filebase_raw = filebase
		filebase = filebase.replace("_06_15.html","")
		
		filebase_parts = filebase.split('_')
		snapshot_date = datetime.datetime(int(filebase_parts[1]), int(filebase_parts[2]), int(filebase_parts[3]))
		
			

		prior_day = snapshot_date

		if '_06_15.html' in filebase_raw:
			prior_day = prior_day - datetime.timedelta(days=1)
		else:
			prior_day = snapshot_date 

		print("prior day %s" % prior_day)

		weekday = prior_day.weekday() 
		print ("date: %s %s " % (int(filebase_parts[2]), int(filebase_parts[3])))

		if ( int(filebase_parts[2]) >= 6  and weekday >= 5 ):
			print("Skipping weekend %s" % snapshot_date)
			continue


		if ( int(filebase_parts[2]) == 7  and int(filebase_parts[3]) ==3 ):
			
			print("Skipping july 3 %s" % snapshot_date)
			continue

		if ( int(filebase_parts[2]) == 9  and int(filebase_parts[3]) ==8 ):
			
			print("Skipping labor day %s" % snapshot_date)
			continue

		print("\nProcessing file %s" % filebase)

		new_filebase = 'ohapageread_' + prior_day.strftime("%Y_%m_%d") + ".csv"

		filebase = new_filebase

		#print("filebase: %s" % filebase)


		raw_page = open(file, 'r').read()
		soup = BeautifulSoup(raw_page, features="html.parser")
		tables = soup.find_all('table')

		for i,table in enumerate(tables):

			first_row = table.find_all('tr')[0]

			try:
				first_header = first_row.find_all('th')[0].text
			except IndexError:

				print("Couldn't get header from first_row, table %s" % i)
				print("firt row is: %s" % first_row)
				continue

			table_name = ''
			
			print("\t|| processing table %s from %s %s" % (i,filebase_parts[2], int(filebase_parts[3]) ))

			if i == 0:
				table_name = 'summary'
				if most_recent:

					# Data current as of 4/20/2020, 8:00 a.m. Updated daily.
					fixed_header = first_header.replace('Updated daily.', '')
					fixed_header = fixed_header.strip(' ')
					print("Fixed header is " + fixed_header)

					day = prior_day.strftime("%d")
					day_string = day + prior_day.strftime("/%Y")
					month = prior_day.strftime("%m")
					day_string_fixed = str(month) + "/" + day_string
					print("day_string_fixed:   %s fixed_header: %s" % (day_string_fixed, fixed_header) )
					
					# make sure the most recent file has data for the correct day
					#assert day_string_fixed in fixed_header
			else:
				table_name = get_table_from_header(first_header, i)

			#print("%s -- %s --%s" % (i, first_header, table_name))

			if table_name:
				#print("Got table name %s" % table_name)

				outfile = "pages_parsed/" + table_name + "_" + filebase


				output_table(table,outfile, False)
			else:
				#print("**No table for '%s'" % first_header)
				pass



		

