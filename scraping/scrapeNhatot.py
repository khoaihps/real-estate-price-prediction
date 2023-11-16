import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import re

def scrape_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    driver.refresh()
    try:
        # Kiểm tra xem nút "Xem thêm" có tồn tại không
        button = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Xem thêm')]")))
        driver.execute_script("arguments[0].scrollIntoView();", button)
        driver.execute_script("arguments[0].click();", button)
    except TimeoutException:
        # Trường hợp không tìm thấy nút "Xem thêm"
        print("No 'Xem thêm' button found on the page")

    # Click the button using JavaScript
    driver.execute_script("arguments[0].click();", button)

    html_content = driver.page_source
    driver.quit()

    data = {
        "Tên": "",
        "Diện tích": "",
        "Chiều ngang": "",
        "Mức giá": "",
        "Hướng cửa chính": "",
        "Số phòng ngủ": "",
        "Số phòng vệ sinh": "",
        "Tình trạng nội thất": "",
        "Giấy tờ pháp lý": "",
        "lat": "",
        "lon": "",
        "Địa chỉ": "",
        "Quận": "",
        "Thành phố": ""
    }

    soup = BeautifulSoup(html_content, 'html.parser')

    data["Tên"] = soup.find('h1', class_='AdDecriptionVeh_adTitle__vEuKD').text.strip()

    # Get giá
    price_span = soup.find('span', class_='AdDecriptionVeh_price__u_N83')
    data["Mức giá"] = price_span.text.split('-')[0].strip()

    # Get địa chỉ
    parent_span = soup.find('div', class_='media-body media-middle AdParam_address__5wp1F AdParam_addressClickable__coDWA').find('span', class_='fz13')
    if parent_span:
        for child in parent_span.find('span', class_='AdParam_addressClickableLoadMap__FLeKT'):
            child.extract()
    address = parent_span.text.strip()

    data["Địa chỉ"] = address

    # Extract information after the last comma
    thanhpho = re.search(r',\s*([^,]+)$', address)

    if thanhpho:
        thanhpho_text = thanhpho.group(1).strip()
        data["Thành phố"] = thanhpho_text

    # Extract information after "Quận", "Huyện", "Thị xã" and before the next comma
    quan = re.search(r'(Quận|Huyện|Thị xã)\s*([^,]+)', address)
    if quan:
        quan_text = quan.group(2).strip()
        data["Quận"] = quan_text

    # Get tọa độ
    script_tags = soup.find_all('script')
    text = ""
    for tag in script_tags:
        if "longitude" in str(tag) and "latitude" in str(tag):
            text = str(tag)
            break

    # Check if longitude and latitude are found
    if text:
        index_longitude = text.find('longitude":') + len('longitude":')
        index_latitude = text.find('latitude":') + len('latitude":')
        longitude = float(text[index_longitude:text.find(',', index_longitude)])
        latitude = float(text[index_latitude:text.find(',', index_latitude)])
        data["lon"] = longitude
        data["lat"] = latitude

    specs_items = soup.find_all('div', class_='media-body media-middle')

    for item in specs_items:
        full_text = item.get_text(strip=True)
        parts = full_text.split(':')
        if len(parts) == 2:
            label = parts[0]
            value = parts[1].strip()
            if label in data:
                data[label] = value


    # Dictionary to map old keys to new keys
    key_mapping = {
        "Chiều ngang": "Mặt tiền",
        "Hướng cửa chính": "Hướng nhà",
        "Số phòng vệ sinh": "Số toilet",
        "Tình trạng nội thất": "Nội thất",
        "Giấy tờ pháp lý": "Pháp lý"
    }

    updated_data = {key_mapping.get(old_key, old_key): value for old_key, value in data.items()}

    return updated_data

if __name__ == "__main__":
    # Gọi hàm scrape_data với URL nhận được
    scraped_data = scrape_data("https://www.nhatot.com/mua-ban-nha-dat-quan-hai-ba-trung-ha-noi/109857164.htm")

    # In ra kết quả hoặc làm gì đó với dữ liệu scrape được
    print(scraped_data)
