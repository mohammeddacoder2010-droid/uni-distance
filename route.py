import csv
import time
import requests

def geocode_home(address):
    url = "https://nominatim.openstreetmap.org/search"

    params = {
        "q": address,
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
        "latitude": float(results[0]["lat"]),
        "longitude": float(results[0]["lon"]),
        "display_name": results[0]["display_name"]
    }


def get_route(home_lat, home_lon, university_lat, university_lon):
    url = (
        f"https://router.project-osrm.org/route/v1/driving/"
        f"{home_lon},{home_lat};{university_lon},{university_lat}"
    )

    params = {
        "overview": "false"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    data = response.json()

    if data["code"] != "Ok":
        return None

    route = data["routes"][0]

    return {
        "distance_km": round(route["distance"] / 1000, 2),
        "duration_minutes": round(route["duration"] / 60)
    }


home_address = input("Enter your home address: ")

print("\nFinding your location...")

try:
    home = geocode_home(home_address)
except requests.RequestException as error:
    print(f"Could not connect to the geocoding service: {error}")
    exit()

if not home:
    print("Could not find that location.")
    exit()

home_lat = home["latitude"]
home_lon = home["longitude"]

print(f"Location found: {home['display_name']}")
print(f"Coordinates: {home_lat}, {home_lon}\n")


with open("universities_geocoded.csv", "r", encoding="utf-8") as file:
    universities = list(csv.DictReader(file))


for university in universities:
    name = university["name"]

    print(f"Routing: {name}")

    try:
        route = get_route(
            home_lat,
            home_lon,
            float(university["latitude"]),
            float(university["longitude"])
        )

        if route:
            university["driving_distance_km"] = route["distance_km"]
            university["driving_time_minutes"] = route["duration_minutes"]

            print(
                f"  → {route['distance_km']} km, "
                f"{route['duration_minutes']} minutes"
            )
        else:
            university["driving_distance_km"] = ""
            university["driving_time_minutes"] = ""
            print("  → Route not found")

    except (requests.RequestException, ValueError) as error:
        university["driving_distance_km"] = ""
        university["driving_time_minutes"] = ""
        print(f"  → Failed: {error}")

    time.sleep(1)


with open(
    "universities_routes.csv",
    "w",
    newline="",
    encoding="utf-8"
) as file:

    fieldnames = [
        "name",
        "abbreviation",
        "year_established",
        "type",
        "latitude",
        "longitude",
        "location",
        "driving_distance_km",
        "driving_time_minutes"
    ]

    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(universities)


print("\nDone!")
print("Created: universities_routes.csv")