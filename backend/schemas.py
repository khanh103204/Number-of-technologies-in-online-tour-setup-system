from pydantic import BaseModel, EmailStr, PositiveInt
from typing import Optional, List
from decimal import Decimal
from datetime import datetime


# ---------- USER ----------
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# ---------- TOUR ----------
class TourBase(BaseModel):
    name: str
    location: str                     # 🆕 có location
    type: str
    description: Optional[str] = None
    price: Decimal
    min_people: Optional[int] = None
    max_people: Optional[int] = None
    duration_days: Optional[int] = None
    difficulty: Optional[str] = "easy"
    rating_avg: Optional[Decimal] = 0.0
    available: Optional[bool] = True


class TourCreate(TourBase):
    pass


class TourUpdate(BaseModel):
    name: Optional[str]
    location: Optional[str]            # 🆕 để cập nhật location
    type: Optional[str]
    description: Optional[str]
    price: Optional[Decimal]
    min_people: Optional[int]
    max_people: Optional[int]
    duration_days: Optional[int]
    difficulty: Optional[str]
    rating_avg: Optional[Decimal]
    available: Optional[bool]


class TourResponse(TourBase):
    id: int
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# ---------- RECOMMEND ----------
class RecommendRequest(BaseModel):
    type: Optional[str] = None
    number_people: Optional[int] = 1
    budget: Optional[Decimal] = None
    per_person: Optional[bool] = True
    top_n: Optional[int] = 10
    location: Optional[str] = None     # 🆕 Thêm location cho Recommend


class RecommendResponse(BaseModel):
    tours: List[TourResponse]


# ---------- BOOKING ----------
class BookingCreate(BaseModel):
    tour_id: int
    number_people: PositiveInt


class BookingResponse(BaseModel):
    id: int
    user_id: Optional[int] = None
    tour_id: Optional[int] = None
    tour: Optional[TourResponse] = None
    number_people: int
    total_price: Decimal
    status: str
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# ---------- PAYMENT ----------
class PaymentCreate(BaseModel):
    booking_id: int
    amount: Decimal
    method: str   # 'VNPay', 'Momo', 'Visa', 'QR'


class PaymentResponse(BaseModel):
    id: int
    booking_id: int
    amount: Decimal
    method: str
    status: str
    paid_at: Optional[datetime]
    created_at: Optional[datetime]

    class Config:
        orm_mode = True


# ---------- AUTH TOKEN ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
