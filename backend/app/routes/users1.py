from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models1 import User
from app.schemas1 import RegisterSchema, LoginSchema
from app.utils import create_access_token

router = APIRouter()




# ✅ Login Route (Validates Plaintext Passwords)
from app.utils import verify_password  # Import password verification function

@router.post("/login")
def login(user_credentials: LoginSchema, db: Session = Depends(get_db)):
    print("\n📌 Received login request")
    print(f"📧 Entered Email: {user_credentials.email}")
    print(f"🔑 Entered Password: {user_credentials.password}")

    # Fetch user from the database
    user = db.query(User).filter(User.email == user_credentials.email).first()

    if not user:
        print(f"❌ User with email '{user_credentials.email}' NOT found in database")
        all_users = db.query(User).all()  # Fetch all users
        print("📌 Existing Users in DB:", [(u.id, u.email) for u in all_users])  # ✅ Debug: See all users
        raise HTTPException(status_code=401, detail="Invalid email or password")

    print(f"✅ User found: {user.email}")
    print(f"🛠️ Stored Hashed Password: {user.password}")

    # Check password verification
    is_password_valid = verify_password(user_credentials.password, user.password)
    print(f"🛠️ Password Verification Result: {is_password_valid}")

    if not is_password_valid:
        print("❌ Password does not match")
        raise HTTPException(status_code=401, detail="Invalid email or password")

    print("✅ User authenticated successfully!")
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
