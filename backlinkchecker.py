import requests
from bs4 import BeautifulSoup

DOMAIN = "example.com"
query = f"link:{DOMAIN}"
url = f"https://www.google.com/search?q={query}"

# Proxy setup (Replace with a working proxy)
proxies = {
    "http": "http://your_proxy:port",
    "https": "https://your_proxy:port"
}

headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(url, headers=headers, proxies=proxies)
soup = BeautifulSoup(response.text, "html.parser")

for link in soup.find_all("a"):
    href = link.get("href")
    if "http" in href:
        print(href)
