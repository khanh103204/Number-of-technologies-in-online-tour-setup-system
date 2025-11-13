# backend/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from jose import JWTError
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

from .. import models, schemas
from ..database import get_db
from ..utils import hash_password, verify_password, create_access_token, decode_access_token

# ==========================================
# 🚪 AUTH ROUTER
# ==========================================
router = APIRouter(prefix="/auth", tags=["auth"])

# ✅ Điều chỉnh tokenUrl phù hợp với router prefix (tránh lỗi khi dùng /api)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

# ==========================================
# 👤 Đăng ký người dùng thường
# ==========================================
@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    db_user = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="user",  # luôn là user khi đăng ký thường
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


# ==========================================
# 🛡️ Đăng ký ADMIN (chỉ nội bộ)
# ==========================================
@router.post("/register-admin", response_model=schemas.UserResponse)
def register_admin(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email đã tồn tại")

    db_admin = models.User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="admin",
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


# ==========================================
# 🔑 Đăng nhập -> trả JWT token
# ==========================================
@router.post("/token", response_model=schemas.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Đăng nhập bằng email và mật khẩu
    Trả về access_token có chứa id, email và role của user
    """
    user = db.query(models.User).filter(models.User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email hoặc mật khẩu không đúng",
        )

    # ✅ Thêm cả email + role vào token để frontend và backend đều nhận diện đúng
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "role": user.role,
    }
    token = create_access_token(token_data)

    return {"access_token": token, "token_type": "bearer"}


# ==========================================
# 👓 Lấy user hiện tại từ token
# ==========================================
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    """
    Giải mã token, lấy thông tin user hiện tại và đảm bảo token hợp lệ
    """
    try:
        payload = decode_access_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Token không hợp lệ")
    except JWTError:
        raise HTTPException(status_code=401, detail="Token hết hạn hoặc không hợp lệ")

    user_id = payload.get("sub")
    role = payload.get("role")
    email = payload.get("email")

    if not user_id:
        raise HTTPException(status_code=401, detail="Thiếu thông tin người dùng trong token")

    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    # ✅ Đồng bộ role theo token để tránh lệch
    if role and user.role != role:
        user.role = role

    return user


# ==========================================
# 🧩 Kiểm tra quyền ADMIN
# ==========================================
def require_admin(current_user: models.User = Depends(get_current_user)):
    """
    Chỉ cho phép truy cập nếu user có vai trò admin
    """
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Chỉ quản trị viên mới được phép truy cập")
    return current_user


# ==========================================
# 👤 Endpoint lấy thông tin user hiện tại
# ==========================================
@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: models.User = Depends(get_current_user)):
    """
    Trả về thông tin người dùng hiện tại từ token
    """
    return current_user
