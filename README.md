# 🏠 Airbnb NYC 2019 — Business Intelligence Project

> Phân tích dữ liệu Airbnb tại thành phố New York năm 2019 thông qua quy trình ETL, mô hình Star Schema và dashboard trực quan hóa bằng Power BI.

---

## 📌 Giới thiệu

Dự án này xây dựng một hệ thống **Business Intelligence (BI)** hoàn chỉnh cho tập dữ liệu Airbnb New York City 2019 (nguồn: [Kaggle - New York City Airbnb Open Data](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data)).

Mục tiêu là thực hiện toàn bộ pipeline phân tích dữ liệu từ thu thập → làm sạch → mô hình hóa → trực quan hóa, nhằm rút ra các insight hữu ích về thị trường cho thuê ngắn hạn tại New York.

---

## 🗂️ Cấu trúc thư mục

```
Airbnb-BI/
│
├── dataset/
│   ├── raw/
│   │   └── AB_NYC_2019.csv          # Dữ liệu gốc từ Kaggle
│   └── processed/
│       ├── airbnb_clean.csv         # Dữ liệu sau khi làm sạch
│       ├── dim_host.csv             # Bảng chiều: Host
│       ├── dim_location.csv         # Bảng chiều: Vị trí
│       ├── dim_room_type.csv        # Bảng chiều: Loại phòng
│       └── fact_listing.csv         # Bảng fact chính
│
├── etl/
│   ├── explore.py                   # Khám phá và kiểm tra dữ liệu thô
│   ├── clean_data.py                # Làm sạch dữ liệu
│   ├── create_dimensions.py         # Tạo các bảng Dimension
│   └── create_fact_table.py         # Tạo bảng Fact
│
├── sql/
│   └── create_tables.sql            # DDL tạo bảng trong cơ sở dữ liệu SQL
│
├── dashboard/
│   ├── nyc_airbnb_dashboard.pbix    # File Power BI Dashboard
│   └── nyc_airbnb_dashboard.pdf     # Xuất PDF của Dashboard
│
├── report/
│   └── report.pdf                   # Báo cáo phân tích chi tiết
│
└── README.md
```

---

## ⚙️ Quy trình ETL

Quy trình xử lý dữ liệu được thực hiện theo 4 bước tuần tự:

### Bước 1 — Khám phá dữ liệu (`explore.py`)
- Đọc file CSV gốc và in thông tin tổng quan
- Kiểm tra kiểu dữ liệu, số lượng bản ghi, giá trị null và thống kê mô tả

### Bước 2 — Làm sạch dữ liệu (`clean_data.py`)
| Vấn đề | Xử lý |
|---|---|
| `reviews_per_month` bị null | Điền giá trị `0` (chưa có đánh giá) |
| `last_review` bị null | Điền chuỗi `"No Review"` |
| `host_name` bị null | Điền `"Unknown"` |
| `name` bị null | Điền `"No Name"` |
| Bản ghi trùng lặp | Xóa bằng `drop_duplicates()` |
| `price <= 0` | Lọc bỏ (dữ liệu không hợp lệ) |
| `minimum_nights <= 0` | Lọc bỏ (dữ liệu không hợp lệ) |

Kết quả xuất ra: `dataset/processed/airbnb_clean.csv`

### Bước 3 — Tạo bảng Dimension (`create_dimensions.py`)
Từ dữ liệu đã làm sạch, tạo 3 bảng chiều:
- **`dim_location`**: `location_id`, `neighbourhood_group`, `neighbourhood`, `latitude`, `longitude`
- **`dim_room_type`**: `room_type_id`, `room_type`
- **`dim_host`**: `host_id`, `host_name`, `calculated_host_listings_count`

### Bước 4 — Tạo bảng Fact (`create_fact_table.py`)
Bảng fact được tạo bằng cách join dữ liệu sạch với các bảng dimension để lấy khóa ngoại:
- **`fact_listing`**: `listing_id`, `host_id`, `location_id`, `room_type_id`, `price`, `minimum_nights`, `number_of_reviews`, `reviews_per_month`, `availability_365`

---

## 🗄️ Mô hình dữ liệu (Star Schema)

