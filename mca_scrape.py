
# Scrapes CSR project data from Ministry of Corporate Affairs (India) website
# Samuel Frantz / George Washington University / sfrantz@gwu.edu

import requests, bs4, time, re
import pandas as pd
from sys import argv, exit

# User should provide a list of CINs and an optional test mode at the command line
if (len(argv) != 2 and len(argv) != 3):
    print("Usage: mca_scrape.py [input] [options]")
    exit(1)

# Import list of company identification numbers (CINs) and names
try:
    companies = pd.read_csv(argv[1], keep_default_na=False)
except:
    print("Unable to read file " + str(argv[1]))
    exit(1)

# Create lists to store the data and any exceptions encountered
csr_data=[]
exceptions = []

# List of CINs to cycle through

cinList = companies['cin'].tolist()

# Your info goes here
headers = {'user-agent': 'Intel_Mac_OSX 10_14_3'}

starturl='http://www.csr.gov.in/CSR/companyprofile.php?year=FY+2015-16&CIN='

# Set counter for accessing dataframe by index number
# Right now this is used only to extract 'company_name' from the CSV

counter = 0

#Define the scraping procedure
def get_projects(cin):

    # Is the CIN 21 characters starting with L or U?
    if (len(i) != 21 or (i[0] != 'L' and i[0] != 'U')):
        print('\n' + i + ' is not a valid CIN')
        exceptions.append(i)

    else:

        # Main procedure:

        try:

            url = (starturl + str(i))
            res = requests.get(url, headers=headers, timeout=7)
            print('')
            print('Connection status:', res.status_code, 'Company:', i)

            if res.status_code == 200:
                print('OK')

            else:
                print(i, ' returned status code ', res.status_code)

            # Extract data tables of CSR projects

            soup=bs4.BeautifulSoup(res.text, "html.parser")

            # 2014-15

            try:
                csr14_15 = soup.find_all('div',{"id":"colfy1"})
                tableRow14_15 = csr14_15[0].find_all('table',{"id":"datatable"})[0].find_all('tr')[1:-1]

                for tr in tableRow14_15:
                    td = tr.find_all('td')
                    row = [i.text for i in td][0:8]
                    row.append('2014-15')
                    row.append(i)
                    if 'company_name' in companies.columns:
                        row.append(companies['company_name'][counter])
                    csr_data.append(row)

            except:
                print('No projects listed for 2014-15')

            # 2015-16

            try:
                csr15_16 = soup.find_all('div',{"id":"colfy2"})
                tableRow15_16 = csr15_16[0].find_all('table',{"id":"datatable"})[0].find_all('tr')[1:-1]

                for tr in tableRow15_16:
                    td = tr.find_all('td')
                    row = [i.text for i in td][0:8]
                    row.append('2015-16')
                    row.append(i)
                    if 'company_name' in companies.columns:
                        row.append(companies['company_name'][counter])
                    csr_data.append(row)

            except:
                print('No projects listed for 2015-16')

            # 2016-17

            try:
                csr16_17 = soup.find_all('div',{"id":"colfy3"})
                tableRow16_17 = csr16_17[0].find_all('table',{"id":"datatable"})[0].find_all('tr')[1:-1]

                for tr in tableRow16_17:
                    td = tr.find_all('td')
                    row = [i.text for i in td][0:8]
                    row.append('2016-17')
                    row.append(i)
                    if 'company_name' in companies.columns:
                        row.append(companies['company_name'][counter])
                    csr_data.append(row)

            except:
                print('No projects listed for 2016-17')

        except:
            print('Error encountered for CIN', i)
            exceptions.append(i)

    # Wait one second between requests
    time.sleep(1)

# Run the scraping procedure
# Run in test mode if -t argument provided at command line
if (len(argv) == 3 and argv[2] == '-t'):
    print("Test mode enabled: gathering up to first ten companies")
    if len(cinList) > 10:
        for i in cinList[0:9]:
            get_projects(i)
            counter += 1
    else:
        for i in cinList:
            get_projects(i)
            counter += 1

# Otherwise run in normal mode to collect data for all CINs in the CSV
else:
    for i in cinList:
        get_projects(i)
        counter += 1

# Create Pandas dataframe to store the results

if 'company_name' in companies.columns:
    cresults=pd.DataFrame(csr_data,columns=['id', 'proj_name', 'proj_sector', 'state', 'district', 'outlay', 'spent', 'mode', 'year', 'cin', 'company_name'])

else:
    cresults=pd.DataFrame(csr_data,columns=['id', 'proj_name', 'proj_sector', 'state', 'district', 'outlay', 'spent', 'mode', 'year', 'cin'])

# Save the dataframe as a timestamped CSV file

timestamp = time.strftime("%Y%m%d-%H%M%S")
cresults.to_csv('results_' + timestamp + '.csv', na_rep='.')
print('Results written to disk. Timestamp:',timestamp)

# Save a list of exceptions/errors, if there were any

if len(exceptions) > 0:
    exceptionsTable=pd.DataFrame(exceptions,columns=['cin'])
    exceptionsTable.to_csv('exceptions_' + timestamp + '.csv', na_rep='.')
    print('Exceptions file written to disk:', len(exceptions), 'exceptions noted.')
else:
    print('No exceptions/errors noted')

exit(0)
