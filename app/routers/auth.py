from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import RegisterIn, LoginIn, TokenOut
from app import models
from app.db import SessionLocal
from app.auth_utils import hash_password, verify_password, create_access_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenOut)
def register(payload: RegisterIn, db: Session = Depends(get_db)):
    if db.query(models.User).filter_by(email=payload.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = models.User(
        name=payload.name,
        email=payload.email,
        role="student",
        hashed_password=hash_password(payload.password)
    )
    db.add(user)
    db.commit()
    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)

@router.post("/login", response_model=TokenOut)
def login(payload: LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email=payload.email).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    token = create_access_token(sub=user.email)
    return TokenOut(access_token=token)