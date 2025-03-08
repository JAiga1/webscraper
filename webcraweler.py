import requests
from bs4 import BeautifulSoup
import csv
import time

visited_urls = set()
csv_filename = "crawled_data.csv"

def crawl(url, depth=2):
    if depth == 0 or url in visited_urls:
        return
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return

    visited_urls.add(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title and all links
    title = soup.title.string if soup.title else "No Title"
    links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith("http")]

    # Save to CSV
    save_to_csv([url, title])

    # Crawl next links
    for link in links:
        crawl(link, depth - 1)
        time.sleep(1)  # Delay to avoid overloading the server

def save_to_csv(data):
    with open(csv_filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(data)

# Start crawling
start_url = "https://example.com"
crawl(start_url)
print("Crawling finished. Data saved in", csv_filename)
