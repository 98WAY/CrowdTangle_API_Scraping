# Scrape public posts from a list with CrowdTangle API
A Python Scraping script to store CrowdTangle data into SCV file

## Usage

### Scrape.py
ct_get_posts(count = 100, start_date = None, end_date = None, include_history= None,
                 sort_by='date', types=None, search_term=None, timeframe=None,
                 min_interactions = 0, offset = 0, api_token=None, listid=None) :
                 modified based on PyCrowdTangle [https://pypi.org/project/PyCrowdTangle],
                 retrieve public posts through CrowdTangle API with given token, listid
                 and other constraints, return a list containing json data as result
                 
fetch_all_posts(token, list_id, count_per_request, start_date, end_date):          
                retrieve all public posts from a list in the time interval between start_date
                and end_date, return a list

### Write_to_CSV.py
create(filename:str): create a csv file

write_to_csv(result: list, filename: str): write
