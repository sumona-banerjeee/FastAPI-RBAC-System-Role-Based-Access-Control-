from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, utils, database

router = APIRouter()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if crud.get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    
    return crud.create_user(db, user, role=user.role, is_active=False)




@router.post("/login")
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, login_data.email)
    if not user or not utils.verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account not approved by Superadmin")

    token = utils.create_access_token({"sub": user.email, "role": user.role})

    if user.role == "superadmin":
        return {
            "message": f"Welcome Superadmin {user.name}",
            "access_token": token,
            "token_type": "bearer"
        }
    else:
        return {
            "message": f"Welcome {user.name}",
            "access_token": token,
            "token_type": "bearer"
        }
