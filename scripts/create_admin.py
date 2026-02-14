#!/usr/bin/env python3
"""
Setup script to create initial admin user
"""
import asyncio
import sys
from getpass import getpass

from app.config.database import async_session_maker
from app.models.user import User, UserRole
from app.core.security import get_password_hash


async def create_admin_user():
    """Create admin user interactively"""
    print("=" * 50)
    print("CasaBricks Admin User Setup")
    print("=" * 50)
    print()
    
    # Get user input
    email = input("Enter admin email: ").strip()
    if not email:
        print("Error: Email is required")
        sys.exit(1)
    
    full_name = input("Enter full name: ").strip()
    if not full_name:
        print("Error: Full name is required")
        sys.exit(1)
    
    password = getpass("Enter password: ")
    if len(password) < 8:
        print("Error: Password must be at least 8 characters")
        sys.exit(1)
    
    password_confirm = getpass("Confirm password: ")
    if password != password_confirm:
        print("Error: Passwords do not match")
        sys.exit(1)
    
    # Create user
    async with async_session_maker() as db:
        # Check if user already exists
        from sqlalchemy import select
        result = await db.execute(
            select(User).where(User.email == email)
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            print(f"Error: User with email {email} already exists")
            sys.exit(1)
        
        # Create new admin user
        admin = User(
            email=email,
            hashed_password=get_password_hash(password),
            full_name=full_name,
            role=UserRole.SUPER_ADMIN,
            is_active=True
        )
        
        db.add(admin)
        await db.commit()
        await db.refresh(admin)
        
        print()
        print("=" * 50)
        print("Admin user created successfully!")
        print("=" * 50)
        print(f"Email: {admin.email}")
        print(f"Name: {admin.full_name}")
        print(f"Role: {admin.role.value}")
        print(f"ID: {admin.id}")
        print()
        print("You can now login at: /api/v1/auth/login")


if __name__ == "__main__":
    try:
        asyncio.run(create_admin_user())
    except KeyboardInterrupt:
        print("\nSetup cancelled")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)
