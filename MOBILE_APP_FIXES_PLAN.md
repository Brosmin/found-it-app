# Mobile App Installation Issues Fix Plan

## Current Issues
Based on the project structure, the mobile app has several issues:
1. Missing screen components (ItemDetailScreen, RegisterScreen, PostItemScreen, etc.)
2. Incomplete implementation of core features
3. Missing build configuration files
4. Incomplete setup process

## Implementation Plan

### 1. Create Missing Screen Components

#### a. Create ItemDetailScreen
Create `mobile-app/src/screens/ItemDetailScreen.tsx`:

```typescript
import React from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Image,
  Alert,
} from 'react-native';
import {
  Card,
  Title,
  Paragraph,
  Button,
  Text,
  Chip,
} from 'react-native-paper';
import { useNavigation, useRoute } from '@react-navigation/native';

interface Item {
  id: number;
  title: string;
  description: string;
  status: 'found' | 'lost' | 'recovered' | 'removed';
  location: string;
  image_path?: string;
  category: {
    name: string;
    color: string;
  };
  created_at: string;
  isOffline?: boolean;
}

export default function ItemDetailScreen() {
  const navigation = useNavigation();
  const route = useRoute();
  const { item } = route.params as { item: Item };

  const handleClaimItem = () => {
    Alert.alert('Claim Item', 'This feature will be implemented in the full version.');
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        {item.image_path && (
          <Image source={{ uri: item.image_path }} style={styles.itemImage} />
        )}
        
        <Card.Content>
          <View style={styles.itemHeader}>
            <Title style={styles.itemTitle}>{item.title}</Title>
            <Chip
              mode="outlined"
              style={[
                styles.statusChip,
                { 
                  backgroundColor: 
                    item.status === 'found' ? '#4CAF50' : 
                    item.status === 'lost' ? '#FF9800' : 
                    item.status === 'recovered' ? '#2196F3' : 
                    '#9E9E9E'
                }
              ]}
              textStyle={{ color: 'white' }}
            >
              {item.status.toUpperCase()}
            </Chip>
          </View>
          
          <Paragraph style={styles.itemDescription}>
            {item.description}
          </Paragraph>
          
          <View style={styles.itemDetails}>
            <Text style={styles.detailLabel}>Category:</Text>
            <Text style={styles.detailValue}>{item.category.name}</Text>
          </View>
          
          <View style={styles.itemDetails}>
            <Text style={styles.detailLabel}>Location:</Text>
            <Text style={styles.detailValue}>{item.location}</Text>
          </View>
          
          <View style={styles.itemDetails}>
            <Text style={styles.detailLabel}>Posted:</Text>
            <Text style={styles.detailValue}>
              {new Date(item.created_at).toLocaleDateString()}
            </Text>
          </View>
        </Card.Content>
      </Card>
      
      <View style={styles.buttonContainer}>
        <Button
          mode="contained"
          onPress={handleClaimItem}
          style={styles.claimButton}
          disabled={item.status !== 'found'}
        >
          Claim This Item
        </Button>
        
        <Button
          mode="outlined"
          onPress={() => navigation.goBack()}
          style={styles.backButton}
        >
          Back to Items
        </Button>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    margin: 16,
    elevation: 2,
  },
  itemImage: {
    width: '100%',
    height: 250,
    resizeMode: 'cover',
  },
  itemHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  itemTitle: {
    flex: 1,
    fontSize: 24,
  },
  statusChip: {
    marginLeft: 8,
  },
  itemDescription: {
    fontSize: 16,
    lineHeight: 24,
    marginBottom: 16,
  },
  itemDetails: {
    flexDirection: 'row',
    marginBottom: 8,
  },
  detailLabel: {
    fontWeight: 'bold',
    width: 100,
  },
  detailValue: {
    flex: 1,
  },
  buttonContainer: {
    padding: 16,
  },
  claimButton: {
    marginBottom: 12,
  },
  backButton: {
    borderColor: '#2196F3',
  },
});
```

#### b. Create RegisterScreen
Create `mobile-app/src/screens/RegisterScreen.tsx`:

