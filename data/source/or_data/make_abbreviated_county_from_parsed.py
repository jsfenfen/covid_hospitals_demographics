import csv
import glob
import os
import datetime
import json



if __name__ == "__main__":



    # lookup counties by name after text munging
    county_lookup = {}

    # county / state / pop lookup file
    county_pops = {}

    def get_county(county_name):
        result = None
        try:
            result = county_lookup[county_name]
        except KeyError:
            #print("Not found")
            pass
        return result

    # deaths and cases keyed off of fips
    deaths_return = {}
    cases_return = {}
    negatives_return = {}

    def read_counties():
        infile = '/Users/jacob/github-whitelabel/covid_hospitals_demographics/djangoapp/pop_hosp_data/oregon/data/orcounties.csv'

        with open(infile) as csvfile:

            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("read counties %s" % row['county'])
                county_lookup[row['county']] = row['statecountyfips']
                cases_return[row['statecountyfips']] = row
                

    def prune_keys(dict):
        new_dict = {}
        for key in dict.keys():
            if key.startswith("202"):
                print("prune keys %s" % key)
                key_parts = key.split("_")
                year = int(key_parts[0])
                month_num = int(key_parts[1])
                if month_num > 11 or year == 2021 :
                
                    raw_dict = dict[key]
                    del(raw_dict['c'])
                    del(raw_dict['d'])
                    del(raw_dict['n'])
                    try:
                        del(raw_dict['n_n'])
                    except KeyError:
                        pass
                    new_dict[key] = raw_dict


                else:
                    print("skipping key %s" % key)
                    pass



            else:
                new_dict[key] = dict[key]
        return new_dict



    def read_populations():
        infile = '/Users/jacob/github-whitelabel/covid_hospitals_demographics/data/source/or_data/psu_population_projections_2019/psu_pops_cbsa.csv'

        with open(infile) as csvfile:

            reader = csv.DictReader(csvfile)
            for row in reader:
                #print("read county pop %s" % row['fips'])
                county_pops[row['fips']] = row

    read_counties()

    read_populations()
    

    datestrings = {}


    files = (glob.glob("pages_parsed/county_ohapageread_*.csv"))
    for file in sorted(files):
        
        filename = os.path.basename(file)
        print("\n\n\nProcessing file %s" % filename)

        infile = open(file, 'r')
        reader = csv.reader(infile)

        datestring = file.split('county_ohapageread_')[1]
        datestring = datestring.replace(".csv", "")
        print("Datestring %s" % datestring)


        try:
            datestrings[datestring]
        except KeyError:
            datestrings[datestring] = 1

        for i,row in enumerate(reader):
            if i > 0:
                #print(row)
                # ['County', 'Number of cases', 'Deaths', 'Negative test results']


                county_fips = get_county(row[0])

                if not county_fips:
                    continue
                
                


                cases = row[1]
                deaths = row[2]
                negatives = '0'



                try:
                    negatives = row[3]
                except IndexError:
                    pass

                if county_fips == '41000':
                    print (negatives)

                
                try: 
                    negatives = int(negatives.replace(',',''))
                except ValueError:
                    print("\n****\n pending negatives wtf")
                    negatives = -999

                if county_fips == '41000' and datestring in ['2020_05_23', '2020_05_24', '2020_05_25']:
                    print("Statewide first iteration %s negatives %s" % (datestring, negatives))


                print(row)
                cases_return[county_fips][datestring] = {'c':int(cases.replace(',','')),'d':int(deaths.replace(',','')),'n':negatives}
                


    ## Now that all the data is in, calculate the new deaths and new cases. 
    all_datestrings = list(datestrings.keys())
    all_datestrings.sort()
    #print(all_datestrings)

    county_list = list(county_lookup.keys())
    county_list.sort()
    county_fips_list = [county_lookup[i] for i in county_list]

    #print(cases_return)
    for i,datestring in enumerate(all_datestrings):
        print("Handling date %s" % datestring)

        if i > 0:
            datestring_parts = datestring.split('_')
            snapshot_date = datetime.datetime(int(datestring_parts[0]), int(datestring_parts[1]), int(datestring_parts[2]))
            prior_day = snapshot_date - datetime.timedelta(days=1)

            prior_datestring = prior_day.strftime("%Y_%m_%d") 

            #print("prior day %s" % prior_datestring)


        for countyfips in county_fips_list:
            

            try:
                todays_data = cases_return[countyfips][datestring]

                if countyfips == '41000':
                    print("statewide: %s" % todays_data)

            except KeyError:
                #print("missing %s %s" % (countyfips, datestring))
                todays_data = {'c':0,'d':0,'n':0}
                #print("adding to: %s" % cases_return[countyfips])
                cases_return[countyfips][datestring] = todays_data

            if i > 0:
                yesterdays_data = cases_return[countyfips][prior_datestring]


                todays_data['n_c'] = todays_data['c'] - yesterdays_data['c']
                todays_data['n_d'] = todays_data['d'] - yesterdays_data['d']


                if todays_data['n'] == -999:
                    # hack for state's april 22 data problem
                    #print("Dealing with april 22 data problem ")
                    todays_data['n_n'] = 0
                    todays_data['n'] = yesterdays_data['n']
                else:
                    todays_data['n_n'] = todays_data['n'] - yesterdays_data['n']
                
                cases_return[countyfips][datestring] = todays_data


    ## Calculate the metro areas


    CBSA_list = ['38900','41420']


    for cbsa in CBSA_list:

        cases_return[cbsa] = {"countyfips": cbsa, "cbsacode":""}
        
        for i,datestring in enumerate(all_datestrings):
            #print("Handling date %s" % datestring)
            c = 0
            n_c = 0
            d = 0 
            n_d = 0
            n = 0
            n_n = 0

            for county_fips in list(cases_return.keys()):
                this_cbsa_code = cases_return[county_fips]['cbsacode']
                if this_cbsa_code == cbsa:
                    #print("county fips %s datestring %s" % (county_fips, datestring))
                    c += cases_return[county_fips][datestring]['c']
                    d += cases_return[county_fips][datestring]['d']
                    n += cases_return[county_fips][datestring]['n']
                    if i>0:
                        n_c += cases_return[county_fips][datestring]['n_c']
                        n_d += cases_return[county_fips][datestring]['n_d']
                        n_n += cases_return[county_fips][datestring]['n_n']

            this_date_data = {
                'c':c,
                'd':d,
                'n':n,
                'n_c':n_c,
                'n_d':n_d,
                'n_n':n_n
            }
            cases_return[cbsa][datestring] = this_date_data

            
    ## Add population estimates too. 


    key_list = ['fips','name','county_cbsa','pop','age_0_17','fraction_0_17','age_18_64','fraction_18_64','age_65_over','fraction_65_over']
    for key in cases_return:

        this_county_pop = county_pops[key]
        for popkey in key_list:
            cases_return[key][popkey] = this_county_pop[popkey]










    outfile2 = "coviddata_abbreviated.js"

    new_dict = {}
    for key in cases_return.keys():
        new_dict[key] = prune_keys(cases_return[key])

    with open(outfile2, 'w') as outfilehandle:
        outfilehandle.write("export default ")
        json.dump(new_dict, outfilehandle)





    #print(cases_return)
    outfile = "coviddata-state-abbreviated.js"
    state_dict = {};
    state_dict['41000'] = new_dict['41000']

    with open(outfile, 'w') as outfilehandle:
        outfilehandle.write("export default ")
        json.dump(state_dict, outfilehandle)

