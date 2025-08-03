#!/usr/bin/env python3
"""
Sample Data Setup Script for FOUND IT Information System
This script adds sample categories and items to make the system functional.
"""

from app import app, db, Category, Item, User
from datetime import datetime

def setup_sample_data():
    with app.app_context():
        # Check if we already have categories
        existing_categories = Category.query.all()
        if existing_categories:
            print("Categories already exist. Skipping category creation.")
            return
        
        print("Setting up sample data...")
        
        # Create sample categories
        categories = [
            Category(name="Electronics", description="Phones, laptops, tablets, and other electronic devices"),
            Category(name="Jewelry", description="Rings, necklaces, watches, and other jewelry items"),
            Category(name="Clothing", description="Shirts, pants, jackets, shoes, and other clothing items"),
            Category(name="Books & Documents", description="Books, notebooks, IDs, and important documents"),
            Category(name="Keys & Accessories", description="Keys, keychains, wallets, and small accessories"),
            Category(name="Sports Equipment", description="Balls, rackets, gym equipment, and sports gear"),
            Category(name="Other", description="Miscellaneous items that don't fit other categories")
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print(f"Created {len(categories)} categories:")
        for cat in categories:
            print(f"  - {cat.name}")
        
        # Create sample items
        sample_items = [
            {
                'title': 'iPhone 13 Found',
                'description': 'Found an iPhone 13 near the library entrance. Has a blue case.',
                'category_id': 1,  # Electronics
                'status': 'found',
                'location': 'Library Entrance',
                'contact_info': 'contact@university.edu',
                'image_path': 'uploads/iphone_sample.jpg',
                'is_approved': True
            },
            {
                'title': 'Gold Ring Lost',
                'description': 'Lost a gold wedding ring in the cafeteria area. Very sentimental value.',
                'category_id': 2,  # Jewelry
                'status': 'lost',
                'location': 'Cafeteria',
                'contact_info': 'john.doe@email.com',
                'image_path': 'uploads/gold_ring_sample.jpg',
                'is_approved': True
            },
            {
                'title': 'Red Backpack Found',
                'description': 'Found a red Jansport backpack in the computer lab. Contains textbooks.',
                'category_id': 3,  # Clothing
                'status': 'found',
                'location': 'Computer Lab B',
                'contact_info': 'lostandfound@university.edu',
                'image_path': 'uploads/red_backpack_sample.jpg',
                'is_approved': True
            },
            {
                'title': 'Student ID Card Lost',
                'description': 'Lost my student ID card somewhere on campus. Name: Sarah Johnson.',
                'category_id': 4,  # Books & Documents
                'status': 'lost',
                'location': 'Campus Grounds',
                'contact_info': 'sarah.johnson@student.edu',
                'image_path': 'uploads/student_id_sample.jpg',
                'is_approved': True
            },
            {
                'title': 'Car Keys Found',
                'description': 'Found car keys with a Toyota keychain in the parking lot.',
                'category_id': 5,  # Keys & Accessories
                'status': 'found',
                'location': 'Parking Lot A',
                'contact_info': 'security@university.edu',
                'image_path': 'uploads/car_keys_sample.jpg',
                'is_approved': True
            }
        ]
        
        for item_data in sample_items:
            item = Item(**item_data)
            db.session.add(item)
        
        db.session.commit()
        print(f"Created {len(sample_items)} sample items")
        
        print("\nSample data setup complete!")
        print("You can now:")
        print("1. Visit http://localhost:5000 to see the public site")
        print("2. Login to admin panel at http://localhost:5000/admin/login")
        print("   Username: admin, Password: admin123")

if __name__ == '__main__':
    setup_sample_data() 