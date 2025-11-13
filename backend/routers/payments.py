# backend/routers/payments.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from .. import models, schemas
from ..database import get_db
from ..routers.auth import get_current_user

router = APIRouter(prefix="/payments", tags=["payments"])

@router.post("/", response_model=schemas.PaymentResponse)
def create_payment(
    payment_data: schemas.PaymentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Thanh toán cho booking
    - Bất kỳ user nào cũng có thể thanh toán.
    - Admin không cần thanh toán, chỉ quản lý tour.
    """

    # ✅ 1. Kiểm tra booking có tồn tại
    booking = db.query(models.Booking).get(payment_data.booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking không tồn tại")

    # ✅ 2. Kiểm tra số tiền hợp lệ
    try:
        amount = float(payment_data.amount)
    except ValueError:
        raise HTTPException(status_code=400, detail="Số tiền không hợp lệ")

    if amount != float(booking.total_price):
        raise HTTPException(
            status_code=400,
            detail=f"Số tiền thanh toán ({amount}) phải bằng tổng tiền booking ({booking.total_price})",
        )

    # ✅ 3. Tạo bản ghi thanh toán
    payment = models.Payment(
        booking_id=booking.id,
        amount=amount,
        method=payment_data.method,
        status="success",  # giả lập thanh toán thành công
        paid_at=datetime.utcnow(),
        created_at=datetime.utcnow(),
    )
    db.add(payment)

    # ✅ 4. Cập nhật trạng thái booking
    booking.status = "paid"

    db.commit()
    db.refresh(payment)

    return payment
