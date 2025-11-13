import pandas as pd

# 1. Đọc file CSV gốc
file_input = "data_tour_raw.csv"  # đổi thành tên file của bạn
df = pd.read_csv(file_input)

# 2. Xem thông tin cơ bản
print("Thông tin dữ liệu ban đầu:")
print(df.info())
print(df.head())

# 3. Loại bỏ dòng trùng lặp
df.drop_duplicates(inplace=True)

# 4. Xử lý giá trị thiếu
# Ví dụ: điền giá trị mặc định hoặc bỏ dòng có dữ liệu quan trọng bị thiếu
df['ten_tour'].fillna('Chưa có tên', inplace=True)
df['dia_diem'].fillna('Chưa rõ địa điểm', inplace=True)
df['gia'].fillna(0, inplace=True)

# 5. Chuẩn hóa kiểu dữ liệu
# Chuyển cột ngày khởi hành sang datetime nếu có
if 'ngay_khoi_hanh' in df.columns:
    df['ngay_khoi_hanh'] = pd.to_datetime(df['ngay_khoi_hanh'], errors='coerce')

# Chuyển giá tour sang số
if 'gia' in df.columns:
    df['gia'] = pd.to_numeric(df['gia'], errors='coerce').fillna(0)

# 6. Loại bỏ khoảng trắng thừa ở các cột text
text_cols = df.select_dtypes(include='object').columns
for col in text_cols:
    df[col] = df[col].str.strip()

# 7. Xuất file CSV sạch
file_output = "data_tour_clean.csv"
df.to_csv(file_output, index=False, encoding='utf-8-sig')

print(f"Đã làm sạch dữ liệu và lưu thành công vào {file_output}")
