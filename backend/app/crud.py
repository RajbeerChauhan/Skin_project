from sqlalchemy.orm import Session
from models import User
from schemas import UserCreate
import bcrypt

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate):
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password.decode("utf-8"),
    
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
