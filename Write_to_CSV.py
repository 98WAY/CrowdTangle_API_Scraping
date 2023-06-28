# -*- coding: utf-8 -*-
import csv
import os

def create(filename:str):
    # Define the desired column names
    columns = [
        'FB_account', 'FB_ID', 'FB_platformID', 'FB_handle', 'Original_name', 'Page Category', 
        'Account Type', 'Now Subscriber', 'Page Admin Top Country', 'Page Description', 'Page Created',
        'Post Created', 'Post Created Date', 'Post Created Time', 'Type', 'Total Interactions',
        'Likes', 'Comments', 'Shares', 'Love', 'Wow', 'Haha', 'Sad', 'Angry', 'Thankful',
        'Care', 'URL', 'Message', 'Link', 'Final Link', 'Link Text', 'Description', 'Past Subscriber',
        'Overperforming Score'
    ]
    
    file_exists = os.path.exists(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the column headers if the file doesn't exist
        if not file_exists:
            writer.writerow(columns)
            print(f'{filename} created successfully.')
        else:
            print(f'{filename} already exists.')


# Extract data from the result list
def write_to_csv(result: list, filename: str):
    # Create a list to store the extracted data
    data = []
    
    # Iterate over the posts and extract the desired information
    for post in result:
        account = post['account']
        statistics = post['statistics']['actual']
        expanded_links = post.get('expandedLinks', [{}])
        expanded = expanded_links[0].get('expanded', '')
        #extract data
        like = statistics['likeCount']
        comment = statistics['commentCount']
        share = statistics['shareCount']
        love = statistics['loveCount']
        wow = statistics['wowCount']
        haha = statistics['hahaCount']
        sad = statistics['sadCount']
        angry = statistics['angryCount']
        thankful = statistics['thankfulCount']    
        care = statistics.get('careCount',0)
        Total_Interaction = like+comment+share+love+wow+haha+sad+angry+thankful+care
        
        
        post_data = [
            account.get('name', ''),
            account.get('id', ''),
            account.get('platformId', ''),
            account.get('handle', ''),
            account.get('originalName', ''),
            account.get('pageCategory', ''),
            account.get('accountType', ''),
            account.get('subscriberCount', ''),
            account.get('pageAdminTopCountry', ''),
            account.get('pageDescription', ''),
            account.get('pageCreatedDate', ''),
            post.get('date', ''),
            post.get('date', '').split()[0],
            post.get('date', '').split()[1],
            post.get('type', ''),
            Total_Interaction,
            like,
            comment,
            share,
            love,
            wow,
            haha,
            sad,
            angry,
            thankful,
            care, 
            post.get('postUrl', ''),
            post.get('message', ''),
            post.get('link', ''),
            expanded,
            post.get('title', ''),
            post.get('description', ''),
            post.get('subscriberCount', ''),
            post.get('score', '')
        ]
        data.append(post_data)
    
    # Write the extracted data to a CSV file    
    with open(filename, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # Write the data rows
        writer.writerows(data)
    
    print(f'Data extracted and saved to {filename}.')
