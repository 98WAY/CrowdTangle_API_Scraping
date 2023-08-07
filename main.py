# -*- coding: utf-8 -*-
from Write_to_CSV import write_to_csv
from Write_to_CSV import create
from Scrape import fetch_all_posts
import datetime
from itertools import groupby
import pytz
from collections import Counter
from collections import defaultdict

def fetch_and_write_posts(start_date, end_date, token, list_id, count_per_request, filename):
# save all public posts of a list into a csv file
    while start_date <= end_date:
        # Set the start_date and end_date for the current month
        current_start_date = start_date

        if start_date.month == 12:
            current_end_date = datetime.date(start_date.year + 1, 1, 1)
        elif start_date.month == 6 and start_date.year == 2023:
        # modify the date to avoid exceed the end_date, in this example case is 2023-06-22 00:00:00
            current_end_date = datetime.date(start_date.year, start_date.month, 22)
        else:
            current_end_date = start_date.replace(month=start_date.month+1, day=1)

        # Call the fetch_all_posts function with the current date range
        result_posts = fetch_all_posts(token, list_id, count_per_request, current_start_date, current_end_date)
        print(len(result_posts))
        # Process the retrieved posts as needed
        write_to_csv(result_posts, filename)

        # Increment the start_date to the next month
        if start_date.month == 12:
            start_date = datetime.date(start_date.year + 1, 1, 1)
        else:
            start_date = start_date.replace(month=start_date.month+1, day=1)

def group_data_by_fb_account(sorted_file):
    print(f"Start grouping file {sorted_file}")
    data = []
    with open(sorted_file, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) 
        for row in reader:
            data.append(row)
    # Group the data by the "FB_account" column
    grouped_data = {}
    for row in data:
        fb_account = row[0]
        if fb_account not in grouped_data:
            grouped_data[fb_account] = []
        grouped_data[fb_account].append(row)

    grouped_filename = f"grouped_{sorted_file}"
    with open(grouped_filename, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for fb_account in grouped_data:
            rows = grouped_data[fb_account]
            writer.writerows(rows)
    print(f"Data grouped by FB_account and saved to {grouped_filename}.")


def sort_data_by_post_created(filename):
    print(f"Start sorting file {filename}")
    data = []
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        for row in reader:
            data.append(row)
    sorted_data = sorted(data, key=lambda x: x[11], reverse=True)
    sorted_filename = f"sorted_{filename}"
    with open(sorted_filename, "w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(sorted_data)
    print(f"Data sorted by Post Created and saved to {sorted_filename}.")
    
def add_us_eastern_time_column(filename):
    #add US/Eastern time column to the file
    eastern_tz = pytz.timezone('US/Eastern')
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  
        date_index = header.index('Post Created Date')
        time_index = header.index('Post Created Time')
        new_header = header + ['Post Created (US Eastern Time)']
        rows = []
        for row in reader:
            post_date_str = row[date_index]
            post_time_str = row[time_index]
            post_datetime_str = f"{post_date_str} {post_time_str}"
            post_datetime = datetime.strptime(post_datetime_str, '%Y-%m-%d %H:%M:%S')
            post_datetime_utc = pytz.utc.localize(post_datetime)

            # Convert the UTC time to US Eastern Time
            post_datetime_est = post_datetime_utc.astimezone(eastern_tz)
            post_datetime_est_str = post_datetime_est.strftime('%Y-%m-%d %H:%M:%S')
            row.append(post_datetime_est_str)
            rows.append(row)

    new_filename = f"modified_{filename}"
    with open(new_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(new_header)  
        writer.writerows(rows) 
    print(f"US Eastern Time column added and saved to {new_filename}.")
 
def filter_data_by_date_range(filename):
#filter the file based on the time range
    start_date = datetime(2020, 1, 1, 0, 0, 0)
    end_date = datetime(2023, 6, 20, 23, 59, 59)

    filtered_rows = []

    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)
        time_index = header.index('Post Created (US Eastern Time)')

        for row in reader:
            post_time_str = row[time_index]
            post_time = datetime.strptime(post_time_str, '%Y-%m-%d %H:%M:%S')
            if start_date <= post_time <= end_date:
                filtered_rows.append(row)

    filtered_filename = f"filtered_{filename}"
    with open(filtered_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(header)  # Write the header row
        writer.writerows(filtered_rows)  # Write the filtered rows
    print(f"Data filtered by date range and saved to {filtered_filename}.")


if __name__ == '__main__':
    start_date = datetime.date(2019, 12, 31)
    end_date = datetime.date(2023, 6, 22)
    token = " " #"APIKEY"
    list_id = 1779953 # 1780534
    count_per_request = 100
    filename = 'extracted_pages.csv' # 'extracted_pages.csv'
    create(filename)
    fetch_and_write_posts(start_date, end_date, token, list_id, count_per_request, filename)
    #filename = "extracted_groups.csv"
    #filename = "extracted_pages.csv"
    #sort_data_by_post_created(filename)
    #group_data_by_fb_account("sorted_extracted_pages.csv")
    #group_data_by_fb_account("sorted_extracted_groups.csv")
    #add_us_eastern_time_column("sorted_extracted_pages.csv")
    #add_us_eastern_time_column("sorted_extracted_groups.csv")
    #filter_data_by_date_range('modified_sorted_extracted_pages.csv')
    #filter_data_by_date_range('modified_sorted_extracted_groups.csv')
