import pandas as pd
import csv

def clear_file(file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.truncate(0)

def remove_duplicates():
    # Đọc dữ liệu từ file CSV vào DataFrame
    data_file_path = "../data/nhatot.com_data.tsv"
    df = pd.read_csv(data_file_path, delimiter='\t')

    # Loại bỏ các dòng trùng lặp
    df.drop_duplicates(inplace=True)

    # # Loại bỏ dòng có giá "thỏa thuận"
    # df = df[df['Mức giá'] != 'Thỏa thuận']

    # Ghi dữ liệu đã xử lý trở lại vào file
    df.to_csv(data_file_path, sep='\t', index=False)

    print("Duplicates removed and data written back to file.")


if __name__ == "__main__":
    remove_duplicates()
