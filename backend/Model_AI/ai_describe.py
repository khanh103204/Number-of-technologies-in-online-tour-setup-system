from fastapi import APIRouter
from pydantic import BaseModel
import random
import re

router = APIRouter()

# ==================== PHẦN CŨ GIỮ NGUYÊN ====================
class DescribeInput(BaseModel):
    name: str
    location: str
    type: str
    price: float

@router.post("/ai_describe/")
def ai_describe(data: DescribeInput):
    """Sinh mô tả cảm xúc đa dạng cho tour"""
    name = data.name
    location = data.location
    type_ = data.type.lower()
    price = int(data.price)

    templates = [
        f"Tour '{name}' tại {location} mang đến cảm giác yên bình giữa không gian {type_} tuyệt đẹp.",
        f"Hòa mình vào thiên nhiên {type_} của {location} cùng '{name}' — một hành trình thư giãn khó quên.",
        f"Nếu bạn đang tìm nơi để nghỉ ngơi và lấy lại năng lượng, '{name}' tại {location} chính là lựa chọn hoàn hảo.",
        f"Hành trình '{name}' sẽ đưa bạn đến với bầu không khí trong lành và nhẹ nhàng của vùng {type_} {location}.",
        f"Tận hưởng giây phút bình yên bên gia đình với tour '{name}' — điểm đến lý tưởng tại {location}.",
    ]
    return {"suggestion": random.choice(templates)}

# ==================== 🔥 PHẦN MỚI BỔ SUNG: XỬ LÝ CÂU HỎI NGƯỜI DÙNG ====================
class TourQuery(BaseModel):
    query: str

@router.post("/ai_describe/query/")
def parse_tour_query(data: TourQuery):
    """
    Hiểu câu hỏi người dùng như:
    'Tôi muốn tour biển Nha Trang cho 4 người, 2 ngày 1 đêm giá dưới 5 triệu'
    Trích xuất:
        - location
        - duration_days
        - people_count
        - price_limit
    """
    text = data.query.lower()

    # --- Tách số người ---
    people_match = re.search(r"(\d+)\s*(?:người|khách)", text)
    people_count = int(people_match.group(1)) if people_match else None

    # --- Tách thời lượng (ngày) ---
    duration_match = re.search(r"(\d+)\s*ngày", text)
    duration_days = int(duration_match.group(1)) if duration_match else None

    # --- Tách giá tiền (triệu / nghìn / đồng) ---
    price_match = re.search(r"(\d+(?:[.,]\d+)*)\s*(?:triệu|tr|nghìn|k|vnđ|đ|dong)", text)
    price_limit = None
    if price_match:
        value = price_match.group(1).replace(",", ".")
        if "triệu" in text or "tr" in text:
            price_limit = float(value) * 1_000_000
        elif "nghìn" in text or "k" in text:
            price_limit = float(value) * 1_000
        else:
            price_limit = float(value)

    # --- Tách địa điểm (tên riêng, viết hoa) ---
    location_match = re.search(r"(nha trang|đà lạt|phú quốc|hạ long|vũng tàu|sapa|đà nẵng|huế|hội an|quy nhơn|phan thiết)", text)
    location = location_match.group(1).title() if location_match else None

    return {
        "query": data.query,
        "parsed": {
            "location": location,
            "people_count": people_count,
            "duration_days": duration_days,
            "price_limit": price_limit
        }
    }
