import requests
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# API Key (replace with your actual API key)
API_KEY = '0e0e4a62a507460f821197c664cdf5cc'
BASE_URL = 'https://newsapi.org/v2/top-headlines'

# Categories to fetch
categories = ['sports', 'technology', 'politics', 'business', 'health']

# Data collection
news_data = []
subcategories_data = []
source_data = []

for category in categories:
    params = {'apiKey': API_KEY, 'category': category, 'country': 'us'}
    response = requests.get(BASE_URL, params=params).json()
    articles = response.get('articles', [])
    
    # Add main category count
    article_count = len(articles)
    news_data.append({'Category': category.capitalize(), 'Number of Articles': article_count})

    # Extract subcategory and source data
    for article in articles:
        title = article.get('title', '').lower()
        source = article.get('source', {}).get('name', 'Unknown')
        source_data.append({'Source': source})

        if 'ai' in title:
            subcategories_data.append({'Subcategory': 'AI', 'Category': category})
        elif 'blockchain' in title:
            subcategories_data.append({'Subcategory': 'Blockchain', 'Category': category})
        elif 'football' in title:
            subcategories_data.append({'Subcategory': 'Football', 'Category': category})
        elif 'cricket' in title:
            subcategories_data.append({'Subcategory': 'Cricket', 'Category': category})

# Convert to DataFrames
df = pd.DataFrame(news_data)
df_subcategories = pd.DataFrame(subcategories_data)
df_sources = pd.DataFrame(source_data)

# Handle potential NaN issues
df['Number of Articles'] = df['Number of Articles'].fillna(0)
df['Number of Articles'] = pd.to_numeric(df['Number of Articles'], errors='coerce').fillna(0)

# Display the DataFrames
print(df)
print(df_subcategories)
print(df_sources)

# Visualization functions
def show_bar_chart():
    plt.figure(figsize=(8, 5))
    plt.bar(df['Category'], df['Number of Articles'], color=['#ff9999','#66b3ff','#99ff99','#ffcc99','#c2c2f0'])
    plt.title('Number of News Articles by Category')
    plt.xlabel('Category')
    plt.ylabel('Number of Articles')
    plt.show()

def show_pie_chart():
    plt.figure(figsize=(6, 6))
    plt.pie(df['Number of Articles'], labels=df['Category'], autopct='%1.1f%%', colors=['#ff9999','#66b3ff','#99ff99','#ffcc99', '#c2c2f0'])
    plt.title('News Category Distribution')
    plt.show()

def show_wordcloud():
    all_titles = ''
    for category in categories:
        params = {'apiKey': API_KEY, 'category': category, 'country': 'us'}
        response = requests.get(BASE_URL, params=params).json()
        titles = ' '.join([article['title'] for article in response.get('articles', []) if article['title']])
        all_titles += titles + ' '

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)

    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of News Headlines')
    plt.show()

def show_subcategory_chart():
    plt.figure(figsize=(8, 5))
    subcategory_counts = df_subcategories['Subcategory'].value_counts()
    plt.bar(subcategory_counts.index, subcategory_counts.values, color=['#ffa07a', '#20b2aa', '#9370db', '#f4a460'])
    plt.title('Number of News Articles by Subcategory')
    plt.xlabel('Subcategory')
    plt.ylabel('Number of Articles')
    plt.show()

def show_source_chart():
    plt.figure(figsize=(8, 5))
    source_counts = df_sources['Source'].value_counts().head(10)
    plt.bar(source_counts.index, source_counts.values, color='#4682B4')
    plt.xticks(rotation=45, ha='right')
    plt.title('Top 10 Most Frequent News Sources')
    plt.xlabel('News Source')
    plt.ylabel('Number of Articles')
    plt.tight_layout()
    plt.show()

def search_articles(keyword=None, start_date=None, end_date=None):
    params = {'apiKey': API_KEY, 'q': keyword, 'from': start_date, 'to': end_date, 'language': 'en'}
    response = requests.get(BASE_URL, params=params).json()
    articles = response.get('articles', [])
    
    if articles:
        print(f"Articles found for '{keyword}':")
        for article in articles:
            print(f"- {article.get('title')} ({article.get('publishedAt')})")
    else:
        print(f"No articles found for '{keyword}' in the specified date range.")

# Menu System
while True:
    print("\nChoose an option:")
    print("1. Bar Chart")
    print("2. Pie Chart")
    print("3. Word Cloud")
    print("4. Subcategory Chart")
    print("5. Top 10 Sources Chart")
    print("6. Search Articles")
    print("7. Exit")

    choice = input("Enter your choice: ")

    if choice == '1':
        show_bar_chart()
    elif choice == '2':
        show_pie_chart()
    elif choice == '3':
        show_wordcloud()
    elif choice == '4':
        show_subcategory_chart()
    elif choice == '5':
        show_source_chart()
    elif choice == '6':
        keyword = input("Enter keyword for search: ")
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")
        search_articles(keyword, start_date, end_date)
    elif choice == '7':
        print("Exiting...")
        break
    else:
        print("Invalid choice. Please try again.")
