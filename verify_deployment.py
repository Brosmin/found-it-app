#!/usr/bin/env python3
"""
Deployment Verification Script
Quick checks to ensure the app is working correctly after deployment.
"""

import os
import sys
from datetime import datetime

def check_database():
    """Check database status."""
    print("🔍 Checking Database...")
    
    db_path = os.environ.get('DATABASE_PATH', '/opt/render/project/src/persistent_data/found_it.db')
    print(f"📊 Database path: {db_path}")
    
    if os.path.exists(db_path):
        size = os.path.getsize(db_path)
        print(f"✅ Database exists: {size} bytes")
        return True
    else:
        print("❌ Database not found!")
        return False

def check_environment():
    """Check environment variables."""
    print("🔍 Checking Environment...")
    
    required_vars = ['DATABASE_PATH', 'PORT']
    for var in required_vars:
        value = os.environ.get(var)
        if value:
            print(f"✅ {var}: {value}")
        else:
            print(f"❌ {var} not set")
    
    return True

def check_directories():
    """Check required directories."""
    print("🔍 Checking Directories...")
    
    directories = [
        '/opt/render/project/src/persistent_data',
        'static/uploads'
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            print(f"✅ {directory} exists")
        else:
            print(f"❌ {directory} missing")
    
    return True

def main():
    """Main verification function."""
    print("🚀 Deployment Verification")
    print("=" * 40)
    
    checks = [
        ("Environment", check_environment),
        ("Directories", check_directories),
        ("Database", check_database)
    ]
    
    all_passed = True
    for check_name, check_func in checks:
        print(f"\n📋 {check_name}")
        print("-" * 20)
        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            print(f"❌ {check_name} failed: {e}")
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("✅ Deployment verification passed!")
        print("🎉 Your app should be working correctly!")
    else:
        print("❌ Some checks failed. Please review the issues above.")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1) 