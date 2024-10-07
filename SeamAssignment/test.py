import requests
from bs4 import BeautifulSoup

# Function to perform a Google search
def google_search(query):
    url = f"https://www.google.com/search?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve search results: {response.status_code}")
        return None

# Function to parse the results
def parse_results(html):
    soup = BeautifulSoup(html, "html.parser")
    search_results = []
    
    # Extract the search result titles and URLs
    for g in soup.find_all('div', class_='g')[:5]:  # limit to first 5 results
        title = g.find('h3')
        link = g.find('a')
        if title and link:
            search_results.append({
                'title': title.text,
                'link': link['href']
            })
    
    return search_results

# Main script
query = "Elon Musk latest podcast"
html = google_search(query)
if html:
    results = parse_results(html)
    for i, result in enumerate(results, start=1):
        print(f"Result {i}: {result['title']}\nURL: {result['link']}\n")

