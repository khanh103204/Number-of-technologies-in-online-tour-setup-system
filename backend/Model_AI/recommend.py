# backend/routers/recommend.py
from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import re

# 🔹 Import hàm recommend_tours từ Model_AI
from ..Model_AI.recommend import recommend_tours as rec_tours

router = APIRouter(
    prefix="/recommend",
    tags=["recommend"]
)

# =========================
# Load dữ liệu tour
# =========================
DATA_PATH = "backend/Model_AI/data_tour_clean.csv"
df = pd.read_csv(DATA_PATH)

# Chuẩn hóa tên cột
df.rename(columns=lambda x: x.strip().lower(), inplace=True)
col_map = {'id': 'tour_id', 'name': 'tour_name', 'max_people': 'num_people'}
df.rename(columns={k: v for k, v in col_map.items() if k in df.columns}, inplace=True)

# Chuyển các cột dạng text về lowercase để so khớp dễ hơn
for col in ['type', 'location', 'tour_name']:
    if col in df.columns:
        df[col] = df[col].astype(str).str.lower()

# =========================
# Request model
# =========================
class RecommendQuery(BaseModel):
    query: str
    top_n: Optional[int] = 5


# =========================
# NLP: Trích xuất thông tin từ câu truy vấn
# =========================
def parse_query(query: str) -> dict:
    query = query.lower()
    info = {}

    # Loại hình tour
    type_match = re.search(r'\b(biển|núi|thành phố|city|đảo|resort|cắm trại|tham quan|team building)\b', query)
    if type_match:
        info['type'] = type_match.group(1)

    # Địa điểm (regex mở rộng & chính xác)
    location_match = re.search(
        r'\b(nha\s*trang|phú\s*quốc|đà\s*lạt|ninh\s*bình|hạ\s*long|sapa|đà\s*nẵng|huế|vũng\s*tàu|cần\s*thơ|quảng\s*ninh|hội\s*an|cát\s*bà|pleiku|buôn\s*mê\s*thuột)\b',
        query
    )
    if location_match:
        info['location'] = location_match.group(1).replace(" ", "")

    # Số người
    num_match = re.search(r'(\d+)\s*(người|khách)', query)
    if num_match:
        info['num_people'] = int(num_match.group(1))

    # Số ngày
    days_match = re.search(r'(\d+)\s*ngày', query)
    if days_match:
        info['duration_days'] = int(days_match.group(1))

    # Ngân sách
    budget_match = re.search(r'(\d+)\s*(triệu|tr)\b', query)
    if budget_match:
        info['budget'] = float(budget_match.group(1)) * 1_000_000

    return info


# =========================
# Lọc tour theo tiêu chí
# =========================
def filter_tours(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    df_filtered = df.copy()

    # Lọc theo địa điểm (ưu tiên cao nhất)
    if 'location' in criteria and 'location' in df_filtered.columns:
        loc = criteria['location'].replace(" ", "")
        df_filtered = df_filtered[df_filtered['location'].str.replace(" ", "").str.contains(loc, case=False, na=False)]

    # Lọc theo loại hình
    if 'type' in criteria and 'type' in df_filtered.columns and not df_filtered.empty:
        df_filtered = df_filtered[df_filtered['type'].str.contains(criteria['type'], case=False, na=False)]

    # Lọc theo số người
    if 'num_people' in criteria and 'num_people' in df_filtered.columns and not df_filtered.empty:
        df_filtered = df_filtered[df_filtered['num_people'] >= criteria['num_people']]

    # Lọc theo số ngày
    if 'duration_days' in criteria and 'duration_days' in df_filtered.columns and not df_filtered.empty:
        df_filtered = df_filtered[df_filtered['duration_days'] == criteria['duration_days']]

    # Lọc theo ngân sách
    if 'budget' in criteria and 'price' in df_filtered.columns and not df_filtered.empty:
        df_filtered = df_filtered[df_filtered['price'] <= criteria['budget']]

    return df_filtered


# =========================
# API: POST /recommend/query
# =========================
@router.post("/query")
def recommend_tour(request: RecommendQuery):
    # 1️⃣ Trích xuất thông tin từ câu query
    criteria = parse_query(request.query)

    # 2️⃣ Lọc tour theo tiêu chí
    df_filtered = filter_tours(df, criteria)

    # Nếu không có tour phù hợp với địa điểm => fallback nhẹ
    if df_filtered.empty and 'location' in criteria:
        # chỉ bỏ tiêu chí location, thử lọc lại phần còn lại
        relaxed_criteria = {k: v for k, v in criteria.items() if k != 'location'}
        df_filtered = filter_tours(df, relaxed_criteria)

    # Nếu vẫn không có gì, lấy toàn bộ
    if df_filtered.empty:
        df_filtered = df.copy()

    # 3️⃣ Lấy top_n kết quả (nếu có nhiều hơn)
    top_tours = df_filtered.head(request.top_n).to_dict(orient="records")

    # 4️⃣ Gợi ý tour tương tự dựa trên AI embedding
    for tour in top_tours:
        try:
            tour['similar'] = rec_tours(tour['tour_id'], top_n=request.top_n)
        except Exception:
            tour['similar'] = []

    return {"criteria": criteria, "recommendations": top_tours}
