import pandas as pd

# Đọc dataset
df = pd.read_csv("dataset/AB_NYC_2019.csv")

# Hiển thị 5 dòng đầu
print(df.head())

print("\n==================== INFO ====================")
print(df.info())

print("\n==================== NULL VALUES ====================")
print(df.isnull().sum())

print("\n==================== STATISTICS ====================")
print(df.describe())