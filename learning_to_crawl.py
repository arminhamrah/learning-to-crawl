import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def count_ai_mentions(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text().lower()
        return text.count('ai')
    except requests.RequestException:
        print(f"Failed to fetch {url}")
        return 0

def get_all_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        return [urljoin(url, link.get('href')) for link in soup.find_all('a', href=True)]
    except requests.RequestException:
        print(f"Failed to fetch {url}")
        return []

def crawl_website(start_url, domain):
    visited = set()
    to_visit = [start_url]
    total_ai_count = 0

    while to_visit:
        current_url = to_visit.pop(0)
        if current_url in visited or domain not in current_url:
            continue

        print(f"Crawling: {current_url}")
        ai_count = count_ai_mentions(current_url)
        total_ai_count += ai_count
        print(f"AI mentions on this page: {ai_count}")

        visited.add(current_url)
        
        for link in get_all_links(current_url):
            if link not in visited and domain in link:
                to_visit.append(link)

    return total_ai_count

start_url = "https://hai.stanford.edu/"
domain = "hai.stanford.edu"
total_mentions = crawl_website(start_url, domain)

print(f"\nTotal 'AI' mentions across the entire website: {total_mentions}")