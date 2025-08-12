from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import config, models


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


SECRET_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str):
    return pwd_context.verify(plain, hashed)


def create_access_token(data: dict, expires_minutes: int = 60):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_minutes)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def check_permission(db: Session, user_id: int, resource_name: str, required_perm: str):
    resource = db.query(models.Resource).filter_by(name=resource_name).first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")

    user_res = db.query(models.UserResource).filter_by(
        user_id=user_id,
        resource_id=resource.id
    ).first()

    if not user_res or required_perm not in user_res.permissions:
        raise HTTPException(
            status_code=403,
            detail=f"Missing permission: {required_perm}"
        )
