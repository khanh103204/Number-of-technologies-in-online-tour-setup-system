# backend/routers/tours.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
from decimal import Decimal

from .. import models, schemas
from ..database import get_db
from ..routers.auth import require_admin

router = APIRouter(prefix="/tours", tags=["tours"])

# ======================================================
# 🧱 ADMIN: Tạo tour mới
# ======================================================
@router.post("/", response_model=schemas.TourResponse, status_code=status.HTTP_201_CREATED)
def create_tour(
    tour: schemas.TourCreate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """
    Chỉ ADMIN được phép tạo tour mới.
    """
    # Kiểm tra tour trùng tên
    existing = db.query(models.Tour).filter(models.Tour.name == tour.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Tour với tên này đã tồn tại")

    # ✅ Kiểm tra location hợp lệ
    if not tour.location or tour.location.strip() == "":
        raise HTTPException(status_code=400, detail="Vui lòng nhập địa điểm (location) cho tour")

    # Tạo tour mới
    db_tour = models.Tour(**tour.dict())
    db.add(db_tour)
    db.commit()
    db.refresh(db_tour)
    return db_tour


# ======================================================
# 🧩 ADMIN: Cập nhật thông tin tour
# ======================================================
@router.put("/{tour_id}", response_model=schemas.TourResponse)
def update_tour(
    tour_id: int,
    tour: schemas.TourUpdate,
    db: Session = Depends(get_db),
    admin=Depends(require_admin),
):
    """
    Chỉ ADMIN được phép cập nhật tour.
    """
    db_tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    if not db_tour:
        raise HTTPException(status_code=404, detail="Tour không tồn tại")

    update_data = tour.dict(exclude_unset=True)

    # ✅ Nếu có trường location thì cập nhật
    if "location" in update_data and update_data["location"]:
        db_tour.location = update_data["location"]

    for field, value in update_data.items():
        setattr(db_tour, field, value)

    db.commit()
    db.refresh(db_tour)
    return db_tour


# ======================================================
# 🔍 Lấy thông tin 1 tour cụ thể
# ======================================================
@router.get("/{tour_id}", response_model=schemas.TourResponse)
def get_tour(tour_id: int, db: Session = Depends(get_db)):
    """
    Lấy thông tin chi tiết 1 tour.
    """
    tour = db.query(models.Tour).filter(models.Tour.id == tour_id).first()
    if not tour:
        raise HTTPException(status_code=404, detail="Tour không tồn tại")
    return tour


# ======================================================
# 📋 Danh sách tour + bộ lọc tìm kiếm
# ======================================================
@router.get("/", response_model=List[schemas.TourResponse])
def list_tours(
    q: Optional[str] = Query(None, description="Tìm kiếm theo tên / mô tả / loại / địa điểm"),
    type: Optional[str] = Query(None, description="Loại tour"),
    location: Optional[str] = Query(None, description="Địa điểm tour"),  # 🆕
    min_price: Optional[Decimal] = None,
    max_price: Optional[Decimal] = None,
    available: Optional[bool] = None,
    db: Session = Depends(get_db),
    limit: int = 50,
    offset: int = 0,
):
    """
    Lọc và tìm kiếm danh sách tour.
    Hỗ trợ: tìm theo tên, mô tả, loại, địa điểm, khoảng giá, trạng thái.
    """
    query = db.query(models.Tour)

    if q:
        like = f"%{q}%"
        query = query.filter(
            (models.Tour.name.ilike(like))
            | (models.Tour.description.ilike(like))
            | (models.Tour.type.ilike(like))
            | (models.Tour.location.ilike(like))  # 🆕 Thêm tìm kiếm theo location
        )

    if type:
        query = query.filter(models.Tour.type == type)
    if location:
        query = query.filter(models.Tour.location.ilike(f"%{location}%"))  # 🆕 Lọc theo location
    if min_price is not None:
        query = query.filter(models.Tour.price >= min_price)
    if max_price is not None:
        query = query.filter(models.Tour.price <= max_price)
    if available is not None:
        query = query.filter(models.Tour.available == available)

    tours = query.offset(offset).limit(limit).all()
    return tours


# ======================================================
# 🤖 Gợi ý tour thông minh (recommend)
# ======================================================
@router.post("/recommend", response_model=schemas.RecommendResponse)
def recommend(req: schemas.RecommendRequest, db: Session = Depends(get_db)):
    """
    Gợi ý tour thông minh (AI-like):
      - Lọc theo loại, số người, và ngân sách
      - Tính điểm ưu tiên (score)
      - Trả về top_n tour phù hợp nhất
    """
    number_people = req.number_people or 1
    budget = req.budget
    per_person = req.per_person if req.per_person is not None else True
    top_n = req.top_n or 10

    query = db.query(models.Tour).filter(models.Tour.available == True)

    # Lọc theo loại nếu có
    if req.type:
        query = query.filter(models.Tour.type == req.type)

    # Lọc theo số người phù hợp
    query = query.filter(
        models.Tour.min_people <= number_people,
        models.Tour.max_people >= number_people,
    )

    tours = query.all()
    if not tours:
        raise HTTPException(status_code=404, detail="Không có tour phù hợp")

    scored = []
    for t in tours:
        score = 0.0

        # Điểm loại tour
        if req.type and t.type == req.type:
            score += 3.0

        # Kiểm tra ngân sách
        if budget is not None:
            tour_price = float(t.price)
            if per_person:
                if tour_price <= float(budget):
                    ratio = max(0.1, tour_price / float(budget))
                    score += 2.0 * (1 - abs(1 - (1 / ratio))) + 1.0
                else:
                    continue
            else:
                total = tour_price * number_people
                if total <= float(budget):
                    ratio = max(0.1, total / float(budget))
                    score += 2.0 * (1 - abs(1 - (1 / ratio))) + 1.0
                else:
                    continue
        else:
            score += 0.5

        # Điểm rating trung bình
        rating = float(t.rating_avg or 0.0)
        score += rating * 0.2

        # Ưu tiên tour ngắn ngày
        if t.duration_days and t.duration_days <= 3:
            score += 0.2

        scored.append((score, rating, t))

    scored.sort(key=lambda x: (x[0], x[1]), reverse=True)
    selected = [item[2] for item in scored][:top_n]

    return {"tours": selected}
