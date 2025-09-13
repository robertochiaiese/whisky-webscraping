"""
scraper.py

A simple web scraper that extracts whisky product information from
https://www.saporideisassi.it/80-whisky and stores the data in a Redis database.

For each whisky, the script retrieves:
    - Name
    - Price
    - Product URL
    - Description
    - Provenance (origin)
    - Type (e.g., Single Malt, Blended)
    - Brand

The data is stored in Redis using the whisky name as the key and the
attributes as hash fields.

Requirements:
    - Python 3.8+
    - requests
    - beautifulsoup4
    - lxml
    - redis (Python client)
    - A running Redis server

Usage:
    python scraper.py
"""


# Import required libraries
import requests                # For making HTTP requests to the website
import lxml                    # Parser backend (used with BeautifulSoup)
from bs4 import BeautifulSoup  # For parsing HTML pages
import logging

def redis_connect(name_redis):
  try:
  r = redis.Redis(host=name_database)
  
  except:
  logging.error("Impossible to connect to the Redis database")
  

logging.basicConfig(
    level = logging.ERROR,
    filename = 'debug.log',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

name_redis = "localhost"

redis_connect(name_redis)

# HTTP headers (to simulate a real browser request)
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36'
}

# Dictionary that will temporarily hold whisky information
whiskylist = {}
product_count = 1   # Counter (currently unused)

# Loop through the first 6 pages of whisky products
for x in range(1, 7):
    # Build the URL dynamically by inserting the page number
    base_url = 'https://www.saporideisassi.it/80-whisky?page=%s' % (x)

    # Send a GET request to fetch the page
    request = requests.get(base_url)
    
    if request.status_code == 200:   # If request was successful
        logging.("Successfully requested")
        
        # Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(request.text, "lxml")
        
        # Find all whisky product containers
        products = soup.find_all(
            'article',
            class_='product-miniature product-miniature-default product-miniature-grid product-miniature-layout-1 js-product-miniature'
        )
        
        # Find all product links
        link = soup.find_all('a', class_='thumbnail product-thumbnail', href=True)
        
        # Loop through each product in the page
        for product in products:
          
            
            # Extract whisky name
            name = product.find_all('h2', class_='h3 product-title')[0].text.strip()
            logging.info("Addedd %s" % (name))
            

            # Extract price (clean up euro symbol and format)
            price = float(
                product.find_all('span', class_='product-price')[0]
                .text.replace('€', '').strip().replace(',', '.')[0:4]
            )

            url = link[0]['href']
            
            print('Name: ' + name)
            print('Price: ' + str(price))
            print('URL: ' + url)

            # --- Access the product page for more details ---
            r_product = requests.get(link[0]['href'])
            soup = BeautifulSoup(r_product.content, 'lxml')
            
            # Extract product description
            product_description = soup.find('div', class_='rte-content product-description').text

            # Extract provenance (country/region)
            try:
                provenance = soup.find('section', class_='product-features').find_all('dd')[0].text
            except:
                provenance = 'Unknown'

            # Extract whisky type (Single Malt, Blended, etc.)
            try:
                type = soup.find('section', class_='product-features').find_all('dd')[1].text
            except:
                type = "Unknown"

            # Extract brand (from manufacturer logo alt attribute)
            try:
                brand = soup.find_all(
                    'img',
                    src=True,
                    alt=True,
                    class_=f"img-fluid manufacturer-logo"
                )[0]['alt']
            except:
                brand = "Unknown"

            # Store all whisky info in a dictionary
            whiskylist = {
                'Price': price,
                'URL': url,
                'Description': product_description,
                'Provenance': provenance,
                'Type': type,
                'Brand': brand
            }

            # Save whisky data in Redis (key = whisky name, value = attributes)
            
            r.hset(name, mapping=whiskylist)
            
    else:
        # If request fails, print status code
        logging.error('Authentication failed: ', request.status_code) 
