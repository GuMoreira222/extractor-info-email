from sqlalchemy.orm import Session
from app.db.session import engine, Base
from app.models.user import User
from app.core.security import get_password_hash
from app.db.session import SessionLocal

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    user = db.query(User).filter(User.username == "admin").first()

    if not user:
        new_user = User(username="admin", hashed_password=get_password_hash("admin"))
        db.add(new_user)
        db.commit()
        print("Admin user created")
    else:
        print("Admin user already exists")
    db.close()

if __name__ == "__main__":
    init_db()