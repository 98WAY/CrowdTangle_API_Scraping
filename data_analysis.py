# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 04:14:28 2023

@author: wanha
"""
import pandas as pd
import matplotlib.pyplot as plt

# Define a function to classify the original scores into three ranges: 0-0.25, 0.25-0.5, 0.5-1.0
def classify_score(x):
    if x >= 0 and x <= 0.25:
        return "0-0.25"
    elif x > 0.25 and x <= 0.5:
        return "0.25-0.5"
    elif x > 0.5 and x <= 1.0:
        return "0.5-1.0"

def classify_score_differences(input_file, output_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # List of score columns (original and translated)
    score_columns = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    # Iterate through each score column
    for col in score_columns:
        original_col = col
        translated_col = f"translated_{col}"
        percentage_col = f"{col}_percentage"

        # Calculate the score differences and percentage changes
        df[percentage_col] = abs(((df[translated_col] - df[original_col]) / df[original_col]) * 100)

    # Keep only rows with non-empty translated_content and non-'en' language
    df = df.dropna(subset=["post_translated_content"], how="any")
    # df = df[df['languages'] != "['en']"]
    df = df[df['languages'] == "['fr']"]


    # Save the updated DataFrame to a new CSV file
    df.to_csv(output_file, index=False)



def create_score_difference_plots(input_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # List of score columns (original and translated)
    score_columns = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    # Create subplots for each score column
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    axes = axes.flatten()

    # Iterate through each score column
    for i, col in enumerate(score_columns):
        original_col = col
        translated_col = f"translated_{col}"

        # Calculate the absolute value of the score difference
        df["abs_score_difference"] = abs(df[translated_col] - df[original_col])

        # Plot the scatter plot for the score difference
        ax = axes[i]
        ax.scatter(df[original_col], df["abs_score_difference"], alpha=0.5)
        ax.set_title(f"{col} Score Difference")
        ax.set_xlabel(f"Original {col} Score")
        ax.set_ylabel("Absolute Score Difference")

    # Adjust spacing and show the plots
    plt.tight_layout()
    plt.show()



def create_percentage_difference_plots(input_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # List of score columns (original and translated)
    score_columns = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    # Create subplots for each score column
    fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(15, 10))
    axes = axes.flatten()

    # Iterate through each score column
    for i, col in enumerate(score_columns):
        original_col = col
        percentage_col = f"{col}_percentage"

        # Plot the scatter plot for the percentage difference
        ax = axes[i]
        ax.scatter(df[original_col], df[percentage_col], alpha=0.5)
        ax.set_title(f"{col} Percentage Difference")
        ax.set_xlabel(f"Original {col} Score")
        ax.set_ylabel("Percentage Difference")

    # Adjust spacing and show the plots
    plt.tight_layout()
    plt.show()
    
def count_and_classify_Percentage_difference(input_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # List of score columns (original and translated)
    score_columns = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    # Create a dictionary to store counts for each score type and percentage range
    score_counts = {col: {"0-25": 0, "25-50": 0, "50-100": 0, ">100": 0} for col in score_columns}

    # Iterate through each row and update the counts based on percentage difference
    for _, row in df.iterrows():
        for col in score_columns:
            percentage_col = f"{col}_percentage"
            if not pd.isnull(row[percentage_col]):
                percentage_diff = row[percentage_col]
                if percentage_diff >= 0 and percentage_diff <= 25:
                    score_counts[col]["0-25"] += 1
                elif percentage_diff > 25 and percentage_diff <= 50:
                    score_counts[col]["25-50"] += 1
                elif percentage_diff > 50 and percentage_diff <= 100:
                    score_counts[col]["50-100"] += 1
                elif percentage_diff > 100:
                    score_counts[col][">100"] += 1

    # Print the count results
    for col, count_dict in score_counts.items():
        print(f"Score Type: {col}")
        for range_label, count in count_dict.items():
            print(f"{range_label}: {count}")
        print("\n")
        
def count_and_classify_original_scores(input_file):
    # Load the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # List of original score columns
    original_score_columns = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    # Create a dictionary to store counts for each original score type and range
    score_counts = {col: {"0-0.25": 0, "0.25-0.5": 0, "0.5-1.0": 0} for col in original_score_columns}

    # Iterate through each row and update the counts based on original scores
    for _, row in df.iterrows():
        for col in original_score_columns:
            original_score = row[col]
            if original_score >= 0 and original_score <= 0.25:
                score_counts[col]["0-0.25"] += 1
            elif original_score > 0.25 and original_score <= 0.5:
                score_counts[col]["0.25-0.5"] += 1
            elif original_score > 0.5 and original_score <= 1.0:
                score_counts[col]["0.5-1.0"] += 1

    # Print the count results
    for col, count_dict in score_counts.items():
        print(f"Score Type: {col}")
        for range_label, count in count_dict.items():
            print(f"{range_label}: {count}")
        print("\n")
        
        
def count_interactions(post_file, score_file):
    df1 = pd.read_csv(post_file)
    df2 = pd.read_csv(score_file)
    df = pd.merge(df1, df2, on="Row_Number", how="inner")
    
    
    # Apply the function to each type of original score and create new columns for the classification
    df["TOXICITY_range"] = df["TOXICITY"].apply(classify_score)
    df["SEVERE_TOXICITY_range"] = df["SEVERE_TOXICITY"].apply(classify_score)
    df["INSULT_range"] = df["INSULT"].apply(classify_score)
    df["PROFANITY_range"] = df["PROFANITY"].apply(classify_score)
    df["THREAT_range"] = df["THREAT"].apply(classify_score)
    df["IDENTITY_ATTACK_range"] = df["IDENTITY_ATTACK"].apply(classify_score)

    # Define a list of score ranges
    score_ranges = ["0-0.25", "0.25-0.5", "0.5-1.0"]
    
    # Define a list of interaction types
    interaction_types = ["Likes", "Comments", "Shares", "Love", "Wow", "Haha", "Sad", "Angry", "Thankful", "Care"]

    # Define a list of original score types
    score_types = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    # Loop through each score type
    for score_type in score_types:
        print(f"Score Type: {score_type}")
        for interaction_type in interaction_types:
            print(f"Interaction Type: {interaction_type}")

            avg_percentages = []
            for score_range in score_ranges:
                df_filtered = df[df[score_type + "_range"] == score_range]

                # Calculate the average percentage based on Total Interactions and interaction type
                total_interactions = df_filtered["Total Interactions"].sum()
                interaction_sum = df_filtered[interaction_type].sum()
                avg_percentage = (interaction_sum / total_interactions) * 100

                avg_percentages.append(f"{score_range}: {avg_percentage:.2f}%")

            print(", ".join(avg_percentages))
        print("\n")


def scatter_interactions(post_file, score_file):            
    # Read the CSV files and merge them by the common column (Row_Number) using inner join
    df1 = pd.read_csv(post_file)
    df2 = pd.read_csv(score_file)
    df = pd.merge(df1, df2, on="Row_Number", how="inner")
    
    # Define a function to classify the original scores into three ranges: 0-0.25, 0.25-0.5, 0.5-1.0
    def classify_score(x):
        if x >= 0 and x <= 0.25:
            return "0-0.25"
        elif x > 0.25 and x <= 0.5:
            return "0.25-0.5"
        elif x > 0.5 and x <= 1.0:
            return "0.5-1.0"
    
    # Apply the function to each type of original score and create new columns for the classification
    df["TOXICITY_range"] = df["TOXICITY"].apply(classify_score)
    df["SEVERE_TOXICITY_range"] = df["SEVERE_TOXICITY"].apply(classify_score)
    df["INSULT_range"] = df["INSULT"].apply(classify_score)
    df["PROFANITY_range"] = df["PROFANITY"].apply(classify_score)
    df["THREAT_range"] = df["THREAT"].apply(classify_score)
    df["IDENTITY_ATTACK_range"] = df["IDENTITY_ATTACK"].apply(classify_score)
    
    # Define a list of interaction types
    interaction_types = ["Likes", "Comments", "Shares", "Love", "Wow", "Haha", "Sad", "Angry", "Thankful", "Care"]
    
    # Define a list of original score types
    score_types = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]
    
    # Define a list of score ranges
    score_ranges = ["0-0.25", "0.25-0.5", "0.5-1.0"]
    
    # Determine the number of columns for the subplots grid
    num_columns = 3  # You can adjust this value
    
    # Calculate the number of rows needed based on the number of interaction types
    num_rows = (len(interaction_types) + num_columns - 1) // num_columns
    
    # Loop through each score type
    for i, score_type in enumerate(score_types):
        # Create subplots for each interaction type
        fig, axes = plt.subplots(num_rows, num_columns, figsize=(18, 6 * num_rows))
        
        # Loop through each interaction type
        for j, interaction_type in enumerate(interaction_types):
            row = j // num_columns
            col = j % num_columns
            ax = axes[row, col]
            
            # Loop through each score range and plot the scatter chart
            for score_range in score_ranges:
                # Filter the dataframe by the score range
                df_filtered = df[df[score_type + "_range"] == score_range]
                
                # Plot the scatter chart with appropriate labels and title
                ax.scatter(df_filtered[score_type], df_filtered[interaction_type], label=score_range)
                
            ax.set_xlabel(score_type + " score")
            ax.set_ylabel(interaction_type + " count")
            ax.set_title("Interaction type by " + score_type + " score")
            ax.legend()
        
        # Adjust spacing and save the plot as an image file with a unique name
        plt.tight_layout()
        plt.savefig(score_type + "_interactions.png")
        plt.show()

def extract_and_output_by_score_type(post_file, score_file):
    # Read the CSV files
    df_posts = pd.read_csv(post_file)
    df_scores = pd.read_csv(score_file)

    # Merge the dataframes based on the common Row_Number
    df_merged = pd.merge(df_posts, df_scores, on="Row_Number", how="inner")

    # Define a list of original score types
    score_types = ["TOXICITY", "SEVERE_TOXICITY", "INSULT", "PROFANITY", "THREAT", "IDENTITY_ATTACK"]

    for score_type in score_types:
        # Filter rows where the score is greater than 0.5 for the current score type
        df_filtered = df_merged[df_merged[score_type] > 0.5]

        # Define the output filename
        output_filename = f"{score_type}_high_scores.csv"

        # Save the filtered dataframe to the output file
        df_filtered.to_csv(output_filename, index=False)
        print(f"Saved {len(df_filtered)} rows to {output_filename}")
    

if __name__ == '__main__':
    input_file = "ppds.csv"  # Replace with your input CSV file
    output_file = "ppds_translated_fr.csv"  # Replace with the desired output filename
    #classify_score_differences(input_file, output_file)
    #create_score_difference_plots("ppms_translated_fr.csv")
    #create_percentage_difference_plots("ppms_translated_fr.csv")
    #count_and_classify_Percentage_difference("ppms_translated_fr.csv")
    #count_and_classify_original_scores("ppds.csv")
    #scatter_interactions("final_page_posts.csv", "ppms.csv")
    #count_interactions("final_page_posts.csv", "ppms.csv")
    extract_and_output_by_score_type("final_page_posts.csv", "ppms.csv")
