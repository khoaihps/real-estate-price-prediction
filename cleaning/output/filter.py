import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

# Đọc dữ liệu từ file TSV
df = pd.read_csv('./cleaning/output/merged_file.tsv', sep='\t')

# Xóa các cột không cần thiết
df.drop(['Hướng nhà', 'Nội thất', 'Mặt tiền', 'Địa chỉ', 'Thành phố', 'Quận'], axis=1, inplace=True)

# Xóa các hàng có giá trị 0 hoặc NaN trong các trường 'Diện tích', 'Số phòng ngủ', 'Số toilet'
df = df[(df['Số phòng ngủ'] != 0) & (df['Số toilet'] != 0)]

# Xóa các hàng có giá trị NaN trong các trường 'lat' và 'lon'
df.dropna(subset=['lat', 'lon'], how='any', inplace=True)

# Xóa các hàng thiếu trường Mức giá
df = df[(df['Mức giá'] != 0) & (df['Mức giá'].notna()) & (df['Diện tích'] != 0)]

#Tukey's Fences
for column in ['Mức giá']:
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1

    # Lọc outliers
    df = df[~((df[column] < (Q1 - 1.5 * IQR)) |(df[column] > (Q3 + 1.5 * IQR)))]

#Scale data
scaler = StandardScaler()
df['Diện tích'] = scaler.fit_transform(df[['Diện tích']])

# Lưu dataframe sau khi xóa vào file mới (nếu cần)
df.to_csv('./cleaning/output/processed_data.tsv', sep='\t', index=False)
