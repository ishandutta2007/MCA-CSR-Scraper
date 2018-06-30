# MCA-CSR-Scraper

## Description

This Python script uses BeautifulSoup to scrape Article 135 disclosures from the Indian Ministry of Corporate Affairs CSR database at https://csr.gov.in/CSR/master_search.php. It will return disclosures from the 2014-15, 2015-16, and 2016-17 fiscal years.

## Usage

The scraper takes a list of Company Identification Numbers (CINs) from a .csv file and queries the database for a user-defined range of these companies. For example, using the provided file `companies_15_16.csv`, defining a range of `0:99` will return the CSR disclosures of the top 100 companies, as ranked by spending in FY 2015-16. The range is currently defined within the script rather than through user input.

## Output

The scraper produces two files at the end of its run: a .csv file containing the CSR disclosures, and a .csv file listing CINs that produced exceptions during the scraping procedure. 

## Known issues

The scraper relies on the output tables on the MCA website being in a defined format. A few companies for which data is available nevertheless encounter exceptions in the scraper. I have not yet investigated what is causing these exceptions and whether they need to be addressed individually or if there is a more robust way to define the scraping procedure.



