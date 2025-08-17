#!/usr/bin/env python3
"""
React Native Setup and APK Build Script
This script helps set up the React Native project and build the APK.
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

def run_command(command, cwd=None):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Error running command: {command}")
            print(f"Error: {result.stderr}")
            return False
        print(f"Success: {command}")
        print(result.stdout)
        return True
    except Exception as e:
        print(f"Exception running command {command}: {e}")
        return False

def check_prerequisites():
    """Check if required tools are installed"""
    print("Checking prerequisites...")
    
    # Check Node.js
    if not run_command("node --version"):
        print("❌ Node.js is not installed or not in PATH")
        print("Please install Node.js from https://nodejs.org/")
        return False
    
    # Check npm
    if not run_command("npm --version"):
        print("❌ npm is not installed or not in PATH")
        return False
    
    # Check React Native CLI
    if not run_command("npx react-native --version"):
        print("⚠️  React Native CLI not found, will install it")
    
    print("✅ Prerequisites check completed")
    return True

def setup_react_native_project():
    """Set up the React Native project structure"""
    print("\nSetting up React Native project...")
    
    # Navigate to mobile-app directory
    mobile_app_dir = Path("mobile-app")
    if not mobile_app_dir.exists():
        print("❌ mobile-app directory not found")
        return False
    
    os.chdir(mobile_app_dir)
    
    # Install dependencies
    print("Installing npm dependencies...")
    if not run_command("npm install"):
        print("❌ Failed to install dependencies")
        return False
    
    # Initialize React Native project if Android directory doesn't exist
    android_dir = Path("android")
    if not android_dir.exists():
        print("Android directory not found. Initializing React Native project...")
        
        # Create a temporary React Native project to get the Android structure
        temp_project = "temp_rn_project"
        if run_command(f"npx react-native init {temp_project} --template react-native-template-typescript"):
            # Copy Android and iOS directories
            if Path(f"{temp_project}/android").exists():
                shutil.copytree(f"{temp_project}/android", "android")
                print("✅ Android directory created")
            
            if Path(f"{temp_project}/ios").exists():
                shutil.copytree(f"{temp_project}/ios", "ios")
                print("✅ iOS directory created")
            
            # Copy other necessary files
            for file in ["metro.config.js", "index.js", "react-native.config.js"]:
                if Path(f"{temp_project}/{file}").exists():
                    shutil.copy2(f"{temp_project}/{file}", ".")
            
            # Clean up temporary project
            shutil.rmtree(temp_project)
        else:
            print("❌ Failed to initialize React Native project")
            return False
    
    print("✅ React Native project setup completed")
    return True

def build_apk():
    """Build the Android APK"""
    print("\nBuilding Android APK...")
    
    # Navigate to mobile-app directory
    mobile_app_dir = Path("mobile-app")
    if not mobile_app_dir.exists():
        print("❌ mobile-app directory not found")
        return False
    
    os.chdir(mobile_app_dir)
    
    # Check if Android directory exists
    android_dir = Path("android")
    if not android_dir.exists():
        print("❌ Android directory not found. Please run setup first.")
        return False
    
    # Build the APK
    print("Building release APK...")
    if run_command("cd android && ./gradlew assembleRelease"):
        print("✅ APK built successfully")
        
        # Find the APK file
        apk_path = Path("android/app/build/outputs/apk/release/app-release.apk")
        if apk_path.exists():
            # Copy to static/downloads directory
            target_dir = Path("../../static/downloads")
            target_dir.mkdir(parents=True, exist_ok=True)
            
            target_path = target_dir / "FOUND IT.apk"
            shutil.copy2(apk_path, target_path)
            print(f"✅ APK copied to: {target_path}")
            return True
        else:
            print("❌ APK file not found at expected location")
            return False
    else:
        print("❌ Failed to build APK")
        return False

def main():
    """Main function"""
    print("🚀 React Native Setup and APK Build Script")
    print("=" * 50)
    
    # Check prerequisites
    if not check_prerequisites():
        print("\n❌ Prerequisites not met. Please install required tools.")
        return
    
    # Setup React Native project
    if not setup_react_native_project():
        print("\n❌ Failed to setup React Native project.")
        return
    
    # Build APK
    if not build_apk():
        print("\n❌ Failed to build APK.")
        return
    
    print("\n🎉 Success! Your APK has been built and placed in static/downloads/FOUND IT.apk")
    print("\nNext steps:")
    print("1. Deploy your Flask app to Render")
    print("2. The APK will be available at: https://found-it-app.onrender.com/static/downloads/FOUND IT.apk")
    print("3. Users can download and install the APK on their Android devices")

if __name__ == "__main__":
    main()
