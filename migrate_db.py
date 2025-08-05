#!/usr/bin/env python3
"""
Database Migration Script for Found-It App
Handles schema updates and data preservation
"""

import os
import sqlite3
from app import app, db

def migrate_database():
    """Migrate database schema and preserve data"""
    with app.app_context():
        try:
            # Get current database path
            db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
            
            # Check if database exists
            if os.path.exists(db_path):
                print(f"📊 Found existing database at {db_path}")
                
                # Backup existing data
                backup_path = db_path + '.backup'
                import shutil
                shutil.copy2(db_path, backup_path)
                print(f"💾 Created backup at {backup_path}")
                
                # Get existing data
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Store existing data
                existing_data = {}
                
                # Get users
                try:
                    cursor.execute("SELECT * FROM user")
                    existing_data['users'] = cursor.fetchall()
                    print(f"👥 Found {len(existing_data['users'])} users")
                except:
                    print("⚠️  No users table found")
                
                # Get items
                try:
                    cursor.execute("SELECT * FROM item")
                    existing_data['items'] = cursor.fetchall()
                    print(f"📦 Found {len(existing_data['items'])} items")
                except:
                    print("⚠️  No items table found")
                
                # Get categories
                try:
                    cursor.execute("SELECT * FROM category")
                    existing_data['categories'] = cursor.fetchall()
                    print(f"📂 Found {len(existing_data['categories'])} categories")
                except:
                    print("⚠️  No categories table found")
                
                conn.close()
                
                # Drop and recreate tables
                db.drop_all()
                db.create_all()
                print("🔄 Recreated database schema")
                
                # Restore data with new schema
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Restore users
                if 'users' in existing_data:
                    for user_data in existing_data['users']:
                        # Adapt to new schema if needed
                        cursor.execute("""
                            INSERT INTO user (username, email, password_hash, role, created_at)
                            VALUES (?, ?, ?, ?, ?)
                        """, user_data[:5])  # Adjust based on your schema
                
                # Restore categories
                if 'categories' in existing_data:
                    for cat_data in existing_data['categories']:
                        cursor.execute("""
                            INSERT INTO category (name, description, icon, color)
                            VALUES (?, ?, ?, ?)
                        """, cat_data[:4])  # Adjust based on your schema
                
                # Restore items
                if 'items' in existing_data:
                    for item_data in existing_data['items']:
                        cursor.execute("""
                            INSERT INTO item (title, description, category_id, status, location, 
                                           contact_info, image_path, user_id, created_at, updated_at,
                                           keywords, color, brand, model, size, material, condition)
                            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        """, item_data[:17])  # Adjust based on your schema
                
                conn.commit()
                conn.close()
                print("✅ Data migration completed successfully!")
                
            else:
                # Create new database
                db.create_all()
                print("📊 Created new database with current schema")
                
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
        
        return True

if __name__ == "__main__":
    print("🔄 Starting database migration...")
    success = migrate_database()
    if success:
        print("✅ Migration completed successfully!")
    else:
        print("❌ Migration failed!") 