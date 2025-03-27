import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import argparse
import concurrent.futures
from urllib.parse import urljoin, urlparse, urldefrag


def normalize_url(url):
    """Remove fragments and normalize URLs."""
    return urldefrag(urljoin(base_url, url)).url.strip()


def crawl(url, depth):
    """Recursively crawl webpages with multithreading."""
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
    
    # Extract images
    images = [img['src'] for img in soup.find_all('img', src=True)]
    images = ", ".join(set(normalize_url(img) for img in images))
    
    # Extract additional headings
    h2_tags = [h2.text.strip() for h2 in soup.find_all('h2')]
    h2_text = ", ".join(h2_tags) if h2_tags else "No H2"

    # Save more data to CSV
    save_to_csv([url, title, description, h1_text, h2_text, images])

    # Find valid links
    links = set(
        normalize_url(a['href']) for a in soup.find_all('a', href=True)
        if is_valid_url(a['href'])
    )

    # Multithreading for crawling next links
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(lambda link: crawl(link, depth - 1), links)
    
    time.sleep(1)  # Avoid excessive requests


def is_valid_url(link):
    """Ensure the link is absolute and within the same domain."""
    parsed_link = urlparse(normalize_url(link))
    return parsed_link.scheme in {"http", "https"} and parsed_link.netloc == parsed_base.netloc


def save_to_csv(data):
    """Append data to CSV file."""
    file_exists = os.path.isfile(csv_filename)
    with open(csv_filename, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["URL", "Title", "Description", "H1", "H2", "Images"])
        writer.writerow(data)


def main():
    parser = argparse.ArgumentParser(description="Multithreaded Web Crawler")
    parser.add_argument("start_url", help="URL to start crawling from")
    parser.add_argument("--depth", type=int, default=2, help="Crawling depth")
    parser.add_argument("--output", default="crawled_data.csv", help="Output CSV filename")
    args = parser.parse_args()

    global visited_urls, session, base_url, parsed_base, csv_filename
    visited_urls = set()
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    csv_filename = args.output

    # Extract base URL for resolving relative links
    base_url = "{0.scheme}://{0.netloc}".format(urlparse(args.start_url))
    parsed_base = urlparse(base_url)

    print(f"Starting crawl at {args.start_url} with depth {args.depth}")
    print(f"Results will be saved to {csv_filename}")
    
    # Initialize CSV file
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Title", "Description", "H1", "H2", "Images"])

    crawl(args.start_url, args.depth)
    print(f"Crawling finished. Visited {len(visited_urls)} pages. Data saved in {csv_filename}")


if __name__ == "__main__":
    main()
