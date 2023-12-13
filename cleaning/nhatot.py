import pandas as pd

def convert_phaply_to_int(value):
    if any(substring in str(value) for substring in ['chưa', 'Chưa', 'đang', 'Đang', 'chờ', 'Chờ', 'làm sổ']):
        return 0
    elif any(substring in str(value) for substring in ['Hợp đồng', 'hợp đồng', 'HĐMB', 'HDMB']):
        return 1
    elif any(substring in str(value) for substring in ['sổ đỏ', 'Sổ đỏ', 'SỔ ĐỎ', 'Có sổ', 'Sổ hồng', 'sổ hồng', 'SỔ HỒNG', 'Đã có', 'đã có', 'sẵn sổ', 'Sẵn sổ', 'sổ đẹp', 'Sổ đẹp', 'đầy đủ', 'Đầy đủ', 'rõ ràng', 'Rõ ràng', 'chính chủ', 'Chính chủ', 'sẵn sàng', 'Sẵn sàng']):
        return 2
    else:
        return -1
    
def one_hot_encoder_huongnha(value):
    directions = ['Bắc', 'Đông', 'Nam', 'Tây']
    return ''.join(['1' if direction in str(value) else '0' for direction in directions])

# Set the display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Specify the file path
file_path = './data/nhatot.com_data.tsv'

# Read the TSV file
df = pd.read_csv(file_path, delimiter='\t')

# # Check for missing values
# print(df.isnull().sum())

# Convert the data to a DataFrame
df['Diện tích'] = df['Diện tích'].str.replace(' m²', '')
df['Diện tích'] = pd.to_numeric(df['Diện tích'], errors='coerce')
df['Diện tích'] = df['Diện tích'].fillna(0).astype(int)

df['Mặt tiền'] = df['Mặt tiền'].str.replace(' m', '')
df['Mặt tiền'] = pd.to_numeric(df['Mặt tiền'], errors='coerce')
df['Mặt tiền'] = df['Mặt tiền'].fillna(0).astype(int)

df['Mức giá'] = df['Mức giá'].str.replace(' tỷ', '')
df['Mức giá'] = pd.to_numeric(df['Mức giá'], errors='coerce')

df['Số phòng ngủ'] = df['Số phòng ngủ'].str.replace(' phòng', '')
df['Số phòng ngủ'] = pd.to_numeric(df['Số phòng ngủ'], errors='coerce')
df['Số phòng ngủ'] = df['Số phòng ngủ'].fillna(0).astype(int)

df['Số toilet'] = df['Số toilet'].str.replace(' phòng', '')
df['Số toilet'] = pd.to_numeric(df['Số toilet'], errors='coerce')
df['Số toilet'] = df['Số toilet'].fillna(0).astype(int)

df['Hướng nhà'] = df['Hướng nhà'].apply(one_hot_encoder_huongnha)
df['Pháp lý'] = df['Pháp lý'].apply(convert_phaply_to_int)


# Count and print the unique values of the 'Hướng nhà' column
value_counts = df['Nội thất'].value_counts()
filtered_counts = value_counts[value_counts > 10]
# print(filtered_counts)

# Print the data
# print(df[['Diện tích', 'Mặt tiền', 'Số phòng ngủ', 'Số toilet', 'Mức giá', 'lat', 'lon', 'Nội thất', 'Pháp lý']].head(10))

file_path = './cleaning/output/nhatot.tsv'
df.to_csv(file_path, sep='\t', index=False)