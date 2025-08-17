#!/usr/bin/env python3
"""
Build script for FOUND IT Mobile App APK
This script will build the React Native app and place the APK in the static downloads folder.
"""

import os
import subprocess
import shutil
import sys

def run_command(command, cwd=None):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        print(f"Success: {result.stdout}")
        return True
    except Exception as e:
        print(f"Exception running command: {e}")
        return False

def main():
    print("🚀 Building FOUND IT Mobile App APK...")
    
    # Check if mobile-app directory exists
    if not os.path.exists('mobile-app'):
        print("❌ mobile-app directory not found!")
        print("Please make sure you're in the project root directory.")
        return False
    
    # Navigate to mobile-app directory
    os.chdir('mobile-app')
    
    # Install dependencies
    print("📦 Installing dependencies...")
    if not run_command('npm install'):
        print("❌ Failed to install dependencies")
        return False
    
    # Create downloads directory if it doesn't exist
    downloads_dir = '../static/downloads'
    os.makedirs(downloads_dir, exist_ok=True)
    
    # For now, create a placeholder APK file
    # In a real scenario, you would build the actual React Native app
    apk_path = os.path.join(downloads_dir, 'FOUND IT.apk')
    
    print("📱 Creating placeholder APK file...")
    
    # Create a simple placeholder file
    with open(apk_path, 'w') as f:
        f.write("FOUND IT Mobile App APK\n")
        f.write("This is a placeholder file.\n")
        f.write("In a real deployment, this would be the actual APK file.\n")
        f.write("\nTo build the actual APK:\n")
        f.write("1. cd mobile-app\n")
        f.write("2. npm install\n")
        f.write("3. cd android\n")
        f.write("4. ./gradlew assembleRelease\n")
        f.write("5. Copy app-release.apk to static/downloads/FOUND IT.apk\n")
    
    print(f"✅ Placeholder APK created at: {apk_path}")
    print("\n📋 Next steps to build the actual APK:")
    print("1. Install React Native CLI: npm install -g react-native-cli")
    print("2. Install Android Studio and configure Android SDK")
    print("3. Run: cd mobile-app && npm install")
    print("4. Run: cd android && ./gradlew assembleRelease")
    print("5. Copy the generated APK to static/downloads/FOUND IT.apk")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
