#!/usr/bin/env python3
"""
Add Sample Images Script for FOUND IT Information System
This script adds sample images to existing items in the database.
"""

import os
import shutil
from app import app, db, Item

def add_sample_images():
    with app.app_context():
        # Ensure uploads directory exists
        uploads_dir = 'static/uploads'
        os.makedirs(uploads_dir, exist_ok=True)
        
        # Sample images mapping
        sample_images = {
            'iPhone 13 Found': 'iphone_sample.jpg',
            'Gold Ring Lost': 'gold_ring_sample.jpg', 
            'Red Backpack Found': 'red_backpack_sample.jpg',
            'Student ID Card Lost': 'student_id_sample.jpg',
            'Car Keys Found': 'car_keys_sample.jpg'
        }
        
        # Create sample image files with placeholder content
        for item_title, filename in sample_images.items():
            image_path = os.path.join(uploads_dir, filename)
            
            # Create a simple placeholder image file
            # In a real scenario, you would copy actual image files
            with open(image_path, 'w') as f:
                f.write(f"# Sample image for {item_title}\n")
                f.write("# This is a placeholder file\n")
                f.write("# In production, this would be an actual image file\n")
            
            print(f"Created placeholder image: {filename}")
        
        # Update items in database with image paths
        for item_title, filename in sample_images.items():
            item = Item.query.filter_by(title=item_title).first()
            if item:
                item.image_path = f'uploads/{filename}'
                print(f"Updated '{item_title}' with image: {filename}")
            else:
                print(f"Item not found: {item_title}")
        
        db.session.commit()
        print("\nSample images added successfully!")
        print("Note: These are placeholder files. Replace with actual images for production.")

if __name__ == '__main__':
    add_sample_images() 