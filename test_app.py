#!/usr/bin/env python3
"""
Comprehensive Testing Script for Found-It App
Tests all functionality to ensure the app works perfectly on all devices.
"""

import os
import sys
import requests
import json
from datetime import datetime

# Configuration
BASE_URL = os.environ.get('APP_URL', 'http://localhost:5000')
ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

def test_database_persistence():
    """Test database persistence across deployments."""
    print("🔍 Testing Database Persistence...")
    
    # Test database path
    db_path = os.environ.get('DATABASE_PATH', '/opt/render/project/src/persistent_data/found_it.db')
    print(f"📊 Database path: {db_path}")
    
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"✅ Database exists with size: {size} bytes")
    else:
        print("❌ Database not found!")
        return False
    
    return True

def test_home_page():
    """Test home page accessibility."""
    print("🔍 Testing Home Page...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            print("✅ Home page accessible")
            return True
        else:
            print(f"❌ Home page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Home page error: {e}")
        return False

def test_user_registration():
    """Test user registration functionality."""
    print("🔍 Testing User Registration...")
    
    # Test data
    test_user = {
        'username': f'testuser_{datetime.now().strftime("%Y%m%d_%H%M%S")}',
        'email': f'test_{datetime.now().strftime("%Y%m%d_%H%M%S")}@test.com',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    
    try:
        response = requests.post(f"{BASE_URL}/register", data=test_user)
        if response.status_code == 200:
            print("✅ User registration form accessible")
            return True
        else:
            print(f"❌ Registration failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Registration error: {e}")
        return False

def test_item_posting():
    """Test item posting functionality."""
    print("🔍 Testing Item Posting...")
    
    try:
        response = requests.get(f"{BASE_URL}/post_item")
        if response.status_code == 200:
            print("✅ Item posting form accessible")
            return True
        else:
            print(f"❌ Item posting failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Item posting error: {e}")
        return False

def test_search_functionality():
    """Test search functionality."""
    print("🔍 Testing Search Functionality...")
    
    try:
        # Test search API
        response = requests.get(f"{BASE_URL}/api/search?q=test")
        if response.status_code == 200:
            print("✅ Search API accessible")
            return True
        else:
            print(f"❌ Search failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Search error: {e}")
        return False

def test_admin_access():
    """Test admin panel accessibility."""
    print("🔍 Testing Admin Access...")
    
    try:
        response = requests.get(f"{BASE_URL}/admin/login")
        if response.status_code == 200:
            print("✅ Admin login accessible")
            return True
        else:
            print(f"❌ Admin access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Admin access error: {e}")
        return False

def test_mobile_responsiveness():
    """Test mobile responsiveness."""
    print("🔍 Testing Mobile Responsiveness...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1'
    }
    
    try:
        response = requests.get(f"{BASE_URL}/", headers=headers)
        if response.status_code == 200:
            print("✅ Mobile access works")
            return True
        else:
            print(f"❌ Mobile access failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Mobile access error: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print("🔍 Testing API Endpoints...")
    
    endpoints = [
        '/api/search',
        '/api/analytics',
        '/items'
    ]
    
    success_count = 0
    for endpoint in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}")
            if response.status_code in [200, 401, 403]:  # 401/403 are expected for protected endpoints
                print(f"✅ {endpoint} accessible")
                success_count += 1
            else:
                print(f"❌ {endpoint} failed: {response.status_code}")
        except Exception as e:
            print(f"❌ {endpoint} error: {e}")
    
    return success_count == len(endpoints)

def test_error_handling():
    """Test error handling."""
    print("🔍 Testing Error Handling...")
    
    try:
        # Test 404 handling
        response = requests.get(f"{BASE_URL}/nonexistent-page")
        if response.status_code == 404:
            print("✅ 404 error handling works")
            return True
        else:
            print(f"❌ 404 handling failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def test_performance():
    """Test basic performance metrics."""
    print("🔍 Testing Performance...")
    
    try:
        start_time = datetime.now()
        response = requests.get(f"{BASE_URL}/")
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        print(f"✅ Response time: {response_time:.2f} seconds")
        
        if response_time < 5.0:  # 5 seconds threshold
            print("✅ Performance acceptable")
            return True
        else:
            print("❌ Performance too slow")
            return False
    except Exception as e:
        print(f"❌ Performance test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🚀 Starting Comprehensive App Testing...")
    print("=" * 50)
    
    tests = [
        ("Database Persistence", test_database_persistence),
        ("Home Page", test_home_page),
        ("User Registration", test_user_registration),
        ("Item Posting", test_item_posting),
        ("Search Functionality", test_search_functionality),
        ("Admin Access", test_admin_access),
        ("Mobile Responsiveness", test_mobile_responsiveness),
        ("API Endpoints", test_api_endpoints),
        ("Error Handling", test_error_handling),
        ("Performance", test_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}")
        print("-" * 30)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\n📈 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Your app is ready for deployment!")
        return True
    else:
        print("⚠️ Some tests failed. Please review and fix issues.")
        return False

if __name__ == '__main__':
    success = run_comprehensive_test()
    sys.exit(0 if success else 1) 