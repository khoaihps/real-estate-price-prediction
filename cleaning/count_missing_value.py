import pandas as pd

def count_missing_values(df):
    missing_values = df.isnull().sum()
    return missing_values

# Đọc dữ liệu từ file hoặc DataFrame của bạn
df = pd.read_csv('./cleaning/output/nhatot.tsv', delimiter='\t')
# Hoặc bạn có thể sử dụng DataFrame bạn đã tạo

# Hiển thị số lượng giá trị thiếu cho từng trường
missing_counts = count_missing_values(df)

# Lưu thông tin về giá trị thiếu vào file văn bản
with open('./cleaning/nhatot_insight.txt', 'w', encoding='utf-8') as file:
    file.write("Missing Value Counts:\n")
    file.write(missing_counts.to_string())

