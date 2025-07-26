# Importing required libraries
from bs4 import BeautifulSoup
import requests
import pandas as pd

# Lists to store scraped data
Movies_title_list = []
years_list = []
rating_list = []
duration_list = []
size_list = []

# Target URL
url = "https://www.imdb.com/chart/top/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Send HTTP request
content = requests.get(url, headers=headers)
print(content.status_code)

# Parse HTML
soup = BeautifulSoup(content.content, "html.parser")

# Find all movie containers (correct this if class doesn't match actual layout)
divs = soup.find_all('div', class_='ipc-metadata-list-summary-item__c')

# NOTE: If using modern IMDb layout, this class might not work — adjust as needed
# Print sample HTML to check structure:
# print(soup.prettify()[:1000])

# Loop through movie blocks
for div in divs:
    try:
        # Movie title
        Movies_name = div.find('h3', class_='ipc-title__text ipc-title__text--reduced').text
        Movies_title_list.append(Movies_name)

        # Release year
        year = div.find_all('span', class_="sc-dc48a950-8 gikOtO cli-title-metadata-item")[0].text
        years_list.append(year)

        # Duration
        duration = div.find_all('span', class_="sc-dc48a950-8 gikOtO cli-title-metadata-item")[1].text
        duration_list.append(duration)

        # Vote count
        size = div.find('span', class_="ipc-rating-star--voteCount").text
        size_list.append(size)

        # Rating
        rating = div.find('span', class_="ipc-rating-star--rating").text
        rating_list.append(rating)

    except AttributeError:
        # If any element is missing, skip that movie
        continue

# Store data in DataFrame
Data = {
    'Movie name': Movies_title_list,
    'Year': years_list,
    'Duration': duration_list,
    'Votes': size_list,
    'Rating': rating_list
}

df = pd.DataFrame(Data)

# Save to CSV, JSON, Excel
df.to_csv("IMDB.csv", index=False)
df.to_json("IMDB.json", indent=4, orient='records')
df.to_excel("IMDB.xlsx", index=False)

print("✅ Data scraping complete!")

print(df)
