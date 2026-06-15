import pandas as pd

# Load dataset
df = pd.read_csv("dataset/AB_NYC_2019.csv")

print("Original shape:", df.shape)

# =========================
# HANDLE MISSING VALUES
# =========================

# reviews_per_month:
# Nếu null => chưa có review
# => thay bằng 0
df["reviews_per_month"] = df["reviews_per_month"].fillna(0)

# last_review:
# Nếu null => chưa từng review
# => thay bằng "No Review"
df["last_review"] = df["last_review"].fillna("No Review")

# host_name:
# nếu thiếu => Unknown
df["host_name"] = df["host_name"].fillna("Unknown")

# name:
# nếu thiếu => No Name
df["name"] = df["name"].fillna("No Name")

# =========================
# REMOVE DUPLICATES
# =========================

df = df.drop_duplicates()

# =========================
# REMOVE INVALID DATA
# =========================

# price > 0
df = df[df["price"] > 0]

# minimum_nights > 0
df = df[df["minimum_nights"] > 0]

print("Cleaned shape:", df.shape)

# =========================
# EXPORT CLEAN DATA
# =========================

df.to_csv("dataset/airbnb_clean.csv", index=False)

print("Cleaned dataset exported successfully!")