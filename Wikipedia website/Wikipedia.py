import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL with complete list of countries and their capitals
url = "https://en.wikipedia.org/wiki/List_of_countries_and_dependencies_by_population"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Find the first main table
table = soup.find("table", class_="wikitable")

# Lists to store the data
countries = []
capitals = []

# Loop through rows of the table
for row in table.find_all("tr")[2:]:  # Skip headers
    cols = row.find_all("td")
    if len(cols) >= 4:
        country = cols[1].text.strip()
        capital = cols[3].text.strip().split("[")[0]  # Remove references like [1]
        countries.append(country)
        capitals.append(capital)

# Save to DataFrame
df = pd.DataFrame({
    "Country": countries,
    "Capital": capitals
})

# Export to files
df.to_csv("All_Countries_Capitals.csv", index=False)
df.to_json("All_Countries_Capitals.json", indent=4)
df.to_excel("All_Countries_Capitals.xlsx", index=False)

print("✅ All countries and their capitals have been scraped and saved.")
