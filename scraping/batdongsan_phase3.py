import pandas as pd
import csv

def clear_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.truncate(0)

def extract_number_from_string(s):
    # Replace commas with dots and filter out non-digit characters
    if '.' in s and ',' in s:
        cleaned_s = ''.join(filter(lambda x: x.isdigit() or x == '.', s.replace('.', '').replace(',', '.')))
        return cleaned_s
    cleaned_s = ''.join(filter(lambda x: x.isdigit() or x == '.', s.replace(',', '.')))
    return cleaned_s

def remove_duplicates():
    # Đọc dữ liệu từ file CSV vào DataFrame
    data_file_path = "../data/batdongsan.com.vn_data.tsv"
    df = pd.read_csv(data_file_path, delimiter='\t')

    # Loại bỏ các dòng trùng lặp
    df.drop_duplicates(inplace=True)

    # # Loại bỏ dòng có giá "thỏa thuận"
    # df = df[df['Mức giá'] != 'Thỏa thuận']

    # Ghi dữ liệu đã xử lý trở lại vào file
    df.to_csv(data_file_path, sep='\t', index=False)

    print("Duplicates removed and data written back to file.")

    data = {
        "Tên": [],
        "Diện tích": [],
        "Mặt tiền": [],
        "Mức giá": [],
        "Hướng nhà": [],
        "Số phòng ngủ": [],
        "Số toilet": [],
        "Nội thất": [],
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
                if key not in data:
                    data[key] = []
                data[key].append(value)
            if "Sổ đỏ/ Sổ hồng." in data["Pháp lý"][-1]:
                data["Pháp lý"][-1] = "Sổ đỏ/ Sổ hồng"
            if "triệu/m²" in data["Mức giá"][-1]:
                price = extract_number_from_string(data["Mức giá"][-1])[:-1]
                square = extract_number_from_string(data["Diện tích"][-1])[:-1]
                data["Mức giá"][-1] = str(round(float(price) * float(square) / 1000, 2)) + " tỷ"
            elif "triệu" in data["Mức giá"][-1]:
                price = extract_number_from_string(data["Mức giá"][-1])
                data["Mức giá"][-1] = str(round(float(price) / 1000, 2)) + " tỷ"

    clear_file(data_file_path)
    with open(data_file_path, 'a', newline='', encoding='utf-8') as tsvfile:
        writer = csv.writer(tsvfile, delimiter='\t')

        writer.writerow(data.keys())

        for i in range(len(data["Tên"])):
            row_data = [data[key][i] for key in data.keys()]
            writer.writerow(row_data)


if __name__ == "__main__":
    remove_duplicates()
