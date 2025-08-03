#!/usr/bin/env python3
"""
Fix Images Script - Create placeholder images and update database
"""

import os
import base64
from app import app, db, Item

def create_simple_images():
    """Create simple placeholder images using base64 encoded data"""
    
    # Ensure uploads directory exists
    uploads_dir = 'static/uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Simple colored rectangles as placeholder images
    image_data = {
        'iphone_sample.jpg': {
            'color': '#007AFF',  # iPhone blue
            'text': 'iPhone 13'
        },
        'gold_ring_sample.jpg': {
            'color': '#FFD700',  # Gold
            'text': 'Gold Ring'
        },
        'red_backpack_sample.jpg': {
            'color': '#DC143C',  # Crimson red
            'text': 'Red Backpack'
        },
        'student_id_sample.jpg': {
            'color': '#228B22',  # Forest green
            'text': 'Student ID'
        },
        'car_keys_sample.jpg': {
            'color': '#696969',  # Dim gray
            'text': 'Car Keys'
        }
    }
    
    # Create simple HTML files as placeholder images
    for filename, data in image_data.items():
        html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>{data['text']} Sample Image</title>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            background-color: {data['color']};
            color: white;
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 200px;
            text-align: center;
        }}
        .container {{
            background-color: rgba(0,0,0,0.3);
            padding: 20px;
            border-radius: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h2>{data['text']}</h2>
        <p>Sample Image</p>
    </div>
</body>
</html>
"""
        
        # Save as HTML file (we'll use this as a placeholder)
        file_path = os.path.join(uploads_dir, filename.replace('.jpg', '.html'))
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"Created placeholder image: {filename}")
    
    # Update database with image paths
    with app.app_context():
        image_mapping = {
            'iPhone 13 Found': 'uploads/iphone_sample.html',
            'Gold Ring Lost': 'uploads/gold_ring_sample.html',
            'Red Backpack Found': 'uploads/red_backpack_sample.html',
            'Student ID Card Lost': 'uploads/student_id_sample.html',
            'Car Keys Found': 'uploads/car_keys_sample.html'
        }
        
        for item_title, image_path in image_mapping.items():
            item = Item.query.filter_by(title=item_title).first()
            if item:
                item.image_path = image_path
                print(f"Updated '{item_title}' with image: {image_path}")
            else:
                print(f"Item not found: {item_title}")
        
        db.session.commit()
        print("\n✅ Images created and database updated successfully!")
        print("Note: These are HTML placeholder images. Replace with actual JPG/PNG files for production.")

if __name__ == '__main__':
    create_simple_images() 