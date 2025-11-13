# backend/Model_AI/app.py

from fastapi import FastAPI
from pydantic import BaseModel
from nlp_query_parser import parse_query, filter_tours
from recommend import recommend_tours
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware

# =========================
# 1️⃣ Khởi tạo app FastAPI
# =========================
app = FastAPI(title="Tour Recommendation API")

# Cho phép CORS từ frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # hoặc domain frontend của bạn
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# 2️⃣ Load dữ liệu tour
# =========================
DATA_PATH = "backend/Model_AI/data_tour_clean.csv"
try:
    df = pd.read_csv(DATA_PATH)
except FileNotFoundError:
    print(f"⚠ Không tìm thấy file CSV: {DATA_PATH}")
    df = pd.DataFrame()

# Chuẩn hóa tên cột
df.rename(columns=lambda x: x.strip().lower(), inplace=True)
col_map = {"id": "tour_id", "name": "tour_name", "max_people": "num_people"}
df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

# =========================
# 3️⃣ Model request
# =========================
class QueryRequest(BaseModel):
    query: str
    top_n: int = 5

# =========================
# 4️⃣ Endpoint gợi ý tour
# =========================
@app.post("/query_tour")
def query_tour(req: QueryRequest):
    if df.empty:
        return {"tours": [], "similar": []}

    # Trích thông tin từ câu hỏi
    criteria = parse_query(req.query)

    # Lọc tour theo tiêu chí
    df_filtered = filter_tours(df, criteria)

    tours = df_filtered.to_dict(orient="records")

    # Gợi ý tour tương tự cho mỗi tour
    similar_list = []
    for tour in tours:
        try:
            sim = recommend_tours(tour["tour_id"], top_n=req.top_n)
        except:
            sim = []
        similar_list.append({"tour_id": tour["tour_id"], "similar": sim})

    return {"tours": tours, "similar": similar_list}

# =========================
# 5️⃣ Root test
# =========================
@app.get("/")
def root():
    return {"message": "Tour Recommendation API is running!"}
