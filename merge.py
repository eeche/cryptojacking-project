import csv
import pandas as pd

df = pd.read_csv(
    'C:\\Users\\dlckd\\Desktop\\cryptoProject\\random_forest\\new_frequency_features_corrected.csv')
add = pd.read_csv(
    'C:\\Users\\dlckd\\Desktop\\cryptoProject\\features_count.csv')

merged_dataframe = pd.concat([df, add])

# 결과 저장
merged_dataframe.to_csv('merged.csv', index=False)
