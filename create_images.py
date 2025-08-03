#!/usr/bin/env python3
"""
Create placeholder image files
"""

import os

def create_placeholder_images():
    # Ensure uploads directory exists
    uploads_dir = 'static/uploads'
    os.makedirs(uploads_dir, exist_ok=True)
    
    # Sample images mapping
    sample_images = {
        'iphone_sample.jpg': 'iPhone 13 Sample Image',
        'gold_ring_sample.jpg': 'Gold Ring Sample Image',
        'red_backpack_sample.jpg': 'Red Backpack Sample Image', 
        'student_id_sample.jpg': 'Student ID Card Sample Image',
        'car_keys_sample.jpg': 'Car Keys Sample Image'
    }
    
    # Create placeholder image files
    for filename, description in sample_images.items():
        image_path = os.path.join(uploads_dir, filename)
        
        # Create a simple text file as placeholder
        with open(image_path, 'w') as f:
            f.write(f"# {description}\n")
            f.write("# This is a placeholder image file\n")
            f.write("# Replace with actual image for production\n")
        
        print(f"Created placeholder image: {filename}")
    
    print("\nPlaceholder images created successfully!")
    print("You can now:")
    print("1. Replace these files with actual images")
    print("2. Update the database through admin panel")
    print("3. Or run the database update script")

if __name__ == '__main__':
    create_placeholder_images() 