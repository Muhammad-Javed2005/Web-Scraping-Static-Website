# Importing required libraries
from bs4 import BeautifulSoup  # For parsing HTML content
import requests                # For sending HTTP requests
import pandas as pd            # For storing and exporting data

# Lists to store scraped data
book_title_list = []
book_price_list = []
book_availability_list = []

# Looping through paginated book pages
for i in range(1, 51):  # Website has 50 pages
    
    # Defining paginated URL
    url = f"http://books.toscrape.com/catalogue/page-{i}.html"
    
    # Sending HTTP request
    content = requests.get(url)
    
    # Printing HTTP status code
    print(content.status_code)
    
    # Parsing the HTML response
    soup = BeautifulSoup(content.content, "html.parser")
    
    # Finding all book containers
    books = soup.find_all('article', class_='product_pod')
    
    # Break the loop if no books found (end of pages)
    if len(books) <= 0:
        break

    # Loop through each book element and extract data
    for book in books:
        # Extract book title
        title = book.find('h3').find('a')['title']
        book_title_list.append(title)

        # Extract book price
        price = book.find('p', class_='price_color').text
        price = price.replace("£", "").strip()
        price = float(price)
        book_price_list.append(price)

        # Extract availability status
        availability = book.find('p', class_='instock availability').text.strip()
        book_availability_list.append(availability)

    # Printing current data (optional)
    print(book_title_list, book_price_list, book_availability_list)

    # Preparing DataFrame from lists
    Data = {
        'Book Title': book_title_list,
        'Price (GBP)': book_price_list,
        'Availability': book_availability_list
    }

    data = pd.DataFrame(Data)

    # Exporting data to CSV, JSON, and Excel
    data.to_csv("books_data.csv", index=False)
    data.to_json("books_data.json", orient='records', indent=4)
    data.to_excel("books_data.xlsx", index=False)


