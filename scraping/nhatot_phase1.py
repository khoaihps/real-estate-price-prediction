import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

def clear_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.truncate(0)  # Xóa toàn bộ nội dung của tệp

def scrape_links():
    output_file = "../data/nhatot.com_links.txt"
    unscraped_links = set()

    with open(output_file, 'r', encoding='utf-8') as existing_links_file:
        existing_links = existing_links_file.read().splitlines()
        unscraped_links.update(existing_links)

    sourceUrl = 'https://www.nhatot.com'
    path = "/mua-ban-bat-dong-san-ha-noi?price=7000000000-30000000000&page="

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

    page_index = 1

    while True:
        driver = webdriver.Chrome(options=chrome_options)
        driver.get(sourceUrl + path + str(page_index))
        print(sourceUrl + path + str(page_index))
        html_content = driver.page_source
        driver.quit()
        # print(html_content)
        soup = BeautifulSoup(html_content, 'html.parser')

        if soup.find('div', class_='NotFound_content__KtIbC'):
            print('No page found.')
            break

        links = soup.find_all('a', class_='AdItem_adItem__gDDQT')

        for link in links:
            href = link.get('href')
            unscraped_links.add(sourceUrl + href)

        if page_index % 10 == 0:
            clear_file(output_file)
            with open(output_file, 'a', encoding='utf-8') as linksfile:
                for link in unscraped_links:
                    linksfile.write(link + '\n')
            print(f"Links have been written to {output_file}")

        page_index += 1

    clear_file(output_file)
    # Ghi dữ liệu
    with open(output_file, 'w', encoding='utf-8') as linksfile:
        for link in unscraped_links:
            linksfile.write(link + '\n')

    print(f"Links have been written to {output_file}")


if __name__ == "__main__":
    scrape_links()

