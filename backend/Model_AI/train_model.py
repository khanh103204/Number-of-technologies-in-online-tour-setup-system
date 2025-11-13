# backend/Model_AI/train_model.py

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from scipy.sparse import hstack

# ==========================
# 1. Load dữ liệu
# ==========================
DATA_PATH = "backend/Model_AI/data_tour_clean.csv"
df = pd.read_csv(DATA_PATH)
print(f"✅ Đã load dữ liệu từ: {DATA_PATH}")

# ==========================
# 2. Kết hợp các trường text
# ==========================
df["text_features"] = (
    df["name"].astype(str) + " " +
    df["description"].astype(str) + " " +
    df["location"].astype(str) + " " +
    df["difficulty"].astype(str)
)

# ==========================
# 3. Vector hóa text
# ==========================
tfidf = TfidfVectorizer(stop_words='english', max_features=5000)
text_vectors = tfidf.fit_transform(df["text_features"])

# ==========================
# 4. Chuẩn hóa numeric
# ==========================
numeric_features = ["price", "min_people", "max_people", "duration_days", "rating_avg"]
scaler = MinMaxScaler()
numeric_vectors = scaler.fit_transform(df[numeric_features])

# ==========================
# 5. Ghép text + numeric
# ==========================
full_vectors = hstack([text_vectors, numeric_vectors])

# ==========================
# 6. Lưu mô hình và vector
# ==========================
joblib.dump(tfidf, "backend/Model_AI/tfidf_vectorizer.pkl")
joblib.dump(scaler, "backend/Model_AI/scaler.pkl")
joblib.dump(full_vectors, "backend/Model_AI/feature_matrix.pkl")

print("✅ Đã huấn luyện và lưu mô hình thành công!")
