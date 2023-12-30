import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def count_values_above_threshold(df, column_name, threshold):
    # Lọc các hàng có giá trị trong cột 'Mức giá' lớn hơn ngưỡng
    filtered_rows = df[df[column_name] > threshold]
    
    # Đếm số lượng hàng
    count = len(filtered_rows)
    
    return count

# Đọc dữ liệu từ tệp CSV hoặc TSV
df = pd.read_csv('./cleaning/output/processed_data.tsv', sep='\t')

result = count_values_above_threshold(df, 'Diện tích', 100)
print(result)

# Vẽ biểu đồ phân bố giá nhà sử dụng Seaborn
# plt.figure(figsize=(10, 6))
# sns.histplot(df['Mức giá'], bins=30, kde=True, color='blue')
# plt.xlabel('Giá nhà')
# plt.ylabel('Số lượng')
# plt.title('Phân bố giá nhà')
# plt.grid(True)
# plt.show()


# Vẽ biểu đồ phân bố giá nhà sử dụng Seaborn
plt.figure(figsize=(10, 6))
sns.histplot(df['Mức giá'], bins=30, kde=True, color='blue')
plt.xlabel('Giá nhà')
plt.ylabel('Số lượng')
plt.title('Phân bố giá nhà')
plt.grid(True)

# Display the mean of 'Mức giá'
mean_price = df['Mức giá'].mean()

# Show the plot
plt.axvline(mean_price, color='red', linestyle='dashed', linewidth=2)
plt.legend({"Mean: " ,mean_price})
plt.show()