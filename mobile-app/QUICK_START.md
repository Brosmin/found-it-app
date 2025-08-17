# 🚀 Quick Start Guide

## Prerequisites
- Node.js (v16 or higher)
- React Native CLI: `npm install -g react-native-cli`
- Android Studio (for Android) or Xcode (for iOS)

## Step 1: Initialize React Native Project

```bash
# Navigate to mobile-app directory
cd mobile-app

# Install dependencies
npm install

# For iOS (macOS only)
cd ios && pod install && cd ..
```

## Step 2: Update API URL

Edit `src/services/apiService.ts` and change:
```typescript
const API_BASE_URL = 'https://your-render-app.onrender.com';
```
Replace with your actual Render app URL.

## Step 3: Run the App

### Android
```bash
npm run android
```

### iOS (macOS only)
```bash
npm run ios
```

### Metro Bundler (Development)
```bash
npm start
```

## Step 4: Build for Distribution

### Android APK
```bash
cd android
./gradlew assembleRelease
```
The APK will be in: `android/app/build/outputs/apk/release/app-release.apk`

### iOS Archive
```bash
cd ios
xcodebuild -workspace FoundItMobile.xcworkspace -scheme FoundItMobile -configuration Release archive -archivePath FoundItMobile.xcarchive
```

## 📱 Sharing the App

### Option 1: Development Build (Easiest)
1. Run `npm run android` or `npm run ios`
2. The app will install on your connected device
3. Share the APK file from `android/app/build/outputs/apk/release/`

### Option 2: Release Build
1. Build the release APK: `cd android && ./gradlew assembleRelease`
2. Find the APK in: `android/app/build/outputs/apk/release/app-release.apk`
3. Share this APK file directly

### Option 3: App Stores (Recommended for production)
1. Create developer accounts on Google Play Console and App Store Connect
2. Follow the deployment instructions in README.md
3. Share the app store links

## 🔧 Troubleshooting

### Common Issues:

1. **Metro bundler issues:**
```bash
npx react-native start --reset-cache
```

2. **Android build issues:**
```bash
cd android && ./gradlew clean && cd ..
```

3. **iOS build issues:**
```bash
cd ios && pod deintegrate && pod install && cd ..
```

4. **Network issues:**
- Check API_BASE_URL in apiService.ts
- Ensure your Flask backend has CORS enabled
- Verify the backend is running on Render

## 📱 Testing on Physical Device

### Android:
1. Enable Developer Options on your Android device
2. Enable USB Debugging
3. Connect device via USB
4. Run `npm run android`

### iOS:
1. Connect iPhone via USB
2. Trust the developer certificate
3. Run `npm run ios`

## 🎯 Next Steps

1. **Test the app** on your device
2. **Update the API URL** to your actual backend
3. **Customize the UI** as needed
4. **Deploy to app stores** for wider distribution

The app is now ready to use! It will work offline and sync when connected to the internet.
