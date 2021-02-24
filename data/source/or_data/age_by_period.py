from datetime import date, timedelta
import csv


start_date = date(2020,4,11)
#week = timedelta(weeks=1)
week = timedelta(days=1)
day = timedelta(days=1)

today = date.today()

calculation_date = start_date
iteration = 0



headers = ['weeknumber', 'date',
'60_to_69_death_new','70_to_79_death_new','80_and_over_death_new', 'Total_death_new', '0_to_9_cases_new', '10_to_19_cases_new','20_to_29_cases_new','30_to_39_cases_new','40_to_49_cases_new','50_to_59_cases_new', '60_to_69_cases_new','70_to_79_cases_new','80_and_over_cases_new', 'Total_cases_new', 'case_prcnt_0_to_9','case_prcnt_10_to_19','case_prcnt_20_to_29','case_prcnt_30_to_39','case_prcnt_40_to_49','case_prcnt_50_to_59','case_prcnt_60_to_69','case_prcnt_70_to_79','case_prcnt_80_and_over']

def clean_raw_stats(stat):
    stat = stat.replace(",","")
    stat = stat.replace("-","0")
    return int(stat)

def read_file(filename):
    try:
        infile = open(filename, 'r')
    except FileNotFoundError:
        return None

    reader = csv.reader(infile)

    todays_rates = {}

    for i,row in enumerate(reader):

   
        if i > 0:


            age_group_stats = {}

            age_group_stats['cases'] = clean_raw_stats(row[1])
            age_group_stats['hosp'] = clean_raw_stats(row[3])
            age_group_stats['death'] = clean_raw_stats(row[4])


            todays_rates[row[0]] = age_group_stats

    reformatted = {}
    for key in todays_rates:
        for key2 in todays_rates[key]:


            new_key = key.replace(" ", "_") + '_' + key2
            reformatted[new_key] = todays_rates[key][key2]



    return reformatted






outputfile = "age_percents_days.csv"
outfh = open(outputfile, 'w')
writer = csv.DictWriter(outfh, fieldnames=headers, restval='', extrasaction='ignore')
writer.writeheader()


collated_results = []

while calculation_date < today:
    print("Handling iteration " + str(iteration) + " date " + str(calculation_date))

    if iteration == 43:
        # president's day, 2/6, there was no data, use 2/7
        print("Using 2/7 instead of 2/6")
        calculation_date += day

    datestring = calculation_date.strftime('%Y_%m_%d')
    filename = "pages_parsed/age_group_ohapageread_%s.csv" % datestring

    #print("\n\n\nProcessing file %s" % filename)
    result = None

    result = read_file(filename)
    if not result:
        iteration += 1
        calculation_date += week
        continue

    varnames = list(result.keys())


    if iteration > 0:
        last_week = collated_results[-1]

        for var in varnames:
            new_name = var + "_new"
            try:
                result[new_name] = result[var] - last_week[var]
            except KeyError:
                result[new_name] = -999

        print("%%%%%")
        print("result is %s" % result)
        print("%%%%%")

        for key in ['0_to_9_cases_new','10_to_19_cases_new','20_to_29_cases_new','30_to_39_cases_new','40_to_49_cases_new','50_to_59_cases_new','60_to_69_cases_new','70_to_79_cases_new','80_and_over_cases_new']:

            new_key = key
            new_key = new_key.replace("_cases_new", "")
            new_key = "case_prcnt_" + new_key
            print("Adding key %s" % new_key)

            try:
                if result['Total_cases_new'] > 0 and result[key] >= 0: 
                    result[new_key] = 100*(0.0+result[key]/result['Total_cases_new'])
                else:
                    result[new_key] = 0

            except KeyError:
                print("Missing key %s" % key)

    # add these
    result['weeknumber'] = iteration
    result['date'] = str(calculation_date)


    print(result)
    collated_results.append(result)

    if iteration > 20 and result['Total_cases_new'] > 0:
        writer.writerow(result)



    iteration += 1
    calculation_date += week