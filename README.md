# MCA-CSR-Scraper

## Description

This Python script uses BeautifulSoup to scrape Article 135 disclosures from the Indian Ministry of Corporate Affairs (MCA) CSR database at https://csr.gov.in/CSR/master_search.php. It returns disclosures from the 2014-15, 2015-16, and 2016-17 fiscal years. I will update the script when 2017-18 disclosures are added to the MCA database.

## Usage

The scraper takes up to two command line arguments: a mandatory argument containing a local path to a .csv file; and an optional argument to enable a test mode:

`> python3.x mca_scrape.py [input] [options]`

It is good practice for the user to update the `headers` variable to include their name and contact information prior to running the scraping procedure. Example:

`headers = {'user-agent': 'Intel_Mac_OSX 10_14_3; John Doe/Anywhere, US; john@doe.com'}`

There is a one-second delay between requests.

### Input CSV Format
The input .csv file must have a column labeled `cin`, containing Indian corporate identity numbers (CINs). Optionally, the file may also include a column labeled `company_name`, in which case the company names provided by the user will be included in the output. Any other columns in the file will be ignored.

The script will pass over any CIN that is not 21 characters in length and that does not begin with L or U, since these irregular CINs are not currently included in the MCA database. Such CINs will be recorded in the exceptions file returned by the script at the end of its run.

### Test mode
Providing a `-t` option at the command line enables a test mode. Under this mode, the scraper will collect data for only the first ten CINs in the input file.

### Example

`> python3.7 mca_scrape.py ./examples/csr_top_100.csv -t`

## Output

The scraper produces two files at the end of its run: a .csv file containing the CSR disclosures, and a .csv file listing CINs that produced exceptions during the scraping procedure.

## Included CSV and output files

The `examples` folder includes three files:
 * `csr_top_100.csv` includes CINs and company names of 100 entities, ranked by their total CSR spending from FY 2014-15 to FY 2016-17. This is based on CSR spending reported in company standalone annual reports, which I have aggregated from the ProwessDx dataset. Note that not all of these companies are included in the MCA data; in particular, those with irregular CINs are not in the database. The scraper excludes these during its run and notes their CINs as exceptions;

 * `csr_top_100_results.csv` contains the results output of the script, as collected on January 29, 2019;

 * `csr_top_100_exceptions.csv` contains the exceptions recorded during the script's run.

## Notes, known issues, and areas for improvement:

_Exceptions / connection issues_:
* The connection to the MCA website occasionally fails, in which case an exception is recorded and the script continues. The exceptions file can be fed back into the script to collect any additional data that was missed due to connection issues. Future versions will improve the robustness of handling connection errors;
* The exceptions file currently records only the CIN, not the company name or nature of the error.