```typescript
import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
} from 'react-native';
import {
  TextInput,
  Button,
  Text,
  Card,
  Title,
  Paragraph,
} from 'react-native-paper';
import { useAuth } from '../context/AuthContext';
import { useNavigation } from '@react-navigation/native';

export default function RegisterScreen() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  
  const { register } = useAuth();
  const navigation = useNavigation();

  const handleRegister = async () => {
    if (!username || !email || !password || !confirmPassword) {
      Alert.alert('Error', 'Please fill in all fields');
      return;
    }

    if (password !== confirmPassword) {
      Alert.alert('Error', 'Passwords do not match');
      return;
    }

    if (password.length < 6) {
      Alert.alert('Error', 'Password must be at least 6 characters long');
      return;
    }

    setIsLoading(true);
    try {
      const success = await register({ username, email, password });
      if (success) {
        Alert.alert('Success', 'Registration successful!', [
          { text: 'OK', onPress: () => navigation.navigate('Login') }
        ]);
      } else {
        Alert.alert('Registration Failed', 'Please try again');
      }
    } catch (error) {
      Alert.alert('Error', 'Network error. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContainer}>
        <View style={styles.logoContainer}>
          <Text style={styles.logo}>🔍</Text>
          <Title style={styles.title}>Found It</Title>
          <Paragraph style={styles.subtitle}>
            Find your lost items, help others find theirs
          </Paragraph>
        </View>

        <Card style={styles.card}>
          <Card.Content>
            <Title style={styles.cardTitle}>Create Account</Title>
            
            <TextInput
              label="Username"
              value={username}
              onChangeText={setUsername}
              mode="outlined"
              style={styles.input}
              autoCapitalize="none"
              autoCorrect={false}
            />

            <TextInput
              label="Email"
              value={email}
              onChangeText={setEmail}
              mode="outlined"
              style={styles.input}
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
            />

            <TextInput
              label="Password"
              value={password}
              onChangeText={setPassword}
              mode="outlined"
              style={styles.input}
              secureTextEntry
              autoCapitalize="none"
            />

            <TextInput
              label="Confirm Password"
              value={confirmPassword}
              onChangeText={setConfirmPassword}
              mode="outlined"
              style={styles.input}
              secureTextEntry
              autoCapitalize="none"
            />

            <Button
              mode="contained"
              onPress={handleRegister}
              loading={isLoading}
              disabled={isLoading}
              style={styles.button}
              contentStyle={styles.buttonContent}
            >
              Register
            </Button>

            <Button
              mode="text"
              onPress={() => navigation.navigate('Login')}
              style={styles.linkButton}
            >
              Already have an account? Sign in
            </Button>
          </Card.Content>
        </Card>

        <View style={styles.features}>
          <Text style={styles.featureText}>✨ Offline Support</Text>
          <Text style={styles.featureText}>📱 Push Notifications</Text>
          <Text style={styles.featureText}>🔍 Smart Search</Text>
          <Text style={styles.featureText}>📸 Photo Upload</Text>
        </View>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  scrollContainer: {
    flexGrow: 1,
    justifyContent: 'center',
    padding: 20,
  },
  logoContainer: {
    alignItems: 'center',
    marginBottom: 40,
  },
  logo: {
    fontSize: 80,
    marginBottom: 10,
  },
  title: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#2196F3',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: 16,
    color: '#666',
    textAlign: 'center',
  },
  card: {
    marginBottom: 30,
    elevation: 4,
  },
  cardTitle: {
    textAlign: 'center',
    marginBottom: 20,
    color: '#333',
  },
  input: {
    marginBottom: 15,
  },
  button: {
    marginTop: 10,
    marginBottom: 15,
    borderRadius: 8,
  },
  buttonContent: {
    paddingVertical: 8,
  },
  linkButton: {
    marginTop: 10,
  },
  features: {
    alignItems: 'center',
  },
  featureText: {
    fontSize: 14,
    color: '#666',
    marginBottom: 5,
  },
});
```

#### c. Create PostItemScreen
Create `mobile-app/src/screens/PostItemScreen.tsx`:

