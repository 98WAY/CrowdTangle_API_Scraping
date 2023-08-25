# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 16:28:22 2023

@author: wanha
"""
import csv
import json
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import time
import datetime


def analyze_post_content(input_file, output_file, api_key, target_column):
    # Initialize the client to interact with the Perspective API
    client = discovery.build(
        "commentanalyzer",
        "v1alpha1",
        developerKey=api_key,
        discoveryServiceUrl="https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1",
        static_discovery=False,
    )

    # Open the input and output CSV files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:

        # Initialize the CSV reader and writer
        reader = csv.DictReader(infile)
        fieldnames = ["Row_Number", "post_"+target_column, "scores", "languages", "detectedLanguages", "error"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Analyze each post description and write the results to the output file
        for row in reader:
            time.sleep(1) 
            target = row[target_column]

            analyze_request = {
                'comment': {
                    'text': target
                },
                'requestedAttributes': {
                    'TOXICITY': {},
                    'SEVERE_TOXICITY': {},
                    'IDENTITY_ATTACK': {},
                    'INSULT': {},
                    'PROFANITY': {},
                    'THREAT': {}
                }
            }
            try:
                # Send the request
                response = client.comments().analyze(body=analyze_request).execute()
        
                # Write the results to the output file
                result_item = {
                    "Row_Number": row["Row_Number"],
                    "post_"+target_column: target,
                    "scores": response["attributeScores"],
                    "languages": response["languages"],
                    "detectedLanguages": response["detectedLanguages"],
                    "error": " "
                }
    
                writer.writerow(result_item)
            except HttpError as e:

                # Check if the error code is 429 (rate limit exceeded)
                if e.resp.status == 429:
                    # Wait for 2 seconds and retry the request
                    time.sleep(2)
                    try:
                        # Send the request again
                        response = client.comments().analyze(body=analyze_request).execute()
        
                        # Write the results to the output file
                        result_item = {
                            "Row_Number": row["Row_Number"],
                            "post_"+target_column: target,
                            "scores": response["attributeScores"],
                            "languages": response["languages"],
                            "detectedLanguages": response["detectedLanguages"],
                            "error": " "
                        }
    
                        writer.writerow(result_item)
                    except HttpError as e2:
                        # Write the error to the output file
                        result_item = {
                            "Row_Number": row["Row_Number"],
                            "post_"+target_column: target,
                            "scores": " ",
                            "languages": "[und]",
                            "detectedLanguages": "[und]",
                            "error": e2
                        }
    
                        writer.writerow(result_item)
                else:
                    # Write the error to the output file
                    result_item = {
                        "Row_Number": row["Row_Number"],
                        "post_"+target_column: target,
                        "scores": " ",
                        "languages": "[und]",
                        "detectedLanguages": "[und]",
                        "error": e
                    }
    
                    writer.writerow(result_item)

        
def classify_error_rows(input_file, output_file1, output_file2):
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file1, "w", newline="", encoding="utf-8") as outfile1, open(output_file2, "w", newline="", encoding="utf-8") as outfile2:
        reader = csv.reader(infile)
        header = next(reader)
        writer1 = csv.writer(outfile1)
        writer2 = csv.writer(outfile2)
        

        # Initialize the non-error CSV writer for the output file
        writer1.writerow(["Row_Number", "post_Description", "scores", "languages", "detectedLanguages"])

        # Initialize the error CSV writer for the output file
        writer2.writerow(["Row_Number", "post_Description"])

     
        # Filter rows with 'error' as null and write them to the output files
        for row in reader:
            if row[5].strip() == "":
                writer1.writerow(row[:5])
            else:
                
                writer2.writerow([row[0], row[1]])
                

              
                

if __name__ == '__main__':
    # Get the current time
    current_time = datetime.datetime.now()
    
    # Print the current time
    print("Current time:", current_time)
    #input_file = "group_post_messages.csv"
    #output_file = "group_post_message_scores.csv"
    API_KEY = "AIzaSyC8qyWiGGX3D8FNScIY9EW-K4l_66Hvqn8"  # Replace with your actual API key
    #analyze_post_content("ppds_e_en.csv", "ppds_e_scores.csv", API_KEY, "translated_content")
    
    classify_error_rows("group_post_message_scores.csv", "gpms_no_error.csv", "gpms_error.csv")

    
    # Get the current time
    current_time = datetime.datetime.now()
    
    # Print the current time
    print("Current time:", current_time)
