import pandas as pd
import numpy as np

# Đọc dữ liệu từ file TSV
df = pd.read_csv('./cleaning/output/processed_data.tsv', sep='\t')

# Thay đổi các giá trị 0 thành NaN, trừ cột 'Pháp lý'
df[df.columns.difference(['Pháp lý'])] = df[df.columns.difference(['Pháp lý'])].replace(0, np.nan)
df[df.columns.difference(['Pháp lý'])] = df[df.columns.difference(['Pháp lý'])].replace(0000, np.nan)

# Đếm số lượng dữ liệu thiếu sau khi đã thay đổi
missing_data_count = df.isnull().sum()

# Tạo dataframe mới với trường "field" và "số missing value"
missing_data_df = pd.DataFrame({'field': missing_data_count.index, 'missing value': missing_data_count.values})

# Lưu kết quả vào file CSV
missing_data_df.to_csv('./cleaning/output/missing_data_count_copy.csv', encoding='utf-8', index=False)
