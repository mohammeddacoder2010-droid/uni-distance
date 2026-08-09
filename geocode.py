import csv
import time
import requests

def geocode_university(university_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{university_name}, Egypt",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "UniDistance/1.0 (educational project)"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()
    results = response.json()

    if not results:
        return None

    return {
        "latitude": results[0]["lat"],
        "longitude": results[0]["lon"],
        "location": results[0]["display_name"]
    }

with open("universities.csv", "r", encoding="utf-8") as file:
    universities = list(csv.DictReader(file))

for university in universities:
    name = university["name"]
    print(f"Geocoding: {name}")

    try:
        result = geocode_university(name)

        if result:
            university["latitude"] = result["latitude"]
            university["longitude"] = result["longitude"]
            university["location"] = result["location"]
            print(f"  → {result['latitude']}, {result['longitude']}")
        else:
            university["latitude"] = ""
            university["longitude"] = ""
            university["location"] = ""
            print("  → Location not found")

    except requests.RequestException as error:
        university["latitude"] = ""
        university["longitude"] = ""
        university["location"] = ""
        print(f"  → Request failed: {error}")

    time.sleep(1)

with open("universities_geocoded.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = [
        "name",
        "abbreviation",
        "year_established",
        "type",
        "latitude",
        "longitude",
        "location"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(universities)

print("\nDone!")
print("Created: universities_geocoded.csv")