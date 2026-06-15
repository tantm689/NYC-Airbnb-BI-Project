import pandas as pd
import csv

# Load cleaned dataset
df = pd.read_csv("dataset/airbnb_clean.csv")

# =========================
# DIM LOCATION
# =========================

dim_location = df[
    [
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude"
    ]
].drop_duplicates().reset_index(drop=True)

dim_location["location_id"] = dim_location.index + 1

dim_location = dim_location[
    [
        "location_id",
        "neighbourhood_group",
        "neighbourhood",
        "latitude",
        "longitude"
    ]
]

# =========================
# DIM ROOM TYPE
# =========================

dim_room_type = df[
    [
        "room_type"
    ]
].drop_duplicates().reset_index(drop=True)

dim_room_type["room_type_id"] = dim_room_type.index + 1

dim_room_type = dim_room_type[
    [
        "room_type_id",
        "room_type"
    ]
]

# =========================
# DIM HOST
# =========================

dim_host = df[
    [
        "host_id",
        "host_name",
        "calculated_host_listings_count"
    ]
].drop_duplicates().reset_index(drop=True)

dim_host = dim_host[
    [
        "host_id",
        "host_name",
        "calculated_host_listings_count"
    ]
]

# =========================
# EXPORT DIMENSIONS
# =========================

dim_location.to_csv(
    "dataset/dim_location.csv",
    index=False,
    encoding="utf-8"
)

dim_room_type.to_csv(
    "dataset/dim_room_type.csv",
    index=False,
    encoding="utf-8"
)

# QUOTE_ALL để tránh lỗi tên host có dấu phẩy hoặc dấu nháy kép
dim_host.to_csv(
    "dataset/dim_host.csv",
    index=False,
    encoding="utf-8",
    quoting=csv.QUOTE_ALL
)

print("Dimension tables created successfully!")