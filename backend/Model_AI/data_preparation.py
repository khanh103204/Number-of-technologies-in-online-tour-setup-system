# data_preparation.py
import pandas as pd
from sklearn.model_selection import train_test_split

# ==========================
# 1. Load dữ liệu
# ==========================
df = pd.read_csv("backend/Model_AI/data_tour_clean.csv")  # cập nhật đường dẫn tương ứng

# ==========================
# 2. Kiểm tra giá trị null
# ==========================
print("Số giá trị null theo cột:")
print(df.isnull().sum())

# Loại bỏ các dòng null trong các trường quan trọng
important_cols = ['id','name','description','location','type','difficulty','price','min_people','max_people','duration_days','rating_avg']
df = df.dropna(subset=important_cols)

# ==========================
# 3. Loại bỏ trùng lặp
# ==========================
df = df.drop_duplicates(subset='id')  # loại bỏ trùng id
df = df.reset_index(drop=True)

# ==========================
# 4. Chuẩn hóa định dạng
# ==========================
# Chuyển numeric về float
numeric_cols = ['price','min_people','max_people','duration_days','rating_avg']
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Nếu có giá trị null sau khi convert, loại bỏ
df = df.dropna(subset=numeric_cols)

# Chuyển text sang string
text_cols = ['name','description','location','type','difficulty']
for col in text_cols:
    df[col] = df[col].astype(str)

# ==========================
# 5. (Tuỳ chọn) chia dữ liệu train/test để test recommendation
# ==========================
# 80% build feature, 20% test
train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

# ==========================
# 6. Lưu dữ liệu đã chuẩn bị
# ==========================
train_df.to_csv("backend/tours_train.csv", index=False)
test_df.to_csv("backend/tours_test.csv", index=False)

print("Data preparation hoàn tất!")
print(f"Train size: {len(train_df)}, Test size: {len(test_df)}")
