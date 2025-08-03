#!/usr/bin/env python3
"""
Create Real Images Script - Generate actual PNG images
"""

import os
from app import app, db, Item

def create_real_images():
    """Create actual PNG images using a simple approach"""
    
    # Ensure uploads directory exists
    uploads_dir = 'static/uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Create simple SVG images that can be converted to PNG
    image_data = {
        'iphone_sample.png': {
            'color': '#007AFF',
            'text': 'iPhone 13',
            'icon': '📱'
        },
        'gold_ring_sample.png': {
            'color': '#FFD700',
            'text': 'Gold Ring',
            'icon': '💍'
        },
        'red_backpack_sample.png': {
            'color': '#DC143C',
            'text': 'Red Backpack',
            'icon': '🎒'
        },
        'student_id_sample.png': {
            'color': '#228B22',
            'text': 'Student ID',
            'icon': '🆔'
        },
        'car_keys_sample.png': {
            'color': '#696969',
            'text': 'Car Keys',
            'icon': '🔑'
        }
    }
    
    # Create SVG files that can be served as images
    for filename, data in image_data.items():
        svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="300" height="200" xmlns="http://www.w3.org/2000/svg">
    <rect width="300" height="200" fill="{data['color']}"/>
    <text x="150" y="80" font-family="Arial, sans-serif" font-size="48" text-anchor="middle" fill="white">{data['icon']}</text>
    <text x="150" y="120" font-family="Arial, sans-serif" font-size="24" text-anchor="middle" fill="white">{data['text']}</text>
    <text x="150" y="150" font-family="Arial, sans-serif" font-size="16" text-anchor="middle" fill="white">Sample Image</text>
</svg>"""
        
        # Save as SVG file
        file_path = os.path.join(uploads_dir, filename.replace('.png', '.svg'))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        print(f"Created image: {filename}")
    
    # Update database with image paths
    with app.app_context():
        image_mapping = {
            'iPhone 13 Found': 'uploads/iphone_sample.svg',
            'Gold Ring Lost': 'uploads/gold_ring_sample.svg',
            'Red Backpack Found': 'uploads/red_backpack_sample.svg',
            'Student ID Card Lost': 'uploads/student_id_sample.svg',
            'Car Keys Found': 'uploads/car_keys_sample.svg'
        }
        
        for item_title, image_path in image_mapping.items():
            item = Item.query.filter_by(title=item_title).first()
            if item:
                item.image_path = image_path
                print(f"Updated '{item_title}' with image: {image_path}")
            else:
                print(f"Item not found: {item_title}")
        
        db.session.commit()
        print("\n✅ Real images created and database updated successfully!")
        print("The images are now SVG files that will display properly in the browser.")

if __name__ == '__main__':
    create_real_images() 