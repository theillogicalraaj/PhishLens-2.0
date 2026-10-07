from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.deps import admin_user
from app.models import AuditLog, User

router=APIRouter(prefix="/api/v1/admin",tags=["admin"])
@router.get("/audit")
def audit(db:Session=Depends(get_db),_:User=Depends(admin_user)):
    logs=db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(200).all()
    return [{"id":x.id,"user_id":x.user_id,"action":x.action,"details":x.details,"created_at":x.created_at} for x in logs]
