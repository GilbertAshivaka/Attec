"""
Script to create an admin user.
Run this after setting up the database.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from app.db.session import SessionLocal
from app.models.user import User, UserRole
from app.core.security import get_password_hash
from app.core.config import settings
import uuid

def create_admin():
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        existing_admin = db.query(User).filter(
            User.email == settings.ADMIN_EMAIL
        ).first()
        
        if existing_admin:
            print(f"Admin user already exists: {settings.ADMIN_EMAIL}")
            return
        
        # Create admin user
        admin = User(
            id=uuid.uuid4(),
            email=settings.ADMIN_EMAIL,
            password=get_password_hash(settings.ADMIN_PASSWORD),
            name=settings.ADMIN_NAME,
            role=UserRole.ADMIN,
            active=True
        )
        
        db.add(admin)
        db.commit()
        
        print(f"✅ Admin user created successfully!")
        print(f"Email: {settings.ADMIN_EMAIL}")
        print(f"Password: {settings.ADMIN_PASSWORD}")
        print(f"\n⚠️  IMPORTANT: Change the password immediately after first login!")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
