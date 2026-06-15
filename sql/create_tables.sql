CREATE TABLE dim_location (
    location_id INT PRIMARY KEY,
    neighbourhood_group VARCHAR(100),
    neighbourhood VARCHAR(100),
    latitude FLOAT,
    longitude FLOAT
);

CREATE TABLE dim_room_type (
    room_type_id INT PRIMARY KEY,
    room_type VARCHAR(100)
);

CREATE TABLE dim_host (
    host_id BIGINT PRIMARY KEY,
    host_name VARCHAR(255),
    calculated_host_listings_count INT
);

CREATE TABLE fact_listing (
    listing_id BIGINT PRIMARY KEY,
    host_id BIGINT,
    location_id INT,
    room_type_id INT,
    price INT,
    minimum_nights INT,
    number_of_reviews INT,
    reviews_per_month FLOAT,
    availability_365 INT,

    FOREIGN KEY (host_id) REFERENCES dim_host(host_id),
    FOREIGN KEY (location_id) REFERENCES dim_location(location_id),
    FOREIGN KEY (room_type_id) REFERENCES dim_room_type(room_type_id)
);