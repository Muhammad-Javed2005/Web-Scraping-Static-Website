# Importing required libraries
from bs4 import BeautifulSoup  # For parsing HTML content
import requests                # For sending HTTP requests
import pandas as pd            # For data storage and manipulation

# Lists to store scraped data
product_list = []
actual_price_list = []
sale_price_list = []




# Loop through paginated URLs
for i in range(1, 1000):
    # Define the target URL with pagination
    url = f"https://saamaan.pk/collections/accessories-and-gadgets?page={i}"

    # Send an HTTP GET request to the URL
    content = requests.get(url)
 
    # Print the status code of the response (200 = OK)
    print(content.status_code)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content.content, "html.parser")

    # Find all product container divs on the page
    divs = soup.find_all('div', class_='product-item__info-inner')

    # If no product items found, break the loop (end of pages)
    if len(divs) <= 0:
        break

    # Loop through each product container
    for div in divs:
        # Extract product name
        product_name = div.find('a', class_='product-item__title text--strong link').text
        product_list.append(product_name)

        # Extract sale price
        sale_price = div.find('span', class_='price').text

        # Clean sale price (remove text and symbols)
        sale_price = str(sale_price).replace("Regular priceRs.", "") \
                                     .replace("Sale priceRs.", "") \
                                     .replace("PKR", "") \
                                     .replace(",", "") \
                                     .replace("Sale priceFrom Rs.", "") \
                                     .strip()
        sale_price = float(sale_price)
        sale_price_list.append(sale_price)

        # Extract actual/original price if available, else use sale price
        try:
            actual_price = div.find('span', class_='price price--compare').text
            actual_price = str(actual_price).replace("Regular priceRs.", "") \
                                             .replace("Sale priceRs.", "") \
                                             .replace("PKR", "") \
                                             .replace(",", "") \
                                             .replace("Sale priceFrom Rs.", "") \
                                             .strip()
            actual_price = float(actual_price)
        except AttributeError:
            actual_price = sale_price  # Fallback to sale price if original price not found

        actual_price_list.append(actual_price)

    # Print current data (optional: can be removed in final version)
    print(product_list, sale_price_list, actual_price_list)

    # Prepare DataFrame for storing the scraped data
    Data = {
        'Product Name': product_list,
        'Sale Price': sale_price_list,
        'Actual Price': actual_price_list
    }

    data = pd.DataFrame(Data)

    # Exporting data to CSV, JSON, and Excel formats
    data.to_csv("Saamaan_data.csv", index=False)
    data.to_json("Saamaan_data.json", orient='records', indent=4)
    data.to_excel("Saamaan_data.xlsx", index=False)




