import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import scrapeBatdongsan

unscraped_links = set()
sourceUrl = 'https://batdongsan.com.vn'
path = "/nha-dat-ban-ha-noi"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

page_index = 0

while True:
    page_index+=1
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(sourceUrl + path)
    print(sourceUrl + path)
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    # Tìm tất cả các phần tử <a> với class 'js__product-link-for-product-id'
    links = soup.find_all('a', class_='js__product-link-for-product-id')

    for link in links:
        href = link.get('href')
        unscraped_links.add(sourceUrl + href)

    pagination_links = soup.find_all('a', class_='re__pagination-icon')
    next_page = False

    for link in pagination_links:
        if link.find('i', class_='re__icon-chevron-right--sm'):
            next_page = True
            path = link.get('href')
            break

    if next_page == False:
        print("No page found")
        break

driver.quit()

# Ghi dữ liệu
output_links_file = "../data/batdongsan.com.vn_links.txt"

with open(output_links_file, 'w', encoding='utf-8') as linksfile:
    for link in unscraped_links:
        linksfile.write(link + '\n')

print(f"Links have been written to {output_links_file}")
