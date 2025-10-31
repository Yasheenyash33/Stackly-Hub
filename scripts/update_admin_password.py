#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import database.database as db_module
import database.models as models_module
from passlib.context import CryptContext

SessionLocal = db_module.SessionLocal
User = models_module.User
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def update_admin_password():
    db = SessionLocal()
    try:
        # Find admin user
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            print("Admin user not found.")
            return

        # Hash the new password
        new_password = "admin1234"
        hashed_password = pwd_context.hash(new_password)

        # Update the password
        admin_user.password_hash = hashed_password
        admin_user.is_temporary_password = False  # Set to False since it's being set explicitly
        db.commit()
        print(f"Admin password updated to '{new_password}'")

    except Exception as e:
        print(f"Error updating admin password: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_admin_password()
