import os
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError, ExpiredSignatureError
from typing import Optional, Dict, Any
import bcrypt

# ==========================
# ⚙️ Cấu hình JWT
# ==========================
SECRET_KEY = os.getenv("SECRET_KEY", "changemeplease")  # ⚠️ Đặt biến môi trường thật khi deploy
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 ngày

# ==========================
# 🔒 Cấu hình mã hoá mật khẩu
# ==========================
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
MAX_BCRYPT_PASSWORD_LENGTH = 72  # bcrypt chỉ hỗ trợ tối đa 72 bytes

# Kiểm tra phiên bản bcrypt an toàn (fix lỗi "trapped error reading bcrypt version")
try:
    bcrypt_version = getattr(bcrypt, "__version__", None)
except Exception:
    bcrypt_version = "unknown"


# ==========================
# 🔐 Mã hoá / kiểm tra mật khẩu
# ==========================
def hash_password(password: str) -> str:
    """
    Hash mật khẩu, truncate nếu quá dài để tránh lỗi bcrypt (>72 bytes)
    """
    truncated = password[:MAX_BCRYPT_PASSWORD_LENGTH]
    return pwd_context.hash(truncated)


def verify_password(plain: str, hashed: str) -> bool:
    """
    Kiểm tra password với hash, truncate nếu cần
    """
    if not plain or not hashed:
        return False
    truncated = plain[:MAX_BCRYPT_PASSWORD_LENGTH]
    try:
        return pwd_context.verify(truncated, hashed)
    except Exception:
        # Nếu hash lỗi (bcrypt version mismatch hoặc dữ liệu cũ)
        return False


# ==========================
# 🎟️ Tạo access token (JWT)
# ==========================
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Tạo JWT token có chứa user.id (sub) và role (admin/user)
    """
    to_encode = data.copy()

    # ✅ Đảm bảo token luôn có 'sub' và 'role'
    user_id = str(data.get("sub") or data.get("id"))
    role = data.get("role", "user")

    to_encode.update({"sub": user_id, "role": role})

    # Thêm thời gian hết hạn
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})

    # Mã hoá JWT
    encoded = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded


# ==========================
# 🔎 Giải mã access token
# ==========================
def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        # Token hết hạn
        return None
    except JWTError:
        # Token sai hoặc bị giả mạo
        return None
