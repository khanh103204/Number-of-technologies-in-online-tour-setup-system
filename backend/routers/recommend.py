from fastapi import APIRouter
from pydantic import BaseModel
from typing import Optional
import pandas as pd
import re
from ..Model_AI.feature_vectorization import get_recommendations, get_tour_index_by_id

# ======================================================
# 🔹 Khai báo Router
# ======================================================
router = APIRouter(
    prefix="/recommend",
    tags=["Recommendation"]
)

# ======================================================
# 🔹 Load dữ liệu tour
# ======================================================
DATA_PATH = "backend/tours_train.csv"
df = pd.read_csv(DATA_PATH)
df.columns = df.columns.str.lower()

# ======================================================
# 🔹 NLP trích xuất thông tin từ câu truy vấn
# ======================================================
def extract_info_from_query(query: str):
    query = query.lower()
    info = {}

    # Địa điểm
    location_match = re.search(
        r"\b(nha trang|đà lạt|phú quốc|ninh bình|hạ long|đà nẵng|vũng tàu|huế|sapa|cần thơ|quảng ninh|kiên giang|khánh hòa)\b",
        query
    )
    if location_match:
        info["location"] = location_match.group(1)

    # Loại hình
    type_match = re.search(r"\b(biển|núi|thành phố|đảo|resort|tham quan)\b", query)
    if type_match:
        info["type"] = type_match.group(1)

    # Số người
    num_match = re.search(r"(\d+)\s*(người|khách)", query)
    if num_match:
        info["number_people"] = int(num_match.group(1))

    # Số ngày
    days_match = re.search(r"(\d+)\s*ngày", query)
    if days_match:
        info["duration_days"] = int(days_match.group(1))

    # Ngân sách
    budget_match = re.search(r"(\d+)\s*(triệu|tr)\b", query)
    if budget_match:
        info["budget"] = float(budget_match.group(1)) * 1_000_000

    return info


# ======================================================
# 🔹 Request Model
# ======================================================
class RecommendQuery(BaseModel):
    query: Optional[str] = None
    tour_id: Optional[int] = None
    top_n: int = 5
    type: Optional[str] = None
    location: Optional[str] = None
    number_people: Optional[int] = None
    budget: Optional[float] = None
    per_person: bool = True


# ======================================================
# 🔹 Hàm lọc tour theo tiêu chí
# ======================================================
def filter_tours(data: pd.DataFrame, info: dict):
    df_filtered = data.copy()

    # Lọc loại hình
    if info.get("type"):
        df_filtered = df_filtered[df_filtered["type"].str.contains(info["type"], case=False, na=False)]

    # Lọc địa điểm (chính xác theo từ khóa)
    if info.get("location"):
        pattern = rf"\b{re.escape(info['location'].lower())}\b"
        df_filtered = df_filtered[df_filtered["location"].str.lower().str.contains(pattern, regex=True, na=False)]

    # Lọc theo số người
    if info.get("number_people"):
        if "min_people" in df_filtered.columns and "max_people" in df_filtered.columns:
            df_filtered = df_filtered[
                (df_filtered["min_people"] <= info["number_people"]) &
                (df_filtered["max_people"] >= info["number_people"])
            ]

    # Lọc theo số ngày
    if info.get("duration_days") and "duration_days" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["duration_days"] == info["duration_days"]]

    # Lọc theo ngân sách
    if info.get("budget") and "price" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["price"] <= info["budget"]]

    return df_filtered


# ======================================================
# 🔹 API POST /recommend/query
# ======================================================
@router.post("/query")
def recommend_tour_post(request: RecommendQuery):
    data = df.copy()
    extracted = {}

    # Nếu có câu query tự nhiên → parse
    if request.query:
        extracted = extract_info_from_query(request.query)

    # Ưu tiên thông tin gửi từ frontend, nếu thiếu thì dùng từ query
    info = {
        "type": request.type or extracted.get("type"),
        "location": request.location or extracted.get("location"),
        "number_people": request.number_people or extracted.get("number_people"),
        "budget": request.budget or extracted.get("budget"),
        "duration_days": extracted.get("duration_days")
    }

    # Lọc theo tiêu chí
    filtered_df = filter_tours(data, info)
    if filtered_df.empty:
        filtered_df = data.copy()

    # ======================================================
    # Gợi ý AI trong phạm vi filter
    # ======================================================
    if request.tour_id:
        try:
            idx = get_tour_index_by_id(request.tour_id)
            recs = get_recommendations(idx, request.top_n)
            recs = [r for r in recs if r["id"] in filtered_df["id"].values]

            # Nếu AI không có gợi ý phù hợp → chọn ngẫu nhiên trong filter
            if not recs:
                recs = filtered_df.sample(min(request.top_n, len(filtered_df))).to_dict(orient="records")
        except Exception:
            recs = filtered_df.sample(min(request.top_n, len(filtered_df))).to_dict(orient="records")
    else:
        recs = filtered_df.sample(min(request.top_n, len(filtered_df))).to_dict(orient="records")

    return {
        "criteria": info,
        "recommendations": recs
    }
