import time
import concurrent.futures
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
import scrapeBatdongsan

links_file_path = "../data/batdongsan.com.vn_links.txt"
data_file_path = "../data/batdongsan.com.vn_data.tsv"

# Đọc danh sách liên kết từ tệp
with open(links_file_path, 'r', encoding='utf-8') as links_file:
    links = links_file.read().splitlines()

# Đọc dữ liệu hiện có từ tệp
existing_data = {
    "Tên": [],
    "Diện tích": [],
    "Mức giá": [],
    "Hướng nhà": [],
    "Số phòng ngủ": [],
    "Số toilet": [],
    "Pháp lý": [],
    "lat": [],
    "lon": [],
    "Địa chỉ": [],
    "Quận": [],
    "Thành phố": []
}
with open(data_file_path, 'r', newline='', encoding='utf-8') as tsvfile:
    reader = csv.DictReader(tsvfile, delimiter='\t')
    for row in reader:
        for key, value in row.items():
            if key not in existing_data:
                existing_data[key] = []
            existing_data[key].append(value)

data = {
    "Tên": [],
    "Diện tích": [],
    "Mức giá": [],
    "Hướng nhà": [],
    "Số phòng ngủ": [],
    "Số toilet": [],
    "Pháp lý": [],
    "lat": [],
    "lon": [],
    "Địa chỉ": [],
    "Quận": [],
    "Thành phố": []
}

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")

successful_links = set()

def process_link(link):
    url = link
    scraped_data = scrapeBatdongsan.scrape_data(url)
    print(f"Scraping link {len(successful_links)+1}: {url}")
    if scraped_data:
        successful_links.add(url)
        for key, value in scraped_data.items():
            if key in data:
                data[key].append(value)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
    futures = [executor.submit(process_link, link) for link in links]
concurrent.futures.wait(futures)

# Thêm dữ liệu mới scrape được vào dữ liệu hiện có
for key in existing_data.keys():
    existing_data[key].extend(data[key])
links = [link for link in links if link not in successful_links]

# Ghi dữ liệu
output_file = "../data/batdongsan.com.vn_data.tsv"
output_links_file = "../data/batdongsan.com.vn_links.txt"

with open(output_file, 'w', newline='', encoding='utf-8') as tsvfile:
    writer = csv.writer(tsvfile, delimiter='\t')

    # Viết dòng đầu tiên chứa tên các key
    writer.writerow(existing_data.keys())

    # Viết các dòng tiếp theo với giá trị tương ứng
    for i in range(len(existing_data["Tên"])):
        row_data = [existing_data[key][i] for key in existing_data.keys()]
        writer.writerow(row_data)

print(f"Data has been written to {output_file}")

with open(output_links_file, 'w', encoding='utf-8') as linksfile:
    for link in links:
        linksfile.write(link + '\n')

print(f"Links have been written to {output_links_file}")

