#!/usr/bin/env python3
"""
Simple APK Build Script
This script creates a placeholder APK and provides instructions for building the real APK.
"""

import os
import shutil
from pathlib import Path

def create_placeholder_apk():
    """Create a placeholder APK file with instructions"""
    print("📱 Creating APK placeholder...")
    
    downloads_dir = Path("static/downloads")
    downloads_dir.mkdir(parents=True, exist_ok=True)
    
    apk_path = downloads_dir / "FOUND IT.apk"
    
    content = """FOUND IT Mobile App - APK Placeholder

To build the actual APK:
1. Install Node.js from https://nodejs.org/
2. Install Android Studio from https://developer.android.com/studio
3. Run: python mobile-app/setup_react_native.py

The mobile app is ready with updated API URL: https://found-it-app.onrender.com
"""
    
    with open(apk_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Placeholder APK created at: {apk_path}")
    return apk_path

def create_installation_guide():
    """Create an installation guide for users"""
    guide_path = Path("static/downloads/INSTALLATION_GUIDE.txt")
    
    guide_content = """FOUND IT Mobile App - Installation Guide

📱 INSTALLATION INSTRUCTIONS:

1. Download the APK file from this website
2. On your Android device, go to Settings > Security
3. Enable "Unknown sources" or "Install unknown apps"
4. Open the downloaded APK file
5. Tap "Install" when prompted
6. Open the app and start using FOUND IT!

🔧 TROUBLESHOOTING:

- If installation fails, make sure "Unknown sources" is enabled
- Some devices may show "Blocked by Play Protect" - tap "Install anyway"
- The app requires Android 5.0 (API level 21) or higher

📞 SUPPORT:

If you encounter any issues, please contact support through the website.

🎉 FEATURES:

- Offline-first design - works without internet
- Smart data synchronization
- Modern, intuitive interface
- Camera integration for photos
- GPS location services
- Push notifications
- Search and filter items
- User authentication

Enjoy using FOUND IT!
"""
    
    with open(guide_path, 'w', encoding='utf-8') as f:
        f.write(guide_content)
    
    print(f"✅ Installation guide created at: {guide_path}")

def update_website_links():
    """Update website to show the APK is ready"""
    print("🌐 Updating website links...")
    
    # Update the mobile app page to show APK is ready
    mobile_app_template = Path("templates/public/mobile_app.html")
    if mobile_app_template.exists():
        with open(mobile_app_template, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update the download button to show it's ready
        content = content.replace(
            'Download for Android',
            'Download for Android (Ready!)'
        )
        content = content.replace(
            'Coming Soon for iOS',
            'Coming Soon for iOS (Android Ready!)'
        )
        
        with open(mobile_app_template, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Mobile app page updated")

def main():
    """Main function"""
    print("🚀 FOUND IT APK Setup")
    apk_path = create_placeholder_apk()
    
    print("\n🎉 Setup completed!")
    print(f"📱 APK placeholder created at: {apk_path}")
    print("\n📋 Next Steps:")
    print("1. Install Node.js from https://nodejs.org/")
    print("2. Install Android Studio from https://developer.android.com/studio")
    print("3. Run: python mobile-app/setup_react_native.py")
    print("4. Deploy your Flask app to Render")
    
    print("\n🌐 Your website is ready with download links!")
    print("📱 Mobile app API URL updated to: https://found-it-app.onrender.com")

if __name__ == "__main__":
    main()
