import pandas as pd

df1 = pd.read_csv('./cleaning/output/batdongsan.tsv', sep='\t')
df2 = pd.read_csv('./cleaning/output/nhatot.tsv', sep='\t')

result_df = pd.concat([df1, df2], ignore_index=True)

result_df.to_csv('./cleaning/output/merged_file.tsv', sep='\t', index=False)