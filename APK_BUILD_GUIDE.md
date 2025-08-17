# FOUND IT Mobile App - APK Build Guide

## Current Status ✅

- ✅ API URL updated to: `https://found-it-app.onrender.com`
- ✅ Mobile app code structure complete
- ✅ Website download links configured
- ✅ Placeholder APK created
- ⏳ **Next: Build actual APK**

## Prerequisites Installation

### 1. Install Node.js
1. Go to https://nodejs.org/
2. Download the LTS version (recommended)
3. Run the installer and follow the wizard
4. Restart your terminal/PowerShell
5. Verify installation:
   ```bash
   node --version
   npm --version
   ```

### 2. Install Android Studio
1. Go to https://developer.android.com/studio
2. Download and install Android Studio
3. During installation, make sure to install:
   - Android SDK
   - Android SDK Platform
   - Android Virtual Device
4. Set up environment variables (optional but recommended)

## Building the APK

### Step 1: Setup React Native Project
```bash
cd mobile-app
python setup_react_native.py
```

### Step 2: Build APK
```bash
cd mobile-app
npm install
npx react-native run-android
```

### Step 3: Create Release APK
```bash
cd mobile-app/android
./gradlew assembleRelease
```

### Step 4: Copy APK to Website
```bash
# Copy the built APK to your website
copy "mobile-app/android/app/build/outputs/apk/release/app-release.apk" "static/downloads/FOUND IT.apk"
```

## Alternative: Quick Build Script

Once Node.js is installed, run:
```bash
python mobile-app/setup_react_native.py
```

This script will:
1. Check prerequisites
2. Setup React Native project
3. Install dependencies
4. Build the APK
5. Copy it to `static/downloads/FOUND IT.apk`

## Website Integration

Your website is already configured with:

### Download Links
- **Homepage**: Prominent "Download for Android" button
- **Navigation**: "Get App" button in header
- **Dedicated Page**: `/mobile-app` route with detailed information

### File Locations
- APK: `static/downloads/FOUND IT.apk`
- Installation Guide: `static/downloads/INSTALLATION_GUIDE.txt`

## Mobile App Features

The mobile app includes:
- ✅ **Offline-first design** - works without internet
- ✅ **Smart sync** - syncs when online
- ✅ **Modern UI** - React Native Paper components
- ✅ **Camera integration** - for item photos
- ✅ **GPS location** - for item locations
- ✅ **Push notifications** - for matches and updates
- ✅ **User authentication** - secure login
- ✅ **Search and filter** - find items easily

## API Integration

The mobile app is configured to connect to your Flask backend at:
```
https://found-it-app.onrender.com
```

## Deployment

1. **Build the APK** (follow steps above)
2. **Deploy your Flask app** to Render
3. **Users can download** the APK from your website
4. **Install on Android devices** - works on Android 5.0+

## Troubleshooting

### Common Issues
- **Node.js not found**: Install from https://nodejs.org/
- **Android SDK not found**: Install Android Studio
- **Build fails**: Check that all dependencies are installed
- **APK won't install**: Enable "Unknown sources" in Android settings

### Getting Help
- Check the console output for specific error messages
- Ensure all prerequisites are installed
- Verify environment variables are set correctly

## Next Steps

1. **Install Node.js and Android Studio**
2. **Run the build script**: `python mobile-app/setup_react_native.py`
3. **Deploy your Flask app** to Render
4. **Share the download link** with users

Your mobile app is ready to go! 🚀
