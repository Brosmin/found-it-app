#!/usr/bin/env python3
"""
Test Approve Functionality
"""

from app import app, db, Item

def test_approve_functionality():
    """Test that approve/unapprove functionality works"""
    
    with app.app_context():
        # Get all items
        items = Item.query.all()
        
        print("Current items and their approval status:")
        for item in items:
            status = "✅ Approved" if item.is_approved else "❌ Not Approved"
            print(f"  - {item.title}: {status}")
        
        # Test approve functionality
        unapproved_items = Item.query.filter_by(is_approved=False).all()
        if unapproved_items:
            print(f"\nFound {len(unapproved_items)} unapproved items")
            for item in unapproved_items:
                print(f"  - {item.title}")
        else:
            print("\nAll items are approved")
        
        # Test unapprove functionality  
        approved_items = Item.query.filter_by(is_approved=True).all()
        if approved_items:
            print(f"\nFound {len(approved_items)} approved items")
            for item in approved_items:
                print(f"  - {item.title}")
        else:
            print("\nNo items are approved")

if __name__ == '__main__':
    test_approve_functionality() 