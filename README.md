# webscraper
Web Crawler & Web Scraper
🚀 Automated tool for crawling and scraping websites, storing extracted data in CSV format.

📌 Features
✅ Web crawling to discover URLs and links from a given website.
✅ Web scraping to extract specific data (e.g., text, prices, headlines).
✅ Stores data in CSV format for easy analysis.
✅ User-agent rotation to avoid detection.
✅ Supports handling dynamic content (optional).

📦 Installation
Clone the Repository


git clone https://github.com/yourusername/webcrawler-scraper.git
cd webcrawler-scraper
Install Dependencies

pip install -r requirements.txt

🔧 Usage
Web Crawler

python crawler.py --start-url "https://example.com"
Web Scraper

python scraper.py --url "https://example.com" --output "data.csv"

🛠️ Requirements
Python 3.x
requests, BeautifulSoup, csv, Scrapy (if needed)
📝 Example Output (CSV Format)
Title	Price	URL
Sample Product	$19.99	https://example.com/product
⚠️ Legal Disclaimer
This tool is for educational purposes only. Ensure you have permission before scraping a website.
