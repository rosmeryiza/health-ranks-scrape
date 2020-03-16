''' Web scraping project:
    Florida county health rankings from the last five years
'''
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv

# make selenium headless so chrome does not start every time
#chrome_options = Options()
#chrome_options.add_argument("--headless") 
# , options=chrome_options

# load driver from my path
driver = webdriver.Chrome('/Users/rosmeryiza/documents/python/scraping/chromedriver')

def get_county_urls(year):
    # get the web page 
    driver.get('https://www.countyhealthrankings.org/app/florida/' + year + '/rankings/outcomes/overall');
    # sleep timer lets the page load fully
    time.sleep(5)
    # page_source is a variable created by Selenium - it holds all the HTML
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")
    # get table that holds the county urls
    table = soup.find('table')
    # get rows that contain county names
    rows = table.find_all('td', class_="county")
    # empty list to hold county urls
    url_list = []
    # get links from each county row
    for row in rows:
        # get county a tag
        county = row.find('a')
        # add url to list of urls
        url_list.append(county.attrs['href'])
    #testing lines
    #print(url_list)
    #print(len(url_list))
    return url_list

def scrape_ranks(url):
        # get the web page 
        driver.get(url)
        # sleep timer lets the page load fully
        time.sleep(4)
        # page_source is a variable created by Selenium - it holds all the HTML
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        #list to write to csv file
        csvrow_list = []
        # find header that contains the county name
        name = soup.find('h2', class_="county-name")
        # add clean county name to csv row list
        csvrow_list.append(name.text.strip())
        #find the table that contains the ranks
        table = soup.find('table', class_="snapshot-data")
        # find the rows within the table that contain the rankings
        rows = table.find_all('tr')
        # holder list for messy list with blanks
        first_list = []
        # get the all rankings from the cells with rank class 
        for row in rows:
            cell = row.find('td', class_="rank")
            try:
                    first_list.append(cell.text.strip())
            except:
                pass
        #loop to clean up blanks from raw text because of weird format
        for f in first_list:
                    if (f != ''):
                        csvrow_list.append(f)
        #testing line
        #print(csvrow_list)
        return (csvrow_list)

def write_csv(county_urls):
    #create csv file
    file = open('countyhealth.csv', 'w')
    # make a Python CSV writer object
    csvwriter = csv.writer(file)
    # write the column headings row 
    csvwriter.writerow(['County Name', 'Health Outcomes', 'Length of Life', 'Quality of Life', 'Health Factors', 'Health Behaviors', 'Clinical Care', 'Social & Economic Factors', 'Physical Environment', 'Year'])
    # insert a 1-second time delay inside the loop 
    # write new rows into the CSV one by one
    for url in county_urls:
        row_list = scrape_ranks('https://www.countyhealthrankings.org' + url)
        # creatively get the year from the url by indexing the string
        year = url[13] + url[14] + url[15] + url[16]
        row_list.append(year)
        time.sleep(1)
        csvwriter.writerow(row_list)
    # close the file - end of function 
    file.close()

#make a list of years to insert into urls
years_list = ['2019', '2018', '2017', '2016', '2015']
#call get_county_urls and feed list of years into it. save county urls in list
all_urls = []

for year in years_list:
    county_urls = get_county_urls(year)
    for url in county_urls:
        all_urls.append(url)

# pass in ALL county urls to write function 
write_csv(all_urls)