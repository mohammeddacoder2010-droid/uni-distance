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

university_types = [
    "State-funded",
    "National",
    "Private"
]

with open("universities.csv", "w", newline="", encoding="utf-8") as file:

    writer = csv.writer(file)
    writer.writerow([
        "name",
        "abbreviation",
        "year_established",
        "type"
    ])

    for table, university_type in zip(tables[:3], university_types):
        rows = table.find_all("tr")
        for row in rows[1:]:
            cells = row.find_all("td")
            if len(cells) >= 3:
                name = cells[0].get_text(" ", strip=True)
                abbreviation = cells[1].get_text(" ", strip=True)
                year = cells[2].get_text(" ", strip=True)
                writer.writerow([
                    name,
                    abbreviation,
                    year,
                    university_type
                ])
print("universities.csv created successfully!")