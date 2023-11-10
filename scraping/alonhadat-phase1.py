import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

sourceUrl = 'https://alonhadat.com.vn'
path = "/nha-dat/can-ban/nha-dat/1/ha-noi.html"

# Use the Kaggle provided ChromeDriver executable
unscraped_links = set()
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
driver = webdriver.Chrome(options=chrome_options)

page_index = 0

while True:
    page_index += 1
    url = sourceUrl + path
    print(url)

    driver.get(url)
    time.sleep(1)  # Add a sleep to allow the page to load, adjust as needed

    # Get the page source after it has been dynamically updated
    html_content = driver.page_source
    soup = BeautifulSoup(html_content, 'html.parser')

    links = soup.find_all('div', class_='ct_title')

    for link in links:
        href = link.find('a').get('href')
        unscraped_links.add(sourceUrl + href)

    next_page = False

    page_div = soup.find('div', class_='page')
    active_a_tag = page_div.find('a', class_='active')
    next_a_tag = active_a_tag.find_next('a')
    if next_a_tag.find_parent('div', class_='page'):
        next_page = True
        path = next_a_tag.get('href')

    if not next_page:
        print("No page found")
        break

# Ghi dữ liệu
output_links_file = "../data/alonhadat_links.txt"

with open(output_links_file, 'w', encoding='utf-8') as linksfile:
    for link in unscraped_links:
        linksfile.write(link + '\n')

print(f"Links have been written to {output_links_file}")

# Close the WebDriver
driver.quit()
