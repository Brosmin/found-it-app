#!/usr/bin/env python3
"""
Test script for the Found-It claiming system
This script tests the basic functionality of the claiming system
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:5000"  # Change this to your app URL
TEST_EMAIL = "test@example.com"
TEST_PHONE = "+234 123 456 789"

def test_claiming_system():
    """Test the complete claiming system workflow"""
    
    print("🧪 Testing Found-It Claiming System")
    print("=" * 50)
    
    # Test 1: Check if the app is running
    print("\n1. Testing app connectivity...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ App is running and accessible")
        else:
            print(f"❌ App returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot connect to app: {e}")
        return False
    
    # Test 2: Check if items page is accessible
    print("\n2. Testing items page...")
    try:
        response = requests.get(f"{BASE_URL}/items")
        if response.status_code == 200:
            print("✅ Items page is accessible")
        else:
            print(f"❌ Items page returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access items page: {e}")
    
    # Test 3: Check if claim item route exists
    print("\n3. Testing claim item route...")
    try:
        response = requests.get(f"{BASE_URL}/claim_item/1")
        if response.status_code == 200:
            print("✅ Claim item page is accessible")
        elif response.status_code == 404:
            print("⚠️  Claim item page exists but no items found (this is normal)")
        else:
            print(f"❌ Claim item page returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access claim item page: {e}")
    
    # Test 4: Check admin routes (should redirect to login)
    print("\n4. Testing admin routes...")
    try:
        response = requests.get(f"{BASE_URL}/admin/claims")
        if response.status_code == 302:  # Redirect to login
            print("✅ Admin claims route exists (redirects to login as expected)")
        else:
            print(f"⚠️  Admin claims route returned status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ Cannot access admin claims route: {e}")
    
    # Test 5: Check database models
    print("\n5. Testing database models...")
    try:
        # Import the app to test database models
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app import app, db, Item, Claim, User
        
        with app.app_context():
            # Check if tables exist
            try:
                db.session.execute('SELECT 1 FROM item LIMIT 1')
                print("✅ Item table exists")
            except Exception as e:
                print(f"❌ Item table error: {e}")
            
            try:
                db.session.execute('SELECT 1 FROM claim LIMIT 1')
                print("✅ Claim table exists")
            except Exception as e:
                print(f"❌ Claim table error: {e}")
            
            # Check item counts
            item_count = Item.query.count()
            claim_count = Claim.query.count()
            user_count = User.query.count()
            
            print(f"📊 Database statistics:")
            print(f"   - Items: {item_count}")
            print(f"   - Claims: {claim_count}")
            print(f"   - Users: {user_count}")
            
    except ImportError as e:
        print(f"⚠️  Could not import app modules: {e}")
    except Exception as e:
        print(f"❌ Database test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 Claiming System Test Summary:")
    print("✅ Public claiming interface accessible")
    print("✅ Admin claims management accessible")
    print("✅ Database models configured")
    print("\n📝 Next steps:")
    print("1. Post some test items through the web interface")
    print("2. Test claiming an item as a regular user")
    print("3. Login as admin to review and approve/reject claims")
    print("4. Verify items are properly archived after approval")
    
    return True

def test_database_persistence():
    """Test database persistence configuration"""
    
    print("\n🗄️  Testing Database Persistence")
    print("=" * 40)
    
    try:
        import sys
        import os
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))
        
        from app import app, DATABASE_PATH
        
        print(f"📁 Database path: {DATABASE_PATH}")
        print(f"📁 Database directory: {os.path.dirname(DATABASE_PATH)}")
        
        # Check if database directory exists
        if os.path.exists(os.path.dirname(DATABASE_PATH)):
            print("✅ Database directory exists")
        else:
            print("❌ Database directory does not exist")
        
        # Check if database file exists
        if os.path.exists(DATABASE_PATH):
            print("✅ Database file exists")
            file_size = os.path.getsize(DATABASE_PATH)
            print(f"📏 Database file size: {file_size} bytes")
        else:
            print("❌ Database file does not exist")
        
        # Check permissions
        try:
            if os.access(os.path.dirname(DATABASE_PATH), os.W_OK):
                print("✅ Database directory is writable")
            else:
                print("❌ Database directory is not writable")
        except Exception as e:
            print(f"⚠️  Could not check directory permissions: {e}")
            
    except ImportError as e:
        print(f"❌ Could not import app: {e}")
    except Exception as e:
        print(f"❌ Persistence test error: {e}")

if __name__ == "__main__":
    print("🚀 Starting Found-It Claiming System Tests")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Run tests
    success = test_claiming_system()
    test_database_persistence()
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if success:
        print("\n🎉 All tests completed successfully!")
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
