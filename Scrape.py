# -*- coding: utf-8 -*-
# import modules
import requests
import pandas as pd
import json
import time


def ct_get_posts(count = 100, start_date = None, end_date = None, include_history= None,
                 sort_by='date', types=None, search_term=None, timeframe=None,
                 min_interactions = 0, offset = 0, api_token=None, listid=None):
    """Retrieve a set of posts for the given parameters get post from crowdtangle 

    Args:
        count (int, optional): The number of posts to return. Defaults to 100. options [1-100]
        start_date (str, optional): The earliest date at which a post could be posted. Time zone is UTC. 
                                    Format is “yyyy-mm-ddThh:mm:ss” or “yyyy-mm-dd” 
                                    (defaults to time 00:00:00).
        end_date (str, optional): The latest date at which a post could be posted.
                                  Time zone is UTC. Format is “yyyy-mm-ddThh:mm:ss”
                                  or “yyyy-mm-dd” (defaults to time 00:00:00).
                                  defaults to "now". 
                                  At most one year from start_date to end_date
        include_history (str, optional): Includes timestep data for growth of each post returned.
                                         Defaults to null (not included). options: 'true'
        sort_by (str, optional): The method by which to filter and order posts.
                                options: 'date', 'interaction_rate', 'overperforming',
                                'total_interactions', 'underperforming'.
                                defaults 'date'
        min_interactions (int, optional): If set, will exclude posts with total interactions 
                                          below this threshold. options int > 0, default 0
        offset (int, optional): The number of posts to offset (generally used for pagination). 
                                Pagination links will also be provided in the response.                                                          
        types (str, optional):  The types of post to include. These can be separated by commas 
                                to include multiple types. If you want all live videos 
                                (whether currently or formerly live), be sure to include both 
                                live_video and live_video_complete. The "video" type does not 
                                mean all videos, it refers to videos that aren't native_video,
                                youtube or vine (e.g. a video on Vimeo).   
                                options: "episode", "extra_clip", "link", "live_video", 
                                "live_video_complete", "live_video_scheduled", "native_video",
                                "photo", "status", "trailer","video", "vine", "youtube"  
                                default all
        search_term (str, optional): Returns only posts that match this search term. 
                                     Terms AND automatically. Separate with commas for OR, 
                                     use quotes for phrases. E.g. CrowdTangle API -> AND. 
                                     CrowdTangle, API -> OR. "CrowdTangle API" -> AND in that
                                     exact order. You can also use traditional Boolean search
                                     with this parameter. default null                                                                                                                         
        api_token (str, optional): you can locate your API token via your crowdtangle dashboard
                                   under Settings > API Access.
    Returns:
        List: result_posts will be a list containing the fetched posts from the API. Each post 
                in the list will be represented as a dictionary or JSON object.
                The status will always be 200 if there is no error. The result contains an array of post objects and
                a pagination object with URLs for both the next and previous page, if they exist
                
    """
    # api-endpoint
    URL_BASE = "https://api.crowdtangle.com"
    endpoint = "/posts"
    # defining a params dict for the parameters to be sent to the API
    PARAMS = {'count': count, 'sortBy':sort_by, 'token': api_token, 
              'minInteractions': min_interactions, 'offset': offset, 'listIds': listid}

    # add params parameters
    if start_date:
        PARAMS['startDate'] = start_date
    if end_date:
        PARAMS['endDate'] = end_date
    if include_history == 'true':
        PARAMS['includeHistory'] = include_history
    if types:
        PARAMS['types'] =  types
    if search_term:
        PARAMS['searchTerm'] =  search_term 
    if timeframe:
        PARAMS['timeframe'] =  timeframe 

    # sending get request and saving the response as response object
    try:
        r = requests.get(url=URL_BASE + endpoint, params=PARAMS)
        if r.status_code != 200:
            out = r.json()
            print(f"status: {out['status']}")
            print(f"Code error: {out['code']}")
            print(f"Message: {out['message']}")
        return r
    except Exception as e:
        print(f"Something went wrong. Exception: {e}")
        return None


def fetch_all_posts(token, list_id, count_per_request, start_date, end_date):
    #Retrieve all posts from a list based on the given date interval
    posts = []
    next_page = None

    while True:
        if next_page:
            response = requests.get(next_page)
            time.sleep(10)
        else:
            # make an initial request to retrieve the first batch of posts
            response = ct_get_posts(count=count_per_request, start_date=start_date, end_date=end_date, listid=list_id, api_token=token)
            time.sleep(10)

        if response.status_code == 200:
            data = response.json()
            posts.extend(data['result']['posts'])
            next_page = data['result']['pagination'].get('nextPage', None)
            if not next_page:
                break
        else:
            print(f"Something went wrong. Status: {response.json().get('status')}")
            break

    return posts
