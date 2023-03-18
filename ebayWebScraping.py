import requests
from bs4 import BeautifulSoup

# Template eBay URL, adding parameters based on search
ebay_url = "https://www.ebay.com/sch/i.html"

# Prompt user for input
title = input("Enter a vinyl title: ")
threshold_price = float(input("Enter a maximum price ($): "))

# eBay query parameters, used to build URL
params = {
    "_from": "R40",
    "_nkw": title,
    "_sacat": 0,
    "_ipg": 100,
    "LH_TitleDesc": 0  # exclude suggested results
}

# Function to check if item price is below threshold
def check_price(item_price, threshold_price):
    if isinstance(item_price, float):
        item_price = str(item_price)
    item_price = item_price.replace('$', '').replace(',', '')  # remove dollar sign and commas
    return float(item_price) < threshold_price


# Raw HTML response
ebay_page = requests.get(ebay_url, params=params)

# BS4 parsing in HTML
ebay_soup = BeautifulSoup(ebay_page.content, 'html.parser')

# Find all item entries (items in eBay are stored under this tag)
ebay_items = ebay_soup.find_all('div', class_='s-item__info')

# Store matching titles and prices in a list of dictionaries
matching_items = []

for item in ebay_items:

    # Find the item title
    item_title = item.find('div', {'class': 's-item__title'}).text.strip()

    # Ignore case
    if title.lower() in item_title.lower():

        # Find corresponding price
        item_price_str = item.find('span', {'class': 's-item__price'}).text.strip()

        # Handle price ranges, remove the dollar sign
        item_price_list = item_price_str[1:].split(" to ")  # split price range

        # If any items are within the price range
        if any(check_price(price, threshold_price) for price in item_price_list):
            
            # Append the item to the dictionary 
            matching_items.append({'title': item_title, 'price': item_price_str})

# Print the matching titles and prices
for item in matching_items:
    print(item['title'], item['price'])
