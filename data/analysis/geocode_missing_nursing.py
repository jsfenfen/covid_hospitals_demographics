import csv
import re

import googlemaps

gmaps = googlemaps.Client(key='')
input_file = "../processed/nursing_gen_info.csv"

# Manually moved the file to nh_gen_info_geocoded_final.csv after complete so it doesn't overwrite
outfilehandle = open("../processed/nh_gen_info_geocoded.csv", 'w') # 

dw = None

reader = csv.DictReader(open(input_file, 'r'))
geocode_count = 0
for i, row in enumerate(reader):


	if i==0:
		headers = row.keys()
		dw = csv.DictWriter(outfilehandle, headers, extrasaction='ignore')
		dw.writeheader()

	if row['geocode_flag'] == '1' and not row['lat']:
		address = "%s %s %s, %s" % (row['Provider Address'], row['Provider City'], row['Provider State'], row['Provider Zip Code'])
		geocode_count += 1

		print ("%s: Need to geocode address %s" % (geocode_count, address))

		result = gmaps.geocode(address)
		try:
			row['lat'] = result[0]['geometry']['location']['lat']
			row['lng'] = result[0]['geometry']['location']['lng']
			row['geocode_accuracy'] = result[0]['geometry']['location_type']
			row['address'] = result[0]['formatted_address']
		except KeyError:
			print("missing in result " % result)

	dw.writerow(row)

print("Finished with %s geocodes" % geocode_count)


