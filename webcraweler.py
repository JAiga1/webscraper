import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import argparse
from urllib.parse import urljoin, urlparse

def crawl(url, depth=2, csv_filename="crawled_data.csv"):
    """Recursively crawl webpages starting from the given URL."""
    if depth == 0 or url in visited_urls:
        return
    
    try:
        response = session.get(url, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error accessing {url}: {e}")
        return
        
    visited_urls.add(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract more data
    title = soup.title.string.strip() if soup.title else "No Title"
    description = soup.find('meta', attrs={'name': 'description'})
    description = description['content'] if description else "No description"
    h1 = soup.find('h1')
    h1_text = h1.text.strip() if h1 else "No H1"
    
    # Save more data to CSV
    save_to_csv([url, title, description, h1_text], csv_filename)
    
    # Extract base URL for resolving relative links
    base_url = "{0.scheme}://{0.netloc}".format(urlparse(url))
    
    # Find all links and filter valid ones
    links = set(urljoin(base_url, a['href']) for a in soup.find_all('a', href=True) 
                if is_valid_url(a['href'], base_url))
    
    # Crawl next links
    for link in links:
        crawl(link, depth - 1, csv_filename)
        time.sleep(1)  # Avoid excessive requests

def is_valid_url(link, base_url):
    """Ensure the link is absolute and within the same domain."""
    parsed_link = urlparse(urljoin(base_url, link))
    parsed_base = urlparse(base_url)
    return (parsed_link.scheme in {"http", "https"} and 
            parsed_link.netloc != "" and 
            parsed_link.netloc == parsed_base.netloc)

def save_to_csv(data, csv_filename):
    """Append data to CSV file."""
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        
        # Write header if file is new
        if not file_exists:
            writer.writerow(["URL", "Title", "Description", "H1"])
        
        writer.writerow(data)

def main():
    parser = argparse.ArgumentParser(description="Web crawler")
    parser.add_argument("start_url", help="URL to start crawling from")
    parser.add_argument("--depth", type=int, default=2, help="Crawling depth")
    parser.add_argument("--output", default="crawled_data.csv", help="Output CSV filename")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between requests in seconds")
    args = parser.parse_args()
    
    global visited_urls, session
    visited_urls = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    
    # Initialize CSV file
    with open(args.output, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title", "Description", "H1"])
    
    print(f"Starting crawl at {args.start_url} with depth {args.depth}")
    print(f"Results will be saved to {args.output}")
    
    crawl(args.start_url, args.depth, args.output)
    print(f"Crawling finished. Visited {len(visited_urls)} pages. Data saved in {args.output}")

if __name__ == "__main__":
    main()
