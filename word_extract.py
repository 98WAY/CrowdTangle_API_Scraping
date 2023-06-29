import csv
import nltk
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

def find_top_frequent_words(filename):
#pages group by FB_handle
    with open(filename, "r", newline='', encoding="utf-8") as file:
        reader = csv.reader(file)
        header = next(reader)
        fb_account_index = header.index('FB_handle')
        message_index = header.index('Message')
        word_counts = {}
        nltk.download('punkt')
        nltk.download('stopwords')
        stop_words = set(stopwords.words('english'))
        stop_words.update(['http', 'hi', 'thank', 'wa', 'thi', 'ha'])
        stemmer = PorterStemmer()

        for row in reader:
            fb_account = row[fb_account_index]
            message = row[message_index]
            tokens = nltk.word_tokenize(message)
            english_words = [word for word in tokens if re.match(r'^[a-zA-Z]+$', word)]
            stemmed_tokens = [stemmer.stem(token) for token in english_words]
            filtered_tokens = [token for token in stemmed_tokens if token.lower() not in stop_words]
            word_count = Counter(filtered_tokens)
            if fb_account not in word_counts:
                word_counts[fb_account] = word_count
            else:
                word_counts[fb_account] += word_count
        top_words_per_account = {}
        for fb_account, account_word_counts in word_counts.items():
            top_words = account_word_counts.most_common(11) 
            top_words_per_account[fb_account] = top_words
        for fb_account, top_words in top_words_per_account.items():
            print(f"Top frequent words for {fb_account}:")
            for word, count in top_words:
                print(f"{word}: {count}")

if __name__ == '__main__':
    filename = "extracted_pages.csv"
    find_top_frequent_words(filename)
