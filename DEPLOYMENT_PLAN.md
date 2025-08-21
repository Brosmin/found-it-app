# Deployment Plan for FOUND IT App

## Current Deployment Process
The app currently deploys automatically when the server starts, which is not ideal. We want to modify this to only deploy on GitHub push events.

## Proposed Solution
Create a GitHub Actions workflow that will trigger deployments to Render only when code is pushed to the main branch.

## Implementation Steps

### 1. Create GitHub Actions Workflow
Create a workflow file at `.github/workflows/deploy.yml` with the following content:

```yaml
name: Deploy to Render

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Deploy to Render
        uses: johnbeynon/render-deploy-action@v0.0.8
        with:
          service-id: ${{ secrets.RENDER_SERVICE_ID }}
          api-key: ${{ secrets.RENDER_API_KEY }}
```

### 2. Configure Render for Manual Deployments
Modify the `render.yaml` file to ensure it's configured for manual deployments:

```yaml
services:
  - type: web
    name: found-it-app
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: bash deploy.sh
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.7
      - key: DATABASE_PATH
        value: /opt/render/project/src/data/found_it.db
    disk:
      name: persistent-storage
      mountPath: /opt/render/project/src
      sizeGB: 1
    autoDeploy: false  # Disable auto-deploy
```

### 3. Update deploy.sh Script
Modify the `deploy.sh` script to remove any automatic deployment triggers and only handle database initialization:

```bash
#!/bin/bash

# Deployment script for Found-It App with database persistence

echo "🚀 Starting deployment with database persistence..."

# Create persistent storage directory
mkdir -p /opt/render/project/src/data

# Set database path to persistent location
export DATABASE_PATH="/opt/render/project/src/data/found_it.db"

# Create database directory if it doesn't exist
mkdir -p $(dirname $DATABASE_PATH)

# Debug: Show current database path and check if it exists
echo "📊 Database path: $DATABASE_PATH"
echo "📊 Database directory: $(dirname $DATABASE_PATH)"
echo "📊 Database exists: $(if [ -f "$DATABASE_PATH" ]; then echo "YES"; else echo "NO"; fi)"

# Create backup if database exists
if [ -f "$DATABASE_PATH" ]; then
    echo "📊 Creating backup of existing database..."
    cp "$DATABASE_PATH" "$DATABASE_PATH.backup.$(date +%Y%m%d_%H%M%S)"
    echo "✅ Backup created successfully"
fi

# Check if database exists, if not create it
if [ ! -f "$DATABASE_PATH" ]; then
    echo "📊 Creating new database at $DATABASE_PATH"
    python -c "
import os
from app import app, db
with app.app_context():
    db.create_all()
    print('Database tables created successfully!')
"
else
    echo "📊 Using existing database at $DATABASE_PATH"
    # Verify database integrity
    python -c "
import os
from app import app, db
with app.app_context():
    try:
        # Test database connection
        db.session.execute('SELECT 1')
        print('✅ Database connection verified!')
        
        # Check if tables exist
        from app import User, Category, Item
        user_count = User.query.count()
        category_count = Category.query.count()
        item_count = Item.query.count()
        print(f'📊 Current data: {user_count} users, {category_count} categories, {item_count} items')
        
    except Exception as e:
        print(f'❌ Database verification failed: {e}')
        # Recreate database if corrupted
        db.create_all()
        print('✅ Database recreated successfully!')
"
fi

# Start the application
echo "🌐 Starting Found-It App..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120
```

### 4. Update Render Dashboard Settings
In the Render dashboard:
1. Go to your service settings
2. Disable "Auto Deploy" in the "Build & Deploy" section
3. Set the deployment trigger to manual or GitHub Actions only

### 5. Set GitHub Secrets
In your GitHub repository:
1. Go to Settings > Secrets and variables > Actions
2. Add the following secrets:
   - `RENDER_SERVICE_ID`: Your Render service ID
   - `RENDER_API_KEY`: Your Render API key

## Benefits of This Approach
1. Deployments only happen when code is pushed to the main branch
2. Better control over when deployments occur
3. Easier to rollback if needed
4. More secure as deployment keys are stored as secrets

## Testing
After implementing these changes:
1. Make a small change to the code
2. Commit and push to the main branch
3. Verify that the GitHub Action triggers
4. Check that the deployment completes successfully on Render