import random
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests
from django.conf import settings

from brand_products.models import Brand, Product

amazon_base_url = "https://www.amazon.com/"

def scrape_amazon_brands():
    brands = Brand.objects.all()

    for brand in brands:
        get_brand_products(brand)


def save_products(brand, products):
    for p in products:        
        product, created = Product.objects.get_or_create(asin=p["data-asin"], brand=brand)
        product.name = p.select_one('div[data-cy="title-recipe"] span.a-text-normal').text
        product.sku="" # could not find the sku in the page.
        product.image_url=p.select_one("img")['src']
        product.save()

ua_pct = {
    "ua": {
        "0": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "1": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0",
        "2": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "3": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "4": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "5": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "6": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
        "7": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "8": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
        "9": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Safari/605.1.15",
        "10": "Mozilla/5.0 (X11; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "11": "Mozilla/5.0 (Windows NT 10.0; rv:131.0) Gecko/20100101 Firefox/131.0",
        "12": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:131.0) Gecko/20100101 Firefox/131.0",
        "13": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:106.0) Gecko/20100101 Firefox/106.0",
        "14": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
    },
    "pct": {"0": 28.8, "1": 13.28, "2": 10.98, "3": 8.55, "4": 6.25, "5": 5.56, "6": 4.53, "7": 4.27,
            "8": 3.57, "9": 2.93, "10": 2.99, "14": 1.59,
            "11": 2.55, "12": 2.44, "13": 1.7
            }}

def random_ua():
    return random.choices(list(ua_pct['ua'].values()), list(ua_pct['pct'].values()))[0]

custom_headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        'accept-language': 'en-GB,en;q=0.9',
    }

def get_brand_products(brand):
    # search by brand name at first
    url = '{0}s?k={1}'.format(amazon_base_url, brand.name)

    response = requests.get(url, headers=custom_headers)    
    print("response 1 status ", response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    # Find the brand filter and get the URL for the filtering by the specific brand name for more precise result
    filter_href = soup.select_one('#brandsRefinements>ul li[aria-label="{0}" i] a'.format(brand.name))["href"]    

    brand_filter_url = urljoin(amazon_base_url, filter_href)
    soup = parse_page(brand, brand_filter_url)

    next_page_el = soup.select_one('a.s-pagination-next')    
    while next_page_el:        
        next_page_url = next_page_el['href']
        next_page_url = urljoin(amazon_base_url, next_page_url)
        print(f'Scraping next page: {next_page_url}')
        soup = parse_page(brand, next_page_url)
        if soup:
            next_page_el = soup.select_one('a.s-pagination-next')
        else:
            print("Brand({0}) products not totally retrieved.".format(brand.name))
            break

def parse_page(brand, page_url):
    retries = settings.NUMBER_OF_RETRIES
    print("NUMBER_OF_RETRIES: ", retries)
    while True:
        print('-------------- start parse ', page_url)
        # select random user-agent to avoid being blocked
        custom_headers["user-agent"] = random_ua()
        print("user-agent ----> ", custom_headers["user-agent"])
        response = requests.get(page_url, headers=custom_headers)
        print("response status ", response.status_code)
        if response.status_code == 200:
            break
        elif retries:
            retries -= 1
            delay = random.randint(settings.MIN_RETRY_DELAY, settings.MAX_RETRY_DELAY)
            print("Wait {0} seconds to retry".format(delay))
            time.sleep(delay)
        else:
            print("Page {0} could not be retrieved".format(page_url))
            return None
    soup = BeautifulSoup(response.text, 'lxml')
    products = soup.select('.s-result-item[data-component-type="s-search-result"]')
    save_products(brand, products)
    print("--------------------")
    return soup

