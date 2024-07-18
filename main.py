import requests
from bs4 import BeautifulSoup
import re
import json
from tabulate import tabulate
import logging

class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.item = {}
        self.seller = {}
        self.logger = logging.getLogger(__name__)

    def fetch_page(self):
        try:
            page = requests.get(self.url)
            page.raise_for_status()
            return page.text
        except requests.RequestException as e:
            self.logger.error(f"Failed to fetch page: {e}")
            return None

    def parse_title(self, soup):
        title_element = soup.select_one('.x-item-title__mainTitle span.ux-textspans--BOLD')
        if title_element:
            self.item['name'] = title_element.text.strip()
        else:
            self.logger.warning("Title element not found")
            self.item['name'] = 'N/A'

    def parse_price(self, soup):
        price_html_element = soup.select_one('.x-bin-price__content .x-price-primary span.ux-textspans')
        if price_html_element:
            price_text = price_html_element.text.strip()
            match = re.search(r'[\d.,]+', price_text)
            if match:
                self.item['price'] = match.group()
            else:
                self.item['price'] = 'N/A'
        else:
            self.logger.warning("Price element not found")
            self.item['price'] = 'N/A'

    def parse_photo_url(self, soup):
        image_element = soup.select_one('.ux-image-carousel-item.active img')
        if image_element:
            self.item['photoUrl'] = image_element['src']
        else:
            self.logger.warning("Image element not found")
            self.item['photoUrl'] = 'N/A'

    def parse_shipping(self, soup):
        shipping_price_element = soup.select_one('.ux-layout-section--shipping .ux-textspans--BOLD')
        if shipping_price_element:
            shipping_price_text = shipping_price_element.text.strip()
            if "Does not ship" in shipping_price_text:
                self.item['shippingPrice'] = f'({shipping_price_text})'
            else:
                match = re.search(r'[\d.,]+', shipping_price_text)
                if match:
                    self.item['shippingPrice'] = match.group()
                else:
                    self.item['shippingPrice'] = 'N/A'
        else:
            self.logger.warning("Shipping price element not found")
            self.item['shippingPrice'] = 'N/A'

    def parse_details(self, soup):
        section_title_elements = soup.select('.section-title')
        details = []
        for section_title_element in section_title_elements:
            if 'Item specifics' in section_title_element.text or 'About this product' in section_title_element.text:
                section_element = section_title_element.parent
                for section_col in section_element.select('.ux-layout-section-evo__col'):
                    col_label = section_col.select_one('.ux-labels-values__labels')
                    col_value = section_col.select_one('.ux-labels-values__values')
                    if col_label and col_value:
                        details.append([col_label.text.strip(), col_value.text.strip()])
        self.item['details'] = details if details else 'N/A'

    def parse_seller_info(self, soup):
        seller_element = soup.select_one('.x-sellercard-atf__info__about-seller a.ux-action')
        if seller_element:
            self.seller['name'] = seller_element.text.strip()
            self.seller['itemsLink'] = seller_element['href']
        else:
            self.logger.warning("Seller information not found")
            self.seller['name'] = 'N/A'
            self.seller['itemsLink'] = 'N/A'

    def scrape_and_save(self):
        page_content = self.fetch_page()
        if not page_content:
            self.logger.error("Failed to fetch page content. Exiting scrape.")
            return

        soup = BeautifulSoup(page_content, 'html.parser')

        self.item['url'] = self.url

        self.parse_title(soup)
        self.parse_price(soup)
        self.parse_photo_url(soup)
        self.parse_shipping(soup)
        self.parse_details(soup)
        self.parse_seller_info(soup)

        self.print_item_info()

        with open('productInfo.json', 'w') as file:
            json.dump({'mainInformation': self.item, 'sellerInformation': self.seller}, file, indent=4)
        print("Data has been saved to 'productInfo.json'")

    def print_item_info(self):
        print("\nMain Information:")
        main_data = [['Name', self.item.get('name', 'N/A')],
                     ['Price', self.item.get('price', 'N/A')],
                     ['Shipping Price', self.item.get('shippingPrice', 'N/A')],
                     ['Photo URL', self.item.get('photoUrl', 'N/A')],
                     ['URL', self.item.get('url', 'N/A')]]

        print(tabulate(main_data, tablefmt='grid'))

        if 'details' in self.item:
            print("\nAbout this Item:")
            details_headers = ['Attribute', 'Value']
            details_data = self.item['details']
            if details_data != 'N/A':
                print(tabulate(details_data, headers=details_headers, tablefmt='grid'))
            else:
                print("No details available for this item.")
        else:
            print("\nNo details available for this item.")

        if self.seller:
            print("\nSeller Information:")
            seller_data = [['Name', self.seller.get('name', 'N/A')],
                           ['Items Link', self.seller.get('itemsLink', 'N/A')]]
            print(tabulate(seller_data, tablefmt='grid'))
        else:
            print("\nSeller Information not available.")

if __name__ == "__main__":
    ebay_itm_url = 'https://www.ebay.com/itm/'
    item_id = '166864551603'
    full_url = ebay_itm_url + item_id
    scraper = EbayScraper(full_url)
    scraper.scrape_and_save()
