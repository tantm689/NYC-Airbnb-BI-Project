import pandas as pd

# =========================
# LOAD DATA
# =========================

df = pd.read_csv("dataset/airbnb_clean.csv")

dim_location = pd.read_csv("dataset/dim_location.csv")
dim_room_type = pd.read_csv("dataset/dim_room_type.csv")

# =========================
# MERGE LOCATION DIMENSION
# =========================

df = df.merge(
    dim_location,
    on=["neighbourhood_group", "neighbourhood", "latitude", "longitude"],
    how="left"
)

# =========================
# MERGE ROOM TYPE DIMENSION
# =========================

df = df.merge(
    dim_room_type,
    on="room_type",
    how="left"
)

# =========================
# CREATE FACT TABLE
# =========================

fact_listing = df[[
    "id",
    "host_id",
    "location_id",
    "room_type_id",
    "price",
    "minimum_nights",
    "number_of_reviews",
    "reviews_per_month",
    "availability_365"
]]

# Rename listing id
fact_listing = fact_listing.rename(columns={
    "id": "listing_id"
})

# =========================
# EXPORT FACT TABLE
# =========================

fact_listing.to_csv("dataset/fact_listing.csv", index=False)

print("Fact table created successfully!")