```typescript
import React, { useState } from 'react';
import {
  View,
  StyleSheet,
  ScrollView,
  Alert,
  Image,
} from 'react-native';
import {
  Card,
  Title,
  TextInput,
  Button,
  Text,
  RadioButton,
  TouchableRipple,
} from 'react-native-paper';
import { useData } from '../context/DataContext';
import { useNavigation } from '@react-navigation/native';

export default function PostItemScreen() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [status, setStatus] = useState<'found' | 'lost'>('found');
  const [location, setLocation] = useState('');
  const [category, setCategory] = useState('');
  const [image, setImage] = useState<string | null>(null);
  
  const { categories, addItem } = useData();
  const navigation = useNavigation();

  const handlePostItem = async () => {
    if (!title || !description || !location || !category) {
      Alert.alert('Error', 'Please fill in all required fields');
      return;
    }

    try {
      const newItem = {
        title,
        description,
        status,
        location,
        category_id: parseInt(category),
        image_path: image,
      };

      await addItem(newItem);
      Alert.alert('Success', 'Item posted successfully!', [
        { text: 'OK', onPress: () => navigation.navigate('Home') }
      ]);
    } catch (error) {
      Alert.alert('Error', 'Failed to post item. Please try again.');
    }
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Post New Item</Title>
          
          <TextInput
            label="Item Title *"
            value={title}
            onChangeText={setTitle}
            mode="outlined"
            style={styles.input}
          />
          
          <TextInput
            label="Description *"
            value={description}
            onChangeText={setDescription}
            mode="outlined"
            style={styles.input}
            multiline
            numberOfLines={4}
          />
          
          <View style={styles.radioContainer}>
            <Text style={styles.radioLabel}>Item Status *</Text>
            <View style={styles.radioButtonRow}>
              <TouchableRipple onPress={() => setStatus('found')}>
                <View style={styles.radioButtonContainer}>
                  <RadioButton
                    value="found"
                    status={status === 'found' ? 'checked' : 'unchecked'}
                    onPress={() => setStatus('found')}
                  />
                  <Text>Found</Text>
                </View>
              </TouchableRipple>
              
              <TouchableRipple onPress={() => setStatus('lost')}>
                <View style={styles.radioButtonContainer}>
                  <RadioButton
                    value="lost"
                    status={status === 'lost' ? 'checked' : 'unchecked'}
                    onPress={() => setStatus('lost')}
                  />
                  <Text>Lost</Text>
                </View>
              </TouchableRipple>
            </View>
          </View>
          
          <TextInput
            label="Location *"
            value={location}
            onChangeText={setLocation}
            mode="outlined"
            style={styles.input}
          />
          
          <TextInput
            label="Category *"
            value={category}
            onChangeText={setCategory}
            mode="outlined"
            style={styles.input}
            placeholder="Enter category ID"
            keyboardType="numeric"
          />
          
          {image && (
            <Image source={{ uri: image }} style={styles.imagePreview} />
          )}
          
          <Button
            mode="contained"
            onPress={handlePostItem}
            style={styles.button}
          >
            Post Item
          </Button>
          
          <Button
            mode="outlined"
            onPress={() => navigation.goBack()}
            style={styles.cancelButton}
          >
            Cancel
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f5f5f5',
  },
  card: {
    margin: 16,
    elevation: 2,
  },
  title: {
    textAlign: 'center',
    marginBottom: 20,
  },
  input: {
    marginBottom: 15,
  },
  radioContainer: {
    marginBottom: 15,
  },
  radioLabel: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  radioButtonRow: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  radioButtonContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginRight: 20,
  },
  imagePreview: {
    width: '100%',
    height: 200,
    resizeMode: 'cover',
    marginBottom: 15,
    borderRadius: 8,
  },
  button: {
    marginTop: 10,
    marginBottom: 10,
  },
  cancelButton: {
    borderColor: '#2196F3',
  },
});
```

### 2. Update App Navigation
Update `mobile-app/App.tsx` to include the new screens:

