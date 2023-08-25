# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 03:48:26 2023

@author: wanha
"""


import csv
import json
import re
import time
from googletrans import Translator
from googleapiclient import discovery
from googleapiclient.errors import HttpError
import datetime
import pandas as pd

def extract_and_write_scores(input_file, output_file):
    # Open the input and output CSV files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        # Create a CSV reader and writer object
        reader = csv.DictReader(infile)
        header = next(reader)
        fieldnames = ["Row_Number", "post_Description", "languages", "detectedLanguages", "TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop over the rows of the input file
        for row in reader:
            # Preprocess the 'scores' column to replace single quotes with double quotes
            scores_json_string = row["scores"].replace("'", "\"")

            try:
                # Parse the 'scores' column as JSON
                scores_dict = json.loads(scores_json_string)
            except json.JSONDecodeError as e:
                # If there's an issue with the JSON, print the error and continue to the next row
                print(f"JSON decoding error in row {row['Row_Number']}: {e}")
                continue

            # Extract the detailed score value for each type and add to separate columns
            row_data = {
                "Row_Number": row["Row_Number"],
                "post_Description": row["post_Description"],
                "languages": row["languages"],
                "detectedLanguages": row["detectedLanguages"],
                "TOXICITY": scores_dict.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "SEVERE_TOXICITY": scores_dict.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "INSULT": scores_dict.get("INSULT", {}).get("summaryScore", {}).get("value", 0),
                "PROFANITY": scores_dict.get("PROFANITY", {}).get("summaryScore", {}).get("value", 0),
                "THREAT": scores_dict.get("THREAT", {}).get("summaryScore", {}).get("value", 0),
                "IDENTITY_ATTACK": scores_dict.get("IDENTITY_ATTACK", {}).get("summaryScore", {}).get("value", 0)
            }

            # Write the row data to the output file
            writer.writerow(row_data)


def extract_and_write_translated_scores(input_file, output_file):
    # Open the input and output CSV files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        # Create a CSV reader and writer object
        reader = csv.DictReader(infile)
        header = next(reader)
        fieldnames = ["Row_Number", "post_translated_content", "languages", "detectedLanguages", "TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Loop over the rows of the input file
        for row in reader:
            # Preprocess the 'scores' column to replace single quotes with double quotes
            scores_json_string = row["scores"].replace("'", "\"")

            try:
                # Parse the 'scores' column as JSON
                scores_dict = json.loads(scores_json_string)
            except json.JSONDecodeError as e:
                # If there's an issue with the JSON, print the error and continue to the next row
                print(f"JSON decoding error in row {row['Row_Number']}: {e}")
                continue

            # Extract the detailed score value for each type and add to separate columns
            row_data = {
                "Row_Number": row["Row_Number"],
                "post_translated_content": row["post_translated_content"],
                "languages": row["languages"],
                "detectedLanguages": row["detectedLanguages"],
                "TOXICITY": scores_dict.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "SEVERE_TOXICITY": scores_dict.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "INSULT": scores_dict.get("INSULT", {}).get("summaryScore", {}).get("value", 0),
                "PROFANITY": scores_dict.get("PROFANITY", {}).get("summaryScore", {}).get("value", 0),
                "THREAT": scores_dict.get("THREAT", {}).get("summaryScore", {}).get("value", 0),
                "IDENTITY_ATTACK": scores_dict.get("IDENTITY_ATTACK", {}).get("summaryScore", {}).get("value", 0)
            }

            # Write the row data to the output file
            writer.writerow(row_data)


def extract_non_english_rows(input_file, output_file):
    # Open the input and output CSV files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        # Create a CSV reader and writer object
        reader = csv.DictReader(infile)
        fieldnames = ["Row_Number", "post_Description", "detectedLanguages"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Filter and write rows where detectedLanguages is not "en"
        for row in reader:
            detected_languages = row["detectedLanguages"]
            if detected_languages != "['en']":
            #if "en" not in detected_languages or ("en" in detected_languages and len(detected_languages) > 6):
                writer.writerow({
                    "Row_Number": row["Row_Number"],
                    "post_Description": row["post_Description"],
                    "detectedLanguages": detected_languages
                })
    
            

def translate_content(input_file):
    # Create a translator object
    translator = Translator()

    # Read the original file and create a list of rows
    with open(input_file, "r", newline="", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    # Modify the header to include the translated column
    header = rows[0]
    header.append("translated_content")

    # Loop over the rows of the input file (excluding the header)
    for row in rows[1:]:
        content = row[1]

        try:
            # Translate the content without web links to English
            translation = translator.translate(content, dest="en")

            # Get the translated text
            translated_content = translation.text

            # Append the translated content to the row
            row.append(translated_content)

        except Exception as e:
            print(f"Error translating row {row[0]}: {e}")
            row.append(content)
        time.sleep(0.5)

    # Write the updated rows back to the original file
    with open(input_file, "w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(rows)


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


def merge_csv_files(file1, file2, output_file):
    # Read the CSV files
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)
    
    # Rename the columns in the second file that you want to add
    df2 = df2.rename(columns={"TOXICITY": "translated_TOXICITY", "SEVERE_TOXICITY": "translated_SEVERE_TOXICITY", "INSULT": "translated_INSULT", "PROFANITY": "translated_PROFANITY", "THREAT": "translated_THREAT", "IDENTITY_ATTACK": "translated_IDENTITY_ATTACK"})
    
    # Select the columns that you want to merge from the second file
    df2 = df2[["Row_Number", "post_translated_content", "translated_TOXICITY", "translated_SEVERE_TOXICITY", "translated_INSULT", "translated_PROFANITY", "translated_THREAT", "translated_IDENTITY_ATTACK"]]
    
    # Merge the two files by the common column (Row_Number) using left join
    df_merged = pd.merge(df1, df2, on="Row_Number", how="left")
    
    # Save the merged dataframe as a new CSV file with the output filename
    df_merged.to_csv(output_file, index=False)


if __name__ == '__main__':
    input_file = "gpds_no_error.csv"   # Replace with the path to your input CSV file
    output_file = "gpds_final.csv"  # Replace with the desired output CSV file name
    #extract_and_write_scores(input_file, output_file)
    #extract_non_english_rows("ppds_final.csv", "ppds_non_en.csv")
    #translate_content("ppms_non_en.csv")
    # Get the current time
    current_time = datetime.datetime.now()
    
    # Print the current time
    print("Current time:", current_time)
    API_KEY = "AIzaSyC8qyWiGGX3D8FNScIY9EW-K4l_66Hvqn8"  # Replace with your actual API key
    #analyze_post_content("ppms_non_en.csv", "ppms_non_en_scores.csv", API_KEY, "translated_content")
    #extract_and_write_translated_scores("ppms_non_en_scores.csv", "ppms_non_en_scores_final.csv")
    merge_csv_files("ppms_final.csv", "ppms_non_en_scores_final.csv", "ppms.csv")    
    
    # Get the current time
    current_time = datetime.datetime.now()
    
    # Print the current time
    print("Current time:", current_time)
