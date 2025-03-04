import requests
from collections import defaultdict
import re

# GitHub API details
GITHUB_REPO = "your-username/your-repo"  # Replace with your repo
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/contents"
GITHUB_TOKEN = "your_personal_access_token"  # Optional, for private repos

# Step 1: Fetch data from GitHub
def fetch_github_files():
    headers = {}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    response = requests.get(GITHUB_API_URL, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code}")

    files = []
    for item in response.json():
        if item["type"] == "file" and item["name"].endswith((".txt", ".md", ".json")):
            file_url = item["download_url"]
            file_content = requests.get(file_url).text
            files.append((item["name"], file_content))

    return files

# Step 2: Indexing
def index(files):
    inverted_index = defaultdict(list)

    for filename, content in files:
        words = re.findall(r'\w+', content.lower())  # Tokenize and normalize
        for word in words:
            inverted_index[word].append(filename)

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
    # Fetch data from GitHub
    print("Fetching data from GitHub...")
    try:
        files = fetch_github_files()
        print(f"Fetched {len(files)} files.")
    except Exception as e:
        print(f"Error: {e}")
        exit()

    # Index the files
    print("Indexing...")
    inverted_index = index(files)
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