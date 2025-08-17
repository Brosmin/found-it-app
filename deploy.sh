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