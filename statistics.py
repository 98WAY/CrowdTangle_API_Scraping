import csv
from datetime import datetime
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict

def analyze_type(filename):
    types_count = Counter()   
    with open(filename, 'r', newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row

        # Find the index of the 'Type' column
        type_index = header.index('Type')

        for row in reader:
            post_type = row[type_index]
            types_count[post_type] += 1

    post_types = list(types_count.keys())
    post_counts = list(types_count.values())
    print(post_counts)
    plt.bar(post_types, post_counts)
    plt.xlabel('Post Type')
    plt.ylabel('Count')
    plt.title('Counts of Different Post Types')
    plt.xticks(rotation=90)  # Rotate x-axis labels if needed
    plt.show()

def count_posts_by_year_groupby_account(filename):
    start_date = datetime(2020, 1, 1)
    end_date = datetime(2023, 6, 21)
    post_counts = defaultdict(lambda: defaultdict(int))
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        fb_account_index = header.index('FB_account')
        post_created_index = header.index('Post Created (US Eastern Time)')
        for row in reader:
            fb_account = row[fb_account_index]
            post_created = datetime.strptime(row[post_created_index], '%Y-%m-%d %H:%M:%S')
            if start_date <= post_created <= end_date:
                # Increment the count for the corresponding FB_account and year
                post_counts[fb_account][post_created.year] += 1

    years = [2020, 2021, 2022, 2023]
    headline = "FB_account " + " ".join(str(year) for year in years)
    print(headline)

    sorted_accounts = sorted(post_counts.keys())
    for fb_account in sorted_accounts:
        counts = post_counts[fb_account]
        year_counts = " ".join(str(counts.get(year, 0)) for year in years)
        print(fb_account, year_counts)


def dot_plot_subscriber(filename):
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        fb_account_index = header.index('FB_handle')
        past_subscriber_index = header.index('Past Subscriber')
        total_interactions_index = header.index('Total Interactions')
        post_created_index = header.index('Post Created (US Eastern Time)')
        account_data = {}
        # Iterate over the rows
        for row in reader:
            fb_account = row[fb_account_index]
            past_subscriber = int(row[past_subscriber_index])
            total_interactions = int(row[total_interactions_index])
            post_created = row[post_created_index]
            year = int(post_created[:4])
            if fb_account not in account_data:
                account_data[fb_account] = {"past_subscriber": [], "total_interactions": [], "year": []}
            account_data[fb_account]["past_subscriber"].append(past_subscriber)
            account_data[fb_account]["total_interactions"].append(total_interactions)
            account_data[fb_account]["year"].append(year)
    for fb_account, data in account_data.items():
        past_subscriber = data["past_subscriber"]
        total_interactions = data["total_interactions"]
        year = data["year"]
        plt.scatter(past_subscriber, total_interactions, c=year, cmap="viridis")
        plt.xlabel("Past Subscriber")
        plt.ylabel("Total Interactions")
        plt.title(f"Dot Plot - {fb_account}")
        cbar = plt.colorbar()
        cbar.set_label("Year")
        plt.show()

def dot_plot_month_interactions_by_type(filename):
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader) 
        post_type_index = header.index('Type')
        total_interactions_index = header.index('Total Interactions')
        post_created_time_index = header.index('Post Created (US Eastern Time)')
        data = defaultdict(list)
        for row in reader:
            post_type = row[post_type_index]
            total_interactions = int(row[total_interactions_index])
            post_created_time = row[post_created_time_index]
            post_created_datetime = datetime.strptime(post_created_time, '%Y-%m-%d %H:%M:%S')
            data[post_type].append((post_created_datetime, total_interactions))
    post_types = list(data.keys())
    colormap = plt.cm.get_cmap('tab20', len(post_types))
    for i, post_type in enumerate(post_types):
        fig, ax = plt.subplots(figsize=(12, 6))
        post_data = data[post_type]
        post_datetimes, total_interactions = zip(*post_data)
        ax.plot(post_datetimes, total_interactions, marker='o', linestyle='', markersize=4, color=colormap(i))
        ax.set_xlabel('Time')
        ax.set_ylabel('Total Interactions')
        ax.set_title(f'Distribution of Total Interactions - {post_type}')
        fig.autofmt_xdate()
        plt.show()

def generate_pie_chart_interaction(filename):
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        category_index = header.index('Page Category')
        interactions_index = header.index('Total Interactions')
        category_interactions = {}
        for row in reader:
            category = row[category_index]
            interactions = int(row[interactions_index])

            if category not in category_interactions:
                category_interactions[category] = interactions
            else:
                category_interactions[category] += interactions
        categories = list(category_interactions.keys())
        interactions = list(category_interactions.values())
        plt.figure(figsize=(12, 10))  # Adjust the figure size
        pie = plt.pie(interactions, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title('Distribution of Interactions by Page Category')
        legend = plt.legend(pie[0], categories, bbox_to_anchor=(1, 0.5), loc="center left")
        legend.set_title('Page Categories')
        plt.show()
        
def generate_post_count_pie_chart(filename):
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)  # Read the header row
        category_index = header.index('Page Category')
        category_counts = {}
        for row in reader:
            category = row[category_index]

            if category not in category_counts:
                category_counts[category] = 1
            else:
                category_counts[category] += 1

        categories = list(category_counts.keys())
        counts = list(category_counts.values())
        plt.figure(figsize=(12, 10))  # Adjust the figure size
        pie = plt.pie(counts, autopct='%1.1f%%')
        plt.axis('equal')
        plt.title('Distribution of Total Posts Count by Page Category', fontsize=16)  # Adjust the font size
        legend = plt.legend(pie[0], categories, bbox_to_anchor=(1, 0.5), loc="center left")
        legend.set_title('Page Categories')

        plt.setp(pie[2], fontsize=12)  # Adjust the font size
        plt.show()

    
# Example usage:
if __name__ == '__main__':
    #analyze_type('page_posts.csv')
    #analyze_type('group_posts.csv')
    #count_posts_by_year_groupby_account('page_posts.csv')
    #count_posts_by_year_groupby_account('group_posts.csv')
    #dot_plot_subscriber('page_posts.csv')
    #dot_plot_month_interactions_by_type('group_posts.csv')
    #generate_pie_chart_interaction('page_posts.csv')
    #generate_post_count_pie_chart('page_posts.csv')
    
