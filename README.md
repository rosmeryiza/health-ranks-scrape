# Scraping County Health Rankings

This scraping project is designed to get the health rankings for Florida counties throughout the past five years. The goal is to format the health rankings into a csv with their respective year, county, and the health rankings. 

## Functions

### `def get_county_urls()`
This function is designed to get the partial urls of each county in order to scrape them in the following function. The function finds the `table` containing the county names and their links, grabs the link in the `href` attribute and stores the links in a list. The function returns that list to be stored into a variable that will be passed into another function designed to scrape the individual pages.

### `def scrape_ranks()`
This function is designed to scrape the individual county pages and return the county name and its rankings. The name of the county comes from the `h2` element on the page with `class = "county-name"` That is then appended to a `csvrow_list` that will eventually contain the name along with the rankings. The function then goes on to get the table element with `class = snapshot-data` that contains the rankings. To get the rankings, the function loops through the rows and grabs the elements with `class = "rank"` and then returns the list to write to the csv.

### `def write_csv()`
This function writes the elements from the page to the csv. It first creates the column headings, and then it loops through the county partial urls that were grabbed with `def get_county_urls()` and calls `def scrape_ranks()` to scrape the pages.

### Errors and debugging
I ran into an error after scraping the rankings. The numbers were surrounded by blanks and to fix that issue I first added the ranks and blanks to a list, using the `.strip()` method to get it as clean as possible. Once I did that, I created a for loop to iterate through the draft list and checked for blanks using an if-statement. Using `csvrow_list.append(f)` I added the non-blank values to the list for the csv file.
Additionally, the pages take a few seconds to load sometimes, meaning that if the page isn't loading and you begin scraping, you will either get a 0 value, NoneType error, or for the county pages it will scrape "Loading county..." instead of the page elements. To avoid this, I added sleep timers after Selenium fetches the page, to give the page time to load entirely.
Another problem I ran into was getting the year for the county page to write into the csv. I solved this creatively by indexing the url string to get the year from that string. I originally planned to scrape it, but found that the year was in a select field that was difficult to grab.

## Calling Functions
To call the functions logically, I began by creating a list of years consisting of the last five years. I then called the get_county_urls function in a loop to iterate through the years list so I can get 67 urls for five different years. Totalling in 335 urls. I created a list that would contain all the 335 urls `all_urls` and appended the 67 urls from each year each time. Then the `all_urls` list is passed into the `write_csv` function to scrape 335 county pages.