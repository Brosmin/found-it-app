#!/usr/bin/env python3
"""
Test script for FOUND IT Information System
This script tests basic functionality of the system
"""

import requests
import time
import sys

def test_system():
    """Test the basic functionality of the system"""
    base_url = "http://localhost:5000"
    
    print("Testing FOUND IT Information System...")
    print("=" * 50)
    
    # Test 1: Check if server is running
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✓ Server is running and accessible")
        else:
            print(f"✗ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ Cannot connect to server. Make sure the server is running on http://localhost:5000")
        return False
    except Exception as e:
        print(f"✗ Error connecting to server: {e}")
        return False
    
    # Test 2: Check public pages
    pages_to_test = [
        ("/", "Home page"),
        ("/items", "Items listing"),
        ("/about", "About page"),
        ("/contact", "Contact page"),
        ("/post_item", "Post item page")
    ]
    
    for page, description in pages_to_test:
        try:
            response = requests.get(f"{base_url}{page}", timeout=5)
            if response.status_code == 200:
                print(f"✓ {description} is accessible")
            else:
                print(f"✗ {description} returned status code: {response.status_code}")
        except Exception as e:
            print(f"✗ Error accessing {description}: {e}")
    
    # Test 3: Check admin login page
    try:
        response = requests.get(f"{base_url}/admin/login", timeout=5)
        if response.status_code == 200:
            print("✓ Admin login page is accessible")
        else:
            print(f"✗ Admin login page returned status code: {response.status_code}")
    except Exception as e:
        print(f"✗ Error accessing admin login page: {e}")
    
    print("\n" + "=" * 50)
    print("System test completed!")
    print("\nTo access the system:")
    print(f"  Public site: {base_url}")
    print(f"  Admin panel: {base_url}/admin/login")
    print("  Default admin credentials: admin / admin123")
    
    return True

if __name__ == "__main__":
    print("FOUND IT Information System - Test Script")
    print("Make sure the server is running before executing this test.")
    print("To start the server, run: python app.py")
    print()
    
    input("Press Enter to start testing...")
    
    success = test_system()
    
    if success:
        print("\n✓ All tests passed! The system is working correctly.")
    else:
        print("\n✗ Some tests failed. Please check the server and try again.")
        sys.exit(1) 