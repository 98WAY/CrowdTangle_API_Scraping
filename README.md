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
create(filename:str): create a csv file

write_to_csv(result: list, filename: str): write
