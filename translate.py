# -*- coding: utf-8 -*-
"""
Created on Sun Aug  6 22:38:52 2023

@author: wanha
"""
import re
import time
import csv
from googletrans import Translator

def translate_content(input_file, output_file):
    #translator = Translator(service_urls=['translate.googleapis.com'], credentials=api_key)
    # Create a translator object
    translator = Translator()
    
    web_link_pattern = r"(https?://)?\S+\.(com|org|net|edu)"

    # Open the input and output files
    with open(input_file, "r", newline="", encoding="utf-8") as infile, open(output_file, "w", newline="", encoding="utf-8") as outfile:
        # Create a reader and a writer object
        reader = csv.reader(infile)
        header = next(reader)
        fieldnames = ["Row_Number", "post_Description", "translated_content"]
        writer = csv.writer(outfile)

        # Write the header row to the output file
        writer.writerow(fieldnames)

        # Loop over the rows of the input file
        for row in reader:
            content = row[1]
            
            if "http:" in content or "https:" in content or "www." in content or "HTTP:" in content or "HTTPS:" in content or "WWW." in content or ".com" in content or ".net" in content or ".org" in content:
                continue
    
    
            # translate the content without web links to English
            translation = translator.translate(content, dest="en")

            # Get the translated text
            translated_content = translation.text
            

            # Write the translated content and the rest of the row to the output file
            writer.writerow([row[0], content, translated_content])
            time.sleep(1)


if __name__ == '__main__':
    # Replace "input.csv" and "output.csv" with your desired input and output file names
    input_file = "gpds_error.csv"
    output_file = "gpds_e_en.csv"

    # Call the function with the input and output file names
    translate_content(input_file, output_file)
