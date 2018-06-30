
# Scrapes CSR project data from Ministry of Corporate Affairs (India) website
# Modified April 10, 2018
# Samuel Frantz / George Washington University / sfrantz@gwu.edu

import requests, bs4, time, re
import pandas as pd
from sys import argv

headers = {'user-agent': 'Intel_Mac_OSX 10_13_3; Samuel Frantz/Washington, DC sfrantz@gwu.edu'}

starturl='http://www.csr.gov.in/CSR/companyprofile.php?year=FY+2015-16&CIN='

# Import list of company identification numbers (CINs) and names
companies = pd.read_csv('companies_15_16.csv')

csr_data=[] # Main data file
exceptions = [] # Companies for which scraping errors encountered

# List of CINs to cycle through
cinList = companies['cin'].tolist()

# Define the scraping procedure

def get_projects(cin):
    try:
        url = (starturl + str(i))
        res = requests.get(url, headers=headers, timeout=7)
        print('')
        print('Connection status:', res.status_code, 'Company:', i)

        if res.status_code == 200:
            print('OK')
        else:
            print(i, 'returned status code', res.status_code)
            exceptions.append(i)
    except:
        print('')
        print('Results for', i, 'returned an error.')
        exceptions.append(i)

    try:

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
                csr_data.append(row)

        except:
            print('2014-15 results not found')

        # 2015-16

        try:
            csr15_16 = soup.find_all('div',{"id":"colfy2"})
            tableRow15_16 = csr15_16[0].find_all('table',{"id":"datatable"})[0].find_all('tr')[1:-1]

            for tr in tableRow15_16:
                td = tr.find_all('td')
                row = [i.text for i in td][0:8]
                row.append('2015-16')
                row.append(i)
                csr_data.append(row)

        except:
            print('2015-16 results not found')

        # 2016-17?

        try:
            csr16_17 = soup.find_all('div',{"id":"colfy3"})
            tableRow16_17 = csr16_17[0].find_all('table',{"id":"datatable"})[0].find_all('tr')[1:-1]

            for tr in tableRow16_17:
                td = tr.find_all('td')
                row = [i.text for i in td][0:8]
                row.append('2016-17')
                row.append(i)
                csr_data.append(row)

        except:
            print('2016-17 results not found')

    except:
        print('Error encountered for CIN', i)
        exceptions.append(i)

    time.sleep(1) # Wait one second between requests

# Run the scraping procedure
for i in cinList[0:99]: # Companies ranked 1-100 in CSR spending
    get_projects(i)

# Create Pandas dataframe

cresults=pd.DataFrame(csr_data,columns=['id', 'proj_name', 'proj_sector', 'state', 'district', 'outlay', 'spent', 'mode', 'year', 'CIN'])

# Save output (results and list of errors) as csv files

timestamp = time.strftime("%Y%m%d-%H%M%S")
cresults.to_csv('results_' + timestamp + '.csv', na_rep='.')
print('Results written to disk. Timestamp:',timestamp)

# Save list of exceptions/errors, if there were any

if len(exceptions) > 0:
    exceptionsTable=pd.DataFrame(exceptions,columns=['CIN'])
    exceptionsTable.to_csv('exceptions_' + timestamp + '.csv', na_rep='.')
    print('Exceptions file written to disk', len(exceptions), 'exceptions noted.')
else:
    print('No exceptions/errors noted')
