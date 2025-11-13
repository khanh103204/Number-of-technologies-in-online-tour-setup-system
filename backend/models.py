from sqlalchemy import (
    Column, Integer, String, DECIMAL, Boolean, Text, Enum,
    ForeignKey, TIMESTAMP
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .database import Base


# ------------------- USER -------------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, unique=True, index=True)
    password = Column(String(255), nullable=False)
    role = Column(Enum('user', 'admin', name='user_roles'), nullable=False, default='user')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Quan hệ với Booking
    bookings = relationship("Booking", back_populates="user", cascade="all, delete-orphan")


# ------------------- TOUR -------------------
class Tour(Base):
    __tablename__ = "tours"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    location = Column(String(150), nullable=False)  # 🆕 Địa điểm tour
    type = Column(String(50), nullable=False)  # Ví dụ: 'biển', 'leo núi', 'city tour', ...
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(12, 2), nullable=False)
    min_people = Column(Integer, nullable=False, default=1)
    max_people = Column(Integer, nullable=False, default=10)
    difficulty = Column(Enum('easy', 'medium', 'hard', name='tour_difficulty'), nullable=False, default='easy')
    duration_days = Column(Integer, nullable=False, default=1)
    rating_avg = Column(DECIMAL(3, 2), nullable=False, default=0.0)
    available = Column(Boolean, nullable=False, default=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Quan hệ với Booking
    bookings = relationship("Booking", back_populates="tour", cascade="all, delete-orphan")


# ------------------- BOOKING -------------------
class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    tour_id = Column(Integer, ForeignKey("tours.id", ondelete="RESTRICT"), nullable=False)
    number_people = Column(Integer, nullable=False)
    total_price = Column(DECIMAL(12, 2), nullable=False)
    status = Column(Enum('pending', 'paid', 'cancelled', name='booking_status'), nullable=False, default='pending')
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    # Quan hệ liên kết
    user = relationship("User", back_populates="bookings")
    tour = relationship("Tour", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")


# ------------------- PAYMENT -------------------
class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey("bookings.id", ondelete="CASCADE"), nullable=False)
    amount = Column(DECIMAL(12, 2), nullable=False)
    method = Column(String(50), nullable=False)  # 'VNPay', 'Momo', 'Visa', 'QR'
    status = Column(Enum('success', 'failed', 'pending', name='payment_status'), nullable=False, default='pending')
    paid_at = Column(TIMESTAMP(timezone=True), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)

    booking = relationship("Booking", back_populates="payments")
