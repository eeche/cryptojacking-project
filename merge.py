import csv
import pandas as pd

df = pd.read_csv(
    'C:\\Users\\dlckd\\Desktop\\cryptoProject\\datasets.csv')
add = pd.read_csv(
    'C:\\Users\\dlckd\\Desktop\\cryptoProject\\data.csv')

merged_dataframe = pd.concat([df, add])

# 결과 저장
merged_dataframe.to_csv('merged.csv', index=False)
