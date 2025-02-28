# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
# from app import models, schemas

# from app.database import SessionLocal

# router = APIRouter()

# # Dependency to get database session
# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @router.post("/signup")
# def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
#     # Check if email already exists
#     db_user = db.query(models.User).filter(models.User.email == user.email).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     # Confirm passwords match
#     if user.password != user.confirm_password:
#         raise HTTPException(status_code=400, detail="Passwords do not match")

#     new_user = models.User(
#         full_name=user.full_name,
#         email=user.email,
#         password=user.password,  # Hash this in production
#         # phone=user.phone
#     )
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)

#     return {"message": "User created successfully"}


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import SessionLocal
from app.utils import hash_password  # Import password hashing function

router = APIRouter()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Confirm passwords match
    if user.password != user.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # ✅ Hash the password before storing it
    hashed_password = hash_password(user.password)

    new_user = models.User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,  # Store the hashed password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}
