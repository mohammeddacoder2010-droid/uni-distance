import csv

with open("universities_geocoded.csv", "r", encoding="utf-8") as file:
    universities = list(csv.DictReader(file))

cleaned_universities = [
    university
    for university in universities
    if university["latitude"] and university["longitude"]
]

with open("universities_geocoded.csv", "w", newline="", encoding="utf-8") as file:
    fieldnames = universities[0].keys()
    writer = csv.DictWriter(file, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(cleaned_universities)

print(f"Original universities: {len(universities)}")
print(f"Universities with locations: {len(cleaned_universities)}")
print(f"Removed: {len(universities) - len(cleaned_universities)}")