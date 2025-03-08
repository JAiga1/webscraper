import requests
from bs4 import BeautifulSoup
import csv

def scrape_website(url, csv_filename):
    # Send GET request
    response = requests.get(url)
    response.raise_for_status()
    
    # Parse the webpage
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract relevant data (modify according to target site)
    data = []
    for item in soup.find_all('div', class_='some-class'):  # Change 'some-class' accordingly
        title = item.find('h2').text.strip()
        description = item.find('p').text.strip()
        data.append([title, description])
    
    # Save data to CSV
    with open(csv_filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Description'])  # Header row
        writer.writerows(data)
    
    print(f"Data saved to {csv_filename}")

# Example usage
scrape_website('https://example.com', 'scraped_data.csv')
