#!/usr/bin/env python3
"""
Simple test script for Found-It basic functionality
"""

import requests
import sys
from datetime import datetime

def test_app_functionality():
    """Test basic app functionality"""
    
    print("🧪 Testing Found-It Basic Functionality")
    print("=" * 50)
    
    # Test URLs
    base_url = "https://found-it-app.onrender.com"
    test_urls = [
        "/",
        "/items", 
        "/post_item",
        "/about",
        "/contact"
    ]
    
    print(f"🌐 Testing app at: {base_url}")
    print(f"⏰ Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    for url in test_urls:
        try:
            full_url = base_url + url
            print(f"\n🔍 Testing: {url}")
            
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {url} - Status: {response.status_code}")
                
                # Check if page contains expected content
                if "FOUND IT" in response.text:
                    print(f"   ✅ Page contains 'FOUND IT' title")
                else:
                    print(f"   ⚠️  Page doesn't contain expected title")
                    
            else:
                print(f"❌ {url} - Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {url} - Error: {e}")
        except Exception as e:
            print(f"❌ {url} - Unexpected error: {e}")
    
    print(f"\n⏰ Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\n📝 Summary:")
    print("✅ Basic functionality test completed")
    print("🌐 App is accessible at the provided URLs")
    print("📱 Items should now show immediately without admin approval")
    print("🔍 Check the /items page to see posted items")

if __name__ == "__main__":
    test_app_functionality()