```
                    ┌─────────────────┐
                    │   dim_host      │
                    │─────────────────│
                    │ host_id (PK)    │
                    │ host_name       │
                    │ listings_count  │
                    └────────┬────────┘
                             │
┌──────────────────┐         │         ┌──────────────────┐
│  dim_location    │         │         │  dim_room_type   │
│──────────────────│         │         │──────────────────│
│ location_id (PK) │         │         │ room_type_id (PK)│
│ neighbourhood    │         │         │ room_type        │
│ neighbourhood_gp │         │         └────────┬─────────┘
│ latitude         │         │                  │
│ longitude        │         │                  │
└────────┬─────────┘         │                  │
         │          ┌────────▼──────────────────▼─────────┐
         │          │           fact_listing               │
         └──────────│─────────────────────────────────────│
                    │ listing_id (PK)                      │
                    │ host_id (FK)                         │
                    │ location_id (FK)                     │
                    │ room_type_id (FK)                    │
                    │ price                                │
                    │ minimum_nights                       │
                    │ number_of_reviews                    │
                    │ reviews_per_month                    │
                    │ availability_365                     │
                    └──────────────────────────────────────┘
```

---

## 📊 Dashboard (Power BI)

File dashboard: [`dashboard/nyc_airbnb_dashboard.pbix`](./dashboard/nyc_airbnb_dashboard.pbix)  
Xuất PDF: [`dashboard/nyc_airbnb_dashboard.pdf`](./dashboard/nyc_airbnb_dashboard.pdf)

Dashboard trực quan hóa các chỉ số chính của thị trường Airbnb NYC 2019, bao gồm:
- Phân bố listing theo khu vực (`neighbourhood_group`)
- So sánh giá thuê trung bình theo loại phòng
- Top host có nhiều listing nhất
- Tỷ lệ các loại phòng (Entire home, Private room, Shared room)
- Mức độ sẵn sàng cho thuê (`availability_365`)
- Phân bổ địa lý trên bản đồ NYC

---

## 🛠️ Công nghệ sử dụng

| Công cụ | Mục đích |
|---|---|
| **Python 3** | Xử lý và biến đổi dữ liệu (ETL) |
| **Pandas** | Thao tác DataFrame |
| **SQL** | Định nghĩa schema cơ sở dữ liệu |
| **Power BI** | Xây dựng Dashboard trực quan |
| **CSV** | Định dạng lưu trữ dữ liệu trung gian |

---

## 🚀 Hướng dẫn chạy

### Yêu cầu
- Python 3.8+
- Thư viện: `pandas`

```bash
pip install pandas
```

### Thực thi ETL

> **Lưu ý:** Chạy các script theo đúng thứ tự từ thư mục gốc của project.

```bash
# Bước 1: Khám phá dữ liệu thô
python etl/explore.py

# Bước 2: Làm sạch dữ liệu
python etl/clean_data.py

# Bước 3: Tạo bảng Dimension
python etl/create_dimensions.py

# Bước 4: Tạo bảng Fact
python etl/create_fact_table.py
```

### Tạo bảng SQL (tuỳ chọn)

Import file [`sql/create_tables.sql`](./sql/create_tables.sql) vào hệ quản trị cơ sở dữ liệu (MySQL, PostgreSQL, ...) để tạo schema tương ứng.

---

## 📁 Dữ liệu

| File | Mô tả | Kích thước |
|---|---|---|
| `AB_NYC_2019.csv` | Dataset gốc từ Kaggle | ~7 MB |
| `airbnb_clean.csv` | Dữ liệu sau làm sạch | ~7 MB |
| `dim_host.csv` | Bảng Host | ~910 KB |
| `dim_location.csv` | Bảng Vị trí | ~2.3 MB |
| `dim_room_type.csv` | Bảng Loại phòng | < 1 KB |
| `fact_listing.csv` | Bảng Fact chính | ~2 MB |

---

## 📄 Báo cáo

Xem báo cáo phân tích chi tiết tại: [`report/report.pdf`](./report/report.pdf)

---

## 👥 Thông tin dự án

- **Môn học:** Business Intelligence 
- **Dataset:** [New York City Airbnb Open Data 2019](https://www.kaggle.com/datasets/dgomonov/new-york-city-airbnb-open-data) — Kaggle
