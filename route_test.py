import requests

#fictional home location
home_lat = 30.0500
home_lon = 31.2500

university_lat = 30.0268120
university_lon = 31.2059186

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

route = data["routes"][0]

distance_km = route["distance"] / 1000
duration_minutes = route["duration"] / 60

print(f"Distance: {distance_km:.2f} km")
print(f"Driving time: {duration_minutes:.0f} minutes")