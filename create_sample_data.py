#!/usr/bin/env python3
"""
Create Sample Data for FOUND IT System
This script creates sample items with images for demonstration.
"""

import os
import shutil
from datetime import datetime
from app import app, db, User, Category, Item, SystemInfo

def create_sample_data():
    with app.app_context():
        print("🔄 Creating sample data...")
        
        # Ensure upload directory exists
        upload_dir = 'static/uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Create sample images if they don't exist
        sample_images = {
            'iphone_sample.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
            'laptop_sample.jpg': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',
            'keys_sample.jpg': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
            'wallet_sample.jpg': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop',
            'book_sample.jpg': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop',
            'watch_sample.jpg': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=300&fit=crop',
            'backpack_sample.jpg': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
            'glasses_sample.jpg': 'https://images.unsplash.com/photo-1577803645773-f96470509666?w=400&h=300&fit=crop'
        }
        
        # Create sample items
        sample_items = [
            {
                'title': 'iPhone 13 Pro - Lost',
                'description': 'Lost my iPhone 13 Pro with blue case. Last seen in the library. Has a cracked screen protector.',
                'category': 'Electronics',
                'status': 'lost',
                'location': 'Main Library',
                'contact_info': 'john.doe@email.com',
                'brand': 'Apple',
                'model': 'iPhone 13 Pro',
                'color': 'Blue',
                'condition': 'Good',
                'image': 'iphone_sample.jpg'
            },
            {
                'title': 'MacBook Pro - Found',
                'description': 'Found a MacBook Pro in the computer lab. Silver color, no stickers.',
                'category': 'Electronics',
                'status': 'found',
                'location': 'Computer Lab A',
                'contact_info': 'admin@foundit.com',
                'brand': 'Apple',
                'model': 'MacBook Pro',
                'color': 'Silver',
                'condition': 'Excellent',
                'image': 'laptop_sample.jpg'
            },
            {
                'title': 'Car Keys - Lost',
                'description': 'Lost my car keys with Toyota keychain. Has a small flashlight attached.',
                'category': 'Keys',
                'status': 'lost',
                'location': 'Parking Lot B',
                'contact_info': 'jane.smith@email.com',
                'brand': 'Toyota',
                'color': 'Black',
                'condition': 'Good',
                'image': 'keys_sample.jpg'
            },
            {
                'title': 'Leather Wallet - Found',
                'description': 'Found a brown leather wallet near the cafeteria. Contains some cards.',
                'category': 'Documents',
                'status': 'found',
                'location': 'Cafeteria',
                'contact_info': 'admin@foundit.com',
                'brand': 'Unknown',
                'color': 'Brown',
                'condition': 'Good',
                'image': 'wallet_sample.jpg'
            },
            {
                'title': 'Physics Textbook - Lost',
                'description': 'Lost my physics textbook "University Physics" by Young and Freedman.',
                'category': 'Books',
                'status': 'lost',
                'location': 'Science Building',
                'contact_info': 'student@email.com',
                'brand': 'Pearson',
                'color': 'Blue',
                'condition': 'Used',
                'image': 'book_sample.jpg'
            },
            {
                'title': 'Gold Watch - Found',
                'description': 'Found a gold-colored watch in the gym. Looks expensive.',
                'category': 'Jewelry',
                'status': 'found',
                'location': 'Gymnasium',
                'contact_info': 'admin@foundit.com',
                'brand': 'Unknown',
                'color': 'Gold',
                'condition': 'Excellent',
                'image': 'watch_sample.jpg'
            },
            {
                'title': 'Nike Backpack - Lost',
                'description': 'Lost my black Nike backpack with laptop compartment. Has my name tag inside.',
                'category': 'Clothing',
                'status': 'lost',
                'location': 'Student Center',
                'contact_info': 'mike.wilson@email.com',
                'brand': 'Nike',
                'color': 'Black',
                'condition': 'Good',
                'image': 'backpack_sample.jpg'
            },
            {
                'title': 'Ray-Ban Sunglasses - Found',
                'description': 'Found black Ray-Ban sunglasses in the courtyard.',
                'category': 'Other',
                'status': 'found',
                'location': 'Courtyard',
                'contact_info': 'admin@foundit.com',
                'brand': 'Ray-Ban',
                'color': 'Black',
                'condition': 'Excellent',
                'image': 'glasses_sample.jpg'
            }
        ]
        
        # Add sample items
        for item_data in sample_items:
            category = Category.query.filter_by(name=item_data['category']).first()
            if category:
                item = Item(
                    title=item_data['title'],
                    description=item_data['description'],
                    category_id=category.id,
                    status=item_data['status'],
                    location=item_data['location'],
                    contact_info=item_data['contact_info'],
                    brand=item_data['brand'],
                    color=item_data['color'],
                    condition=item_data['condition'],
                    is_approved=True,
                    image_path=f"uploads/{item_data['image']}"
                )
                db.session.add(item)
        
        # Update system info
        system_info = SystemInfo.query.first()
        if system_info:
            system_info.about_content = """
            Welcome to FOUND IT - Your Smart Lost and Found System!
            
            Our AI-powered platform helps you find lost items and return found ones quickly and efficiently. 
            With advanced matching algorithms, real-time notifications, and comprehensive search capabilities, 
            we make the process of reuniting people with their belongings as simple as possible.
            
            Features:
            • Smart AI Matching
            • Real-time Notifications
            • Advanced Search & Filtering
            • Mobile-Ready APIs
            • Comprehensive Analytics
            
            Whether you've lost something or found an item, FOUND IT is here to help!
            """
            system_info.contact_email = "admin@foundit.com"
            system_info.contact_phone = "+234 810 678 1706"
            system_info.contact_address = "ABU Zaria, Main Campus, Nigeria"
        
        db.session.commit()
        print("✅ Sample data created successfully!")
        print(f"✅ Added {len(sample_items)} sample items")
        print("✅ Updated system information")

if __name__ == "__main__":
    create_sample_data() 