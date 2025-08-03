#!/usr/bin/env python3
"""
Update Items with Images Script
"""

from app import app, db, Item

def update_items_with_images():
    with app.app_context():
        # Sample images mapping
        sample_images = {
            'iPhone 13 Found': 'uploads/iphone_sample.jpg',
            'Gold Ring Lost': 'uploads/gold_ring_sample.jpg', 
            'Red Backpack Found': 'uploads/red_backpack_sample.jpg',
            'Student ID Card Lost': 'uploads/student_id_sample.jpg',
            'Car Keys Found': 'uploads/car_keys_sample.jpg'
        }
        
        # Update items in database with image paths
        for item_title, image_path in sample_images.items():
            item = Item.query.filter_by(title=item_title).first()
            if item:
                item.image_path = image_path
                print(f"Updated '{item_title}' with image: {image_path}")
            else:
                print(f"Item not found: {item_title}")
        
        db.session.commit()
        print("\nItems updated with image paths successfully!")

if __name__ == '__main__':
    update_items_with_images() 