from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from .. import models, schemas
from ..database import get_db
from ..routers.auth import get_current_user
from decimal import Decimal

router = APIRouter(prefix="/bookings", tags=["bookings"])


# 🧾 1️⃣ Tạo booking mới
@router.post("/", response_model=schemas.BookingResponse)
def create_booking(
    bk: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    tour = db.query(models.Tour).get(bk.tour_id)
    if not tour or not tour.available:
        raise HTTPException(status_code=404, detail="Tour not available")

    if bk.number_people < tour.min_people or bk.number_people > tour.max_people:
        raise HTTPException(
            status_code=400,
            detail=f"Number of people must be between {tour.min_people} and {tour.max_people}"
        )

    total = Decimal(tour.price) * bk.number_people
    booking = models.Booking(
        user_id=current_user.id,
        tour_id=tour.id,
        number_people=bk.number_people,
        total_price=total,
        status="pending"
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


# 📋 2️⃣ Lấy danh sách booking của người dùng
@router.get("/me", response_model=list[schemas.BookingResponse])
def my_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    bookings = (
        db.query(models.Booking)
        .options(joinedload(models.Booking.tour))
        .filter(models.Booking.user_id == current_user.id)
        .all()
    )
    return bookings  # ✅ Trả trực tiếp ORM object, FastAPI tự chuyển theo schema


# 🔍 3️⃣ Xem chi tiết 1 booking cụ thể
@router.get("/{booking_id}", response_model=schemas.BookingResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booking = (
        db.query(models.Booking)
        .options(joinedload(models.Booking.tour))
        .get(booking_id)
    )

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    return booking  # ✅ Trả trực tiếp ORM object


# ❌ 4️⃣ Hủy booking (người dùng chỉ được hủy tour của chính mình)
@router.delete("/{booking_id}")
def cancel_booking(
    booking_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    booking = db.query(models.Booking).get(booking_id)

    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Chỉ chủ sở hữu hoặc admin mới có quyền hủy
    if booking.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")

    # Không thể hủy booking đã thanh toán
    if booking.status == "paid":
        raise HTTPException(status_code=400, detail="Cannot cancel a paid booking")

    db.delete(booking)
    db.commit()

    return {"message": "Booking cancelled successfully"}
