#!/usr/bin/env python3
"""
Database Initialization Script for Render Deployment
"""
from app import app, db, User, Category, Item, Message, SystemInfo
from werkzeug.security import generate_password_hash

def init_database():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Check if admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                username='admin',
                email='admin@foundit.com',
                password_hash=generate_password_hash('admin123'),
                role='admin',
                is_active=True
            )
            db.session.add(admin_user)
            print("✅ Admin user created!")
        
        # Check if categories exist
        if Category.query.count() == 0:
            # Create sample categories
            categories = [
                Category(name='Electronics', description='Phones, laptops, tablets, etc.'),
                Category(name='Jewelry', description='Rings, necklaces, watches, etc.'),
                Category(name='Clothing', description='Shirts, pants, jackets, etc.'),
                Category(name='Documents', description='IDs, cards, papers, etc.'),
                Category(name='Keys', description='Car keys, house keys, etc.'),
                Category(name='Other', description='Miscellaneous items')
            ]
            for category in categories:
                db.session.add(category)
            print("✅ Sample categories created!")
        
        # Check if system info exists
        system_info = SystemInfo.query.first()
        if not system_info:
            system_info = SystemInfo(
                site_name='FOUND IT',
                contact_email='contact@foundit.com',
                contact_phone='+1234567890',
                address='University Campus',
                description='A comprehensive found items management system'
            )
            db.session.add(system_info)
            print("✅ System info created!")
        
        # Commit all changes
        db.session.commit()
        print("✅ Database initialization completed successfully!")
        print("📊 Database Summary:")
        print(f"   - Users: {User.query.count()}")
        print(f"   - Categories: {Category.query.count()}")
        print(f"   - Items: {Item.query.count()}")
        print(f"   - Messages: {Message.query.count()}")

if __name__ == '__main__':
    init_database() 