# backend/Model_AI/feature_vectorization.py

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import hstack
import os

# ==========================
# 1. Load dữ liệu
# ==========================
DATA_PATH = "backend/Model_AI/data_tour_clean.csv"
MODEL_DIR = "backend/Model_AI/model_cache"
os.makedirs(MODEL_DIR, exist_ok=True)

print(f"✅ Đang load dữ liệu từ: {DATA_PATH}")
df = pd.read_csv(DATA_PATH)

# ==========================
# 2. Tiền xử lý & kết hợp text
# ==========================
def preprocess_text(text):
    import re
    if pd.isna(text):
        return ""
    text = text.lower()
    text = re.sub(r"[^a-zA-ZÀ-ỹ0-9\s]", "", text)
    return text.strip()

df["text_features"] = (
    df["name"].astype(str) + " " +
    df["description"].astype(str) + " " +
    df["location"].astype(str) + " " +
    df["type"].astype(str) + " " +
    df["difficulty"].astype(str)
).apply(preprocess_text)

# ==========================
# 3. Vector hóa TF-IDF
# ==========================
print("🔹 Đang tạo vector TF-IDF ...")
tfidf = TfidfVectorizer(stop_words="english", max_features=2000)
text_vectors = tfidf.fit_transform(df["text_features"])

# ==========================
# 4. Chuẩn hóa đặc trưng số
# ==========================
numeric_features = ["price", "min_people", "max_people", "duration_days", "rating_avg"]
scaler = MinMaxScaler()
numeric_vectors = scaler.fit_transform(df[numeric_features])

# ==========================
# 5. Ghép text + numeric
# ==========================
from scipy.sparse import csr_matrix
numeric_vectors_sparse = csr_matrix(numeric_vectors)
feature_matrix = hstack([text_vectors, numeric_vectors_sparse])

print(f"✅ Vector hóa hoàn tất. Ma trận đặc trưng: {feature_matrix.shape}")

# ==========================
# 6. Hàm tính similarity
# ==========================
def compute_similarity_matrix():
    """Tính ma trận cosine similarity cho tất cả tour"""
    return cosine_similarity(feature_matrix, feature_matrix)

# ==========================
# 7. Hàm lấy tour tương tự
# ==========================
def get_recommendations(tour_index: int, top_n: int = 5):
    if tour_index >= len(df):
        raise ValueError("tour_index nằm ngoài kích thước dữ liệu!")

    similarity_matrix = compute_similarity_matrix()
    sim_scores = list(enumerate(similarity_matrix[tour_index]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:top_n+1]
    recommended_indices = [i[0] for i in sim_scores if i[0] < len(df)]

    return df.iloc[recommended_indices][[
        "id", "name", "location", "type", "price", "duration_days", "rating_avg"
    ]].to_dict(orient="records")

# ==========================
# 8. Hàm tìm index theo ID
# ==========================
def get_tour_index_by_id(tour_id: int):
    if tour_id not in df["id"].values:
        raise ValueError(f"Tour_id {tour_id} không tồn tại trong dữ liệu.")
    return df[df["id"] == tour_id].index[0]

# ==========================
# 9. Hàm huấn luyện lại
# ==========================
def retrain_model(new_data_path: str = None):
    """
    Huấn luyện lại TF-IDF + MinMaxScaler khi dữ liệu thay đổi.
    """
    path = new_data_path or DATA_PATH
    data = pd.read_csv(path)

    data["text_features"] = (
        data["name"].astype(str) + " " +
        data["description"].astype(str) + " " +
        data["location"].astype(str) + " " +
        data["type"].astype(str) + " " +
        data["difficulty"].astype(str)
    ).apply(preprocess_text)

    new_tfidf = TfidfVectorizer(stop_words="english", max_features=2000)
    text_vecs = new_tfidf.fit_transform(data["text_features"])

    new_scaler = MinMaxScaler()
    num_vecs = new_scaler.fit_transform(data[numeric_features])
    num_vecs_sparse = csr_matrix(num_vecs)

    new_feature_matrix = hstack([text_vecs, num_vecs_sparse])

    # Lưu mô hình để backend load lại nhanh
    joblib.dump(new_tfidf, os.path.join(MODEL_DIR, "tfidf.pkl"))
    joblib.dump(new_scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
    joblib.dump(new_feature_matrix, os.path.join(MODEL_DIR, "feature_matrix.pkl"))
    print(f"✅ Đã huấn luyện & lưu mô hình mới: {new_feature_matrix.shape}")

    return new_tfidf, new_feature_matrix
