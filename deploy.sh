#!/bin/bash

# Deployment script for Found-It App with database persistence

echo "🚀 Starting deployment with database persistence..."

# Create persistent storage directory
mkdir -p /opt/render/project/src/persistent_data

# Set database path to persistent location
export DATABASE_PATH="/opt/render/project/src/persistent_data/found_it.db"

# Create database directory if it doesn't exist
mkdir -p $(dirname $DATABASE_PATH)

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
fi

# Start the application
echo "🌐 Starting Found-It App..."
gunicorn app:app --bind 0.0.0.0:$PORT --workers 2 --timeout 120 