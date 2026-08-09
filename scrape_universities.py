import requests
from bs4 import BeautifulSoup
import csv

url = "https://en.wikipedia.org/wiki/List_of_universities_in_Egypt"

headers = {
    "User-Agent": "UniDistance/1.0 (educational project)"
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

tables = soup.find_all("table")

print(f"Found {len(tables)} tables")

# Tables 0, 1 and 2 contain the universities
university_tables = tables[:3]

for table in university_tables:
    rows = table.find_all("tr")

    for row in rows:
        cells = row.find_all(["th", "td"])

        print([cell.get_text(" ", strip=True) for cell in cells])