# -*- coding: utf-8 -*-
"""
Created on Mon Aug  7 03:48:26 2023

@author: wanha
"""


import csv
import json

def extract_and_write_scores(input_file, output_file):
    # Open the input and output CSV files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        # Create a CSV reader and writer object
        reader = csv.DictReader(infile)
        header = next(reader)
        fieldnames = ["Row_Number", "post_Description", "TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]
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
                "TOXICITY": scores_dict.get("TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "SEVERE_TOXICITY": scores_dict.get("SEVERE_TOXICITY", {}).get("summaryScore", {}).get("value", 0),
                "INSULT": scores_dict.get("INSULT", {}).get("summaryScore", {}).get("value", 0),
                "PROFANITY": scores_dict.get("PROFANITY", {}).get("summaryScore", {}).get("value", 0),
                "THREAT": scores_dict.get("THREAT", {}).get("summaryScore", {}).get("value", 0),
                "IDENTITY_ATTACK": scores_dict.get("IDENTITY_ATTACK", {}).get("summaryScore", {}).get("value", 0)
            }

            # Write the row data to the output file
            writer.writerow(row_data)
            
def sort_rows_by_score_type(input_file, output_file, ranking_column_name):
    # Open the input and output CSV files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        # Create a CSV reader and writer object
        reader = csv.DictReader(infile)
        header = next(reader)
        fieldnames = ["Row_Number", "post_Description", "TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Store the rows in a list
        rows = list(reader)

        # Sort the rows based on the ranking_column_name
        rows.sort(key=lambda row: float(row[ranking_column_name]), reverse=True)

  
        # Write the sorted rows to the output file
        writer.writerows(rows)


if __name__ == '__main__':
    input_file = "ppds_no_error.csv"   # Replace with the path to your input CSV file
    output_file = "ppds_final.csv"  # Replace with the desired output CSV file name
    #extract_and_write_scores(input_file, output_file)
