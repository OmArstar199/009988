import requests
from bs4 import BeautifulSoup
from collections import defaultdict
import re

# Step 1: Web Crawler
def crawl(url, max_pages=10):
    pages = []
    to_visit = [url]
    visited = set()

    while to_visit and len(pages) < max_pages:
        current_url = to_visit.pop(0)
        if current_url in visited:
            continue

        try:
            response = requests.get(current_url)
            soup = BeautifulSoup(response.text, 'html.parser')
            pages.append((current_url, soup.get_text()))

            # Extract links and add to to_visit list
            for link in soup.find_all('a', href=True):
                full_url = link['href']
                if full_url.startswith('http'):
                    to_visit.append(full_url)

            visited.add(current_url)
        except Exception as e:
            print(f"Error crawling {current_url}: {e}")

    return pages

# Step 2: Indexing
def index(pages):
    inverted_index = defaultdict(list)

    for url, text in pages:
        words = re.findall(r'\w+', text.lower())  # Tokenize and normalize
        for word in words:
            inverted_index[word].append(url)

    return inverted_index

# Step 3: Search
def search(query, inverted_index):
    query_words = re.findall(r'\w+', query.lower())
    results = set()

    for word in query_words:
        if word in inverted_index:
            results.update(inverted_index[word])

    return list(results)

# Main Program
if __name__ == "__main__":
    # Crawl a website
    start_url = "https://example.com"  # Replace with your target website
    print("Crawling...")
    pages = crawl(start_url, max_pages=5)  # Limit to 5 pages for demo
    print(f"Crawled {len(pages)} pages.")

    # Index the crawled pages
    print("Indexing...")
    inverted_index = index(pages)
    print("Indexing complete.")

    # Search
    while True:
        query = input("Enter your search query (or 'quit' to exit): ")
        if query.lower() == 'quit':
            break

        results = search(query, inverted_index)
        if results:
            print(f"Found {len(results)} results:")
            for result in results:
                print(f"- {result}")
        else:
            print("No results found.")