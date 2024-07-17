
## eBay Product Scraper

### Overview
This project is a Python-based web scraper designed to extract product information from eBay listings. It utilizes BeautifulSoup for parsing HTML and requests library for fetching web pages. The scraper retrieves details such as product name, price, shipping cost, photo URL, seller information, and additional item specifics from eBay product pages.

### Features
- **Data Extraction**: Extracts product details including name, price, shipping cost, and photo URL.
- **Seller Information**: Retrieves seller's name and items link.
- **Additional Details**: Scrapes item specifics and about the product details.
- **JSON Export**: Saves extracted data into a JSON file for easy retrieval and analysis.

### Installation
1. Clone the repository:
   ```
   git clone https://github.com/GreyKxtx/ebay-product-scraper.git
   ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

### Usage
1. Navigate to the project directory:
   ```
   cd ebay-product-scraper
   ```
2. Run the scraper using Python:
   ```
   python main.py
   ```
