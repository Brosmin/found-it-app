#!/usr/bin/env python3
"""
Test script for the authentication system
"""

from app import app, db, User
from werkzeug.security import generate_password_hash

def test_auth_system():
    with app.app_context():
        # Test user registration
        print("Testing user registration...")
        
        # Create a test user
        test_user = User(
            username='testuser',
            email='test@example.com',
            password_hash=generate_password_hash('testpass123'),
            role='staff'
        )
        
        # Check if user already exists
        existing_user = User.query.filter_by(username='testuser').first()
        if not existing_user:
            db.session.add(test_user)
            db.session.commit()
            print("✅ Test user created successfully")
        else:
            print("✅ Test user already exists")
        
        # Test admin user
        admin_user = User.query.filter_by(role='admin').first()
        if admin_user:
            print(f"✅ Admin user found: {admin_user.username}")
        else:
            print("❌ No admin user found")
        
        print("\nAuthentication system test completed!")
        print("You can now test the following:")
        print("1. Visit http://localhost:5000 to see the public site")
        print("2. Click 'Register' to create a new account")
        print("3. Click 'Login' to sign in")
        print("4. Admin login: http://localhost:5000/admin/login")
        print("   Username: admin, Password: admin123")

if __name__ == '__main__':
    test_auth_system() 