```typescript
// Add these imports at the top
import ItemDetailScreen from './src/screens/ItemDetailScreen';
import RegisterScreen from './src/screens/RegisterScreen';
import PostItemScreen from './src/screens/PostItemScreen';

// Update the Tab.Navigator component
function TabNavigator() {
  return (
    <Tab.Navigator
      screenOptions={({ route }) => ({
        tabBarIcon: ({ focused, color, size }) => {
          let iconName;
          if (route.name === 'Home') {
            iconName = 'home';
          } else if (route.name === 'Post') {
            iconName = 'add-circle';
          } else if (route.name === 'Search') {
            iconName = 'search';
          } else if (route.name === 'Matches') {
            iconName = 'notifications';
          } else if (route.name === 'Profile') {
            iconName = 'person';
          }
          return <Icon name={iconName} size={size} color={color} />;
        },
      })}
    >
      <Tab.Screen name="Home" component={HomeScreen} />
      <Tab.Screen name="Post" component={PostItemScreen} />
      <Tab.Screen name="Search" component={SearchScreen} />
      <Tab.Screen name="Matches" component={MatchesScreen} />
      <Tab.Screen name="Profile" component={ProfileScreen} />
    </Tab.Navigator>
  );
}

// Update the AppNavigator component
function AppNavigator() {
  const { isAuthenticated, isLoading } = useAuth();
  const [isOnline, setIsOnline] = useState(true);

  useEffect(() => {
    // Initialize app
    const initializeApp = async () => {
      try {
        await initializeDatabase();
        await syncOfflineData();
        SplashScreen.hide();
      } catch (error) {
        console.error('App initialization failed:', error);
        SplashScreen.hide();
      }
    };

    // Monitor network connectivity
    const unsubscribe = NetInfo.addEventListener(state => {
      setIsOnline(state.isConnected);
    });

    initializeApp();
    return unsubscribe;
  }, []);

  if (isLoading) {
    return null; // Splash screen will show
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false }}>
        {!isAuthenticated ? (
          <>
            <Stack.Screen name="Login" component={LoginScreen} />
            <Stack.Screen name="Register" component={RegisterScreen} />
          </>
        ) : (
          <>
            <Stack.Screen name="Main" component={TabNavigator} />
            <Stack.Screen name="ItemDetail" component={ItemDetailScreen} />
            <Stack.Screen name="Offline" component={OfflineScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
```

### 3. Update Build Configuration
Update `mobile-app/package.json` to ensure all dependencies are properly listed:

```json
{
  "dependencies": {
    // ... existing dependencies ...
    "react-native-vector-icons": "^10.0.2"
  },
  "devDependencies": {
    // ... existing devDependencies ...
    "@types/react-native-vector-icons": "^6.4.14"
  }
}
```

### 4. Create Missing Build Scripts
Create `mobile-app/build_apk.py`:

```python
#!/usr/bin/env python3
"""
APK Build Script for Found It Mobile App
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

def build_apk():
    """Build the Android APK"""
    print("🚀 Building Android APK...")
    
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
    
    # Clean previous builds
    print("🧹 Cleaning previous builds...")
    if not run_command("cd android && ./gradlew clean"):
        print("❌ Failed to clean previous builds")
        return False
    
    # Build the APK
    print("🔨 Building release APK...")
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
    print("🚀 Found It Mobile App APK Build Script")
    print("=" * 50)
    
    # Build APK
    if not build_apk():
        print("\n❌ Failed to build APK.")
        return 1
    
    print("\n🎉 Success! Your APK has been built and placed in static/downloads/FOUND IT.apk")
    print("\nNext steps:")
    print("1. Deploy your Flask app to Render")
    print("2. The APK will be available at: https://found-it-app.onrender.com/static/downloads/FOUND IT.apk")
    print("3. Users can download and install the APK on their Android devices")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
```

### 5. Update Setup Script
Update `mobile-app/setup.sh` to ensure all dependencies are installed:

```bash
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

# Link vector icons
echo "🔗 Linking vector icons..."
npx react-native link react-native-vector-icons

echo "✅ Setup complete!"
echo ""
echo "📱 Next steps:"
echo "1. Update API_BASE_URL in src/services/apiService.ts"
echo "2. Run 'npm start' to start Metro bundler"
echo "3. Run 'npm run android' or 'npm run ios' to launch the app"
echo ""
echo "🔗 For more information, see README.md"
```

## Benefits of These Fixes
1. Complete mobile app with all necessary screens
2. Proper navigation between screens
3. Working registration and login flow
4. Item posting functionality
5. Item detail view with status display
6. Proper build scripts for APK generation
7. Improved user experience

## Testing
After implementing these changes:
1. Test that all screens render correctly
2. Verify navigation between screens works
3. Test registration and login functionality
4. Test item posting and viewing
5. Verify APK build process works
6. Test offline functionality