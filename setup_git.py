#!/usr/bin/env python3
"""
Git Setup Helper Script for FOUND IT Project
This script helps set up Git repository and guides through GitHub deployment.
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e}")
        print(f"Error output: {e.stderr}")
        return None

def check_git_installed():
    """Check if Git is installed"""
    try:
        subprocess.run(['git', '--version'], check=True, capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def main():
    print("🚀 FOUND IT - Git Setup Helper")
    print("=" * 50)
    
    # Check if Git is installed
    if not check_git_installed():
        print("❌ Git is not installed or not in PATH.")
        print("Please install Git from: https://git-scm.com/")
        print("After installation, restart this script.")
        return
    
    print("✅ Git is installed!")
    
    # Check if we're in the project directory
    if not os.path.exists('app.py'):
        print("❌ Please run this script from the project root directory (where app.py is located)")
        return
    
    print("✅ Found project files!")
    
    # Initialize Git repository
    if not os.path.exists('.git'):
        run_command('git init', 'Initializing Git repository')
    else:
        print("✅ Git repository already exists")
    
    # Add all files
    run_command('git add .', 'Adding all files to Git')
    
    # Create initial commit
    run_command('git commit -m "Initial commit: FOUND IT Smart Lost and Found System"', 'Creating initial commit')
    
    print("\n🎉 Git repository setup completed!")
    print("\n📋 Next Steps:")
    print("1. Create a GitHub repository:")
    print("   - Go to https://github.com/new")
    print("   - Name it: found-it-app")
    print("   - Make it public or private")
    print("   - Don't initialize with README (we already have one)")
    
    print("\n2. Connect your local repository to GitHub:")
    print("   git remote add origin https://github.com/YOUR_USERNAME/found-it-app.git")
    print("   git branch -M main")
    print("   git push -u origin main")
    
    print("\n3. Deploy to Render:")
    print("   - Go to https://render.com")
    print("   - Create account and connect GitHub")
    print("   - Create new Web Service")
    print("   - Select your found-it-app repository")
    print("   - Build Command: pip install -r requirements.txt")
    print("   - Start Command: gunicorn wsgi:app")
    
    print("\n4. Your app will be live at: https://found-it-app.onrender.com")
    
    print("\n🔧 For future updates:")
    print("   git add .")
    print("   git commit -m 'Your update message'")
    print("   git push")
    print("   (Render will automatically redeploy)")
    
    print("\n🎓 Your Computer Engineering Final Year Project is ready!")
    print("Features included:")
    print("✅ Smart Matching Algorithm")
    print("✅ Real-time Notifications")
    print("✅ Advanced Analytics Dashboard")
    print("✅ RESTful API Endpoints")
    print("✅ Enhanced Search & Filtering")
    print("✅ Mobile App Ready APIs")

if __name__ == "__main__":
    main() 