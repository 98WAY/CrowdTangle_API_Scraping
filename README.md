# Scrape public posts from a list with CrowdTangle API
A Python Scraping script to store CrowdTangle data into SCV file

## Usage

### Scrape.py
ct_get_posts() : modified based on PyCrowdTangle [https://pypi.org/project/PyCrowdTangle],
                 retrieve public posts through CrowdTangle API with given token, listid
                 and other constraints, return a list containing json data as result
                 
fetch_all_posts():  retrieve all public posts from a list in the time interval between start_date
                    and end_date, return a list

### Write_to_CSV.py
create(): create a csv file

write_to_csv(): write data from fetch_all_posts() to csv file, the default timezone of the [post time data is UTC

## Example
main.py under CT_Scrape shows an example to scrape all public posts ranging from 2019/12/31 to 2023/06/22 based on UTC timezone with given
CrowdTangle API token and list id of potential extremist pages or groups.
Further data process are in Dtaprocess branch.
