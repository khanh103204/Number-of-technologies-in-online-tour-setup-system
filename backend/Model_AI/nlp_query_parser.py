import re
import pandas as pd

def parse_query(query: str) -> dict:
    """
    Trích xuất thông tin từ câu hỏi tự nhiên của người dùng.
    Trả về dict gồm: location, type, num_people, duration_days, budget
    """
    info = {}

    # 1. Loại tour (biển, núi, city, ...)
    type_match = re.search(r'\b(biển|núi|thành phố|city|du lịch)\b', query, re.IGNORECASE)
    if type_match:
        info['type'] = type_match.group(1).lower()

    # 2. Địa điểm
    location_match = re.search(r'tour\s+([a-zA-ZÀ-ỹ\s]+)', query, re.IGNORECASE)
    if location_match:
        loc = location_match.group(1).strip().lower()
        # Loại bỏ từ "cho" nếu có
        loc = re.sub(r'\s+cho.*', '', loc)
        info['location'] = loc

    # 3. Số lượng người
    num_match = re.search(r'(\d+)\s*người', query)
    if num_match:
        info['num_people'] = int(num_match.group(1))

    # 4. Số ngày
    days_match = re.search(r'(\d+)\s*ngày', query)
    if days_match:
        info['duration_days'] = int(days_match.group(1))

    # 5. Ngân sách tối đa
    budget_match = re.search(r'giá\s*(dưới|<)\s*(\d+\.?\d*)\s*triệu', query, re.IGNORECASE)
    if budget_match:
        info['budget'] = float(budget_match.group(2)) * 1_000_000  # quy về VND

    return info

def filter_tours(df: pd.DataFrame, criteria: dict) -> pd.DataFrame:
    """
    Lọc DataFrame tour dựa trên dict criteria
    """
    df_filtered = df.copy()
    
    if 'type' in criteria:
        df_filtered = df_filtered[df_filtered['type'].str.lower() == criteria['type']]
    if 'location' in criteria:
        df_filtered = df_filtered[df_filtered['location'].str.lower().str.contains(criteria['location'])]
    if 'num_people' in criteria:
        df_filtered = df_filtered[df_filtered['num_people'] >= criteria['num_people']]
    if 'duration_days' in criteria:
        df_filtered = df_filtered[df_filtered['duration_days'] == criteria['duration_days']]
    if 'budget' in criteria:
        df_filtered = df_filtered[df_filtered['price'] <= criteria['budget']]
    
    return df_filtered
