#!/bin/bash

echo "🚀 Setting up Found It Mobile App..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if React Native CLI is installed
if ! command -v react-native &> /dev/null; then
    echo "📦 Installing React Native CLI..."
    npm install -g react-native-cli
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Install iOS dependencies (macOS only)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Installing iOS dependencies..."
    cd ios && pod install && cd ..
else
    echo "⚠️  Skipping iOS setup (not on macOS)"
fi

# Create necessary directories
echo "📁 Creating project structure..."
mkdir -p src/screens
mkdir -p src/components
mkdir -p src/context
mkdir -p src/services
mkdir -p src/utils
mkdir -p src/types

# Set up environment
echo "🔧 Setting up environment..."
if [ ! -f .env ]; then
    echo "API_BASE_URL=https://your-render-app.onrender.com" > .env
    echo "⚠️  Please update .env with your actual API URL"
fi

# Set up Android (if on Linux/macOS)
if [[ "$OSTYPE" == "linux-gnu"* ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🤖 Setting up Android..."
    cd android && ./gradlew clean && cd ..
fi

echo "✅ Setup complete!"
echo ""
echo "📱 Next steps:"
echo "1. Update API_BASE_URL in src/services/apiService.ts"
echo "2. Run 'npm start' to start Metro bundler"
echo "3. Run 'npm run android' or 'npm run ios' to launch the app"
echo ""
echo "🔗 For more information, see README.md"
