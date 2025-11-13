# backend/routers/ai_rag.py
import os
from fastapi import APIRouter, HTTPException, Query, Depends
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict
from .. import models, database
from sqlalchemy.orm import Session
import openai
import pickle

# ---------------- CONFIG -----------------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

router = APIRouter(prefix="/ai", tags=["AI Recommendation"])

# --- 1️⃣ Tải mô hình embedding ---
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
dimension = 384  # kích thước vector embedding
INDEX_FILE = "backend/ai_index.faiss"
TOURS_FILE = "backend/tours_data.pkl"

# --- 2️⃣ Khởi tạo FAISS index ---
index = faiss.IndexFlatL2(dimension)
tours_data: List[models.Tour] = []

# --- 3️⃣ Hàm load dữ liệu từ DB hoặc file ---
def load_tours_from_db(db: Session, force_reload: bool = False):
    global tours_data, index

    # Nếu đã có file và không force reload → load từ file
    if os.path.exists(INDEX_FILE) and os.path.exists(TOURS_FILE) and not force_reload:
        index = faiss.read_index(INDEX_FILE)
        with open(TOURS_FILE, "rb") as f:
            tours_data = pickle.load(f)
        print(f"✅ Đã load FAISS index và {len(tours_data)} tour từ file")
        return

    # Load từ DB
    tours = db.query(models.Tour).all()
    if not tours:
        print("⚠️ Không có tour nào trong database")
        tours_data = []
        return

    texts = [
        f"{t.title}. {t.description}. Địa điểm: {t.location}. Giá: {t.price} VND"
        for t in tours
    ]
    embeddings = model.encode(texts)
    index.reset()
    index.add(np.array(embeddings, dtype=np.float32))
    tours_data = tours

    # Lưu ra file
    faiss.write_index(index, INDEX_FILE)
    with open(TOURS_FILE, "wb") as f:
        pickle.dump(tours_data, f)
    print(f"✅ Đã tải và lưu {len(tours)} tour vào FAISS index")

# --- 4️⃣ API reload dữ liệu thủ công ---
@router.post("/reload", response_model=None)
def reload_data(db: Session = Depends(database.get_db)):
    """
    Reload lại dữ liệu tour vào FAISS index
    """
    try:
        load_tours_from_db(db, force_reload=True)
        return {"message": "Đã tải lại dữ liệu tour vào AI hệ thống", "total": len(tours_data)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Reload failed: {str(e)}")

# --- 5️⃣ API recommend tour ---
@router.get("/recommend", response_model=None)
def recommend_tour(
    query: str = Query(..., description="Câu hỏi hoặc yêu cầu du lịch của người dùng"),
    db: Session = Depends(database.get_db)
):
    """
    Recommend tour dựa trên câu hỏi của người dùng
    """
    # Nếu chưa có dữ liệu → load từ DB
    if len(tours_data) == 0:
        load_tours_from_db(db)

    if len(tours_data) == 0:
        raise HTTPException(status_code=404, detail="Không có tour nào trong hệ thống")

    # Mã hóa query
    q_embedding = model.encode([query])
    q_vector = np.array(q_embedding, dtype=np.float32)

    # Truy xuất k tour gần nhất
    k = min(5, len(tours_data))
    D, I = index.search(q_vector, k)
    recommended = [tours_data[i] for i in I[0] if i < len(tours_data)]

    # Sinh câu trả lời tự nhiên bằng GPT nếu có key
    answer = None
    if OPENAI_API_KEY and recommended:
        tour_list_str = ", ".join([f"{t.title} ({t.location}, {t.price} VND)" for t in recommended])
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Bạn là trợ lý du lịch chuyên nghiệp."},
                    {"role": "user", "content": f"Người dùng hỏi: {query}. Gợi ý các tour sau: {tour_list_str}"}
                ]
            )
            answer = response["choices"][0]["message"]["content"]
        except Exception as e:
            answer = f"GPT error: {str(e)}"

    # Trả về dữ liệu JSON
    return {
        "query": query,
        "ai_answer": answer,
        "recommendations": [
            {
                "id": t.id,
                "title": t.title,
                "location": t.location,
                "price": t.price,
                "description": t.description
            } for t in recommended
        ]
    }
