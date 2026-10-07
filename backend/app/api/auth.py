from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.core.config import settings
from app.deps import current_user
from app.models import AuditLog, User
from app.schemas import LoginIn, RegisterIn, Token, UserOut

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    email = payload.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(409, "Account already exists")
    import os
    role = "admin" if email == os.getenv("BOOTSTRAP_ADMIN_EMAIL", "").lower() and os.getenv("BOOTSTRAP_ADMIN_EMAIL") else "analyst"
    user = User(email=email, full_name=payload.full_name.strip(), password_hash=hash_password(payload.password), role=role)
    db.add(user); db.commit(); db.refresh(user)
    db.add(AuditLog(user_id=user.id, action="register", details=f"role={user.role}")); db.commit()
    return Token(access_token=create_access_token(user.id, user.email, user.role))

@router.post("/login", response_model=Token)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")
    db.add(AuditLog(user_id=user.id, action="login", details="successful")); db.commit()
    return Token(access_token=create_access_token(user.id, user.email, user.role))

@router.get("/me", response_model=UserOut)
def me(user: User = Depends(current_user)):
    return user
