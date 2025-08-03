#!/usr/bin/env python3
"""
Create Sample Images and Update Database
"""

import os
from PIL import Image, ImageDraw, ImageFont
from app import app, db, Item

def create_sample_images():
    # Ensure uploads directory exists
    uploads_dir = 'static/uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Sample images mapping
    sample_images = {
        'iphone_sample.jpg': 'iPhone 13',
        'gold_ring_sample.jpg': 'Gold Ring',
        'red_backpack_sample.jpg': 'Red Backpack', 
        'student_id_sample.jpg': 'Student ID Card',
        'car_keys_sample.jpg': 'Car Keys'
    }
    
    # Create sample images
    for filename, title in sample_images.items():
        # Create a simple image with text
        img = Image.new('RGB', (300, 200), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Add text to the image
        try:
            # Try to use a default font
            font = ImageFont.load_default()
        except:
            font = None
        
        # Draw text
        text = f"Sample Image\n{title}"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (300 - text_width) // 2
        y = (200 - text_height) // 2
        
        draw.text((x, y), text, fill='black', font=font)
        
        # Save the image
        image_path = os.path.join(uploads_dir, filename)
        img.save(image_path)
        print(f"Created sample image: {filename}")
    
    # Update database items
    with app.app_context():
        image_mapping = {
            'iPhone 13 Found': 'uploads/iphone_sample.jpg',
            'Gold Ring Lost': 'uploads/gold_ring_sample.jpg',
            'Red Backpack Found': 'uploads/red_backpack_sample.jpg', 
            'Student ID Card Lost': 'uploads/student_id_sample.jpg',
            'Car Keys Found': 'uploads/car_keys_sample.jpg'
        }
        
        for item_title, image_path in image_mapping.items():
            item = Item.query.filter_by(title=item_title).first()
            if item:
                item.image_path = image_path
                print(f"Updated '{item_title}' with image: {image_path}")
            else:
                print(f"Item not found: {item_title}")
        
        db.session.commit()
        print("\nSample images created and database updated successfully!")

if __name__ == '__main__':
    create_sample_images() 