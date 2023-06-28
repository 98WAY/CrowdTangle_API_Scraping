# -*- coding: utf-8 -*-
from Write_to_CSV import write_to_csv
from Write_to_CSV import create
from Scrape import ct_get_posts
from Scrape import fetch_all_posts
import json
import datetime

if __name__ == '__main__':
    #retrieve data from 2019-12-31 00:00:00 to 2023-06-21 23:59:59 based on UTC timezone
    start_date = datetime.date(2019, 12, 31)
    end_date = datetime.date(2023, 6, 22)
    token = ""
        #"Tm3mU0VqFtchygsnOILeKjiYaynKqWsWZpnyvYpn"
    list_id = 12345678
        #1780534
    count_per_request = 100

    create('extracted_groups.csv')
    
    
while start_date <= end_date:
    # Set the start_date and end_date for the current month
    current_start_date = start_date

    if start_date.month == 12:
        current_end_date = datetime.date(start_date.year + 1, 1, 1)
    elif start_date.month == 6 and start_date.year == 2023:
        current_end_date = datetime.date(start_date.year, start_date.month, 22)
    else:
        current_end_date = start_date.replace(month=start_date.month+1, day=1)

    # Call the fetch_all_posts function with the current date range
    result_posts = fetch_all_posts(token, list_id, count_per_request, current_start_date, current_end_date)
    print(len(result_posts)) 
    # Process the retrieved posts as needed
    write_to_csv(result_posts, 'extracted_groups.csv')

    # Increment the start_date to the next month
    if start_date.month == 12:
        start_date = datetime.date(start_date.year + 1, 1, 1)
    else:
        start_date = start_date.replace(month=start_date.month+1, day=1)
