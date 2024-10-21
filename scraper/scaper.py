from urllib.parse import urljoin
from bs4 import BeautifulSoup
import requests

from brand_products.models import Brand, Product

amazon_base_url = "https://www.amazon.com/"

def scrape_amazon_brands():
    brands = Brand.objects.all()

    for brand in brands:
        get_brand_products(brand)


def save_products(brand, products):
    for p in products:        
        product, created = Product.objects.get_or_create(name=p.select_one('div[data-cy="title-recipe"] span.a-text-normal').text, brand=brand)        
        product.asin=p["data-asin"]
        product.sku=""
        product.image_url=p.select_one("img")['src']
        product.save()

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
    # Find the brand filter and get the URL for the filtering by the specfic brand name for more precise result
    filter_href = soup.select_one('#brandsRefinements>ul li[aria-label="{0}" i] a'.format(brand.name))["href"]    

    brand_filter_url = urljoin(amazon_base_url, filter_href)
    soup = parse_page(brand, brand_filter_url)

    next_page_el = soup.select_one('a.s-pagination-next')    
    while next_page_el:        
        next_page_url = next_page_el['href']
        next_page_url = urljoin(amazon_base_url, next_page_url)
        print(f'Scraping next page: {next_page_url}')
        soup = parse_page(brand, next_page_url)
        next_page_el = soup.select_one('a.s-pagination-next')    

def parse_page(brand, page_url):    
    print('-------------- start parse ', page_url)
    response = requests.get(page_url, headers=custom_headers)    
    print("response status ", response.status_code)
    soup = BeautifulSoup(response.text, 'lxml')
    products = soup.select('.s-result-item[data-component-type="s-search-result"]')    
    print("page products count ", len(products))
    save_products(brand, products)
    print("--------------------")
    return soup

