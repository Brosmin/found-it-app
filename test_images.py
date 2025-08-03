#!/usr/bin/env python3
"""
Test Images Script - Verify images are working
"""

from app import app, db, Item

def test_images():
    """Test that images are properly linked in the database"""
    
    with app.app_context():
        # Get all items with images
        items_with_images = Item.query.filter(Item.image_path.isnot(None)).all()
        
        print("Items with images:")
        for item in items_with_images:
            print(f"  - {item.title}: {item.image_path}")
        
        # Check if we have the expected items
        expected_items = [
            'iPhone 13 Found',
            'Gold Ring Lost', 
            'Red Backpack Found',
            'Student ID Card Lost',
            'Car Keys Found'
        ]
        
        print("\nChecking expected items:")
        for expected in expected_items:
            item = Item.query.filter_by(title=expected).first()
            if item and item.image_path:
                print(f"  ✅ {expected}: {item.image_path}")
            elif item:
                print(f"  ❌ {expected}: No image path")
            else:
                print(f"  ❌ {expected}: Item not found")
        
        print(f"\nTotal items with images: {len(items_with_images)}")

if __name__ == '__main__':
    test_images() 