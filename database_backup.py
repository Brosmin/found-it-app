#!/usr/bin/env python3
"""
Database Backup and Recovery System for Found-It App
Handles database backup, verification, and recovery operations.
"""

import os
import sqlite3
import shutil
from datetime import datetime
import sys
from pathlib import Path

# Database configuration
DATABASE_PATH = os.environ.get('DATABASE_PATH', '/opt/render/project/src/persistent_data/found_it.db')
BACKUP_DIR = os.path.dirname(DATABASE_PATH)

def create_backup():
    """Create a timestamped backup of the database."""
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database not found at {DATABASE_PATH}")
        return False
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = f"{DATABASE_PATH}.backup.{timestamp}"
    
    try:
        shutil.copy2(DATABASE_PATH, backup_path)
        print(f"✅ Backup created: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def verify_database():
    """Verify database integrity and structure."""
    if not os.path.exists(DATABASE_PATH):
        print(f"❌ Database not found at {DATABASE_PATH}")
        return False
    
    try:
        # Test SQLite connection
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['user', 'category', 'item', 'item_match', 'notification', 'message', 'system_info', 'analytics']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        
        # Check table structure
        for table in required_tables:
            cursor.execute(f"PRAGMA table_info({table});")
            columns = cursor.fetchall()
            print(f"✅ Table '{table}' has {len(columns)} columns")
        
        # Count records
        for table in required_tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table};")
            count = cursor.fetchone()[0]
            print(f"📊 Table '{table}': {count} records")
        
        conn.close()
        print("✅ Database verification completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False

def restore_backup(backup_path):
    """Restore database from backup."""
    if not os.path.exists(backup_path):
        print(f"❌ Backup not found: {backup_path}")
        return False
    
    try:
        # Create backup of current database if it exists
        if os.path.exists(DATABASE_PATH):
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            current_backup = f"{DATABASE_PATH}.before_restore.{timestamp}"
            shutil.copy2(DATABASE_PATH, current_backup)
            print(f"📊 Current database backed up to: {current_backup}")
        
        # Restore from backup
        shutil.copy2(backup_path, DATABASE_PATH)
        print(f"✅ Database restored from: {backup_path}")
        return True
        
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def list_backups():
    """List all available backups."""
    backup_files = []
    for file in os.listdir(BACKUP_DIR):
        if file.startswith('found_it.db.backup.'):
            backup_files.append(file)
    
    if not backup_files:
        print("📊 No backups found")
        return []
    
    print("📊 Available backups:")
    for backup in sorted(backup_files, reverse=True):
        backup_path = os.path.join(BACKUP_DIR, backup)
        size = os.path.getsize(backup_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(backup_path))
        print(f"  {backup} ({size} bytes, {mtime.strftime('%Y-%m-%d %H:%M:%S')})")
    
    return backup_files

def cleanup_old_backups(keep_count=5):
    """Remove old backups, keeping only the most recent ones."""
    backup_files = []
    for file in os.listdir(BACKUP_DIR):
        if file.startswith('found_it.db.backup.'):
            backup_path = os.path.join(BACKUP_DIR, file)
            backup_files.append((backup_path, os.path.getmtime(backup_path)))
    
    if len(backup_files) <= keep_count:
        print(f"📊 No cleanup needed. {len(backup_files)} backups (keeping {keep_count})")
        return
    
    # Sort by modification time (oldest first)
    backup_files.sort(key=lambda x: x[1])
    
    # Remove oldest backups
    to_remove = backup_files[:-keep_count]
    for backup_path, mtime in to_remove:
        try:
            os.remove(backup_path)
            print(f"🗑️ Removed old backup: {os.path.basename(backup_path)}")
        except Exception as e:
            print(f"❌ Failed to remove {backup_path}: {e}")

def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python database_backup.py [backup|verify|restore|list|cleanup]")
        print("Commands:")
        print("  backup   - Create a new backup")
        print("  verify   - Verify database integrity")
        print("  restore  - Restore from backup (requires backup filename)")
        print("  list     - List available backups")
        print("  cleanup  - Remove old backups (keeps 5 most recent)")
        return
    
    command = sys.argv[1]
    
    if command == 'backup':
        create_backup()
    elif command == 'verify':
        verify_database()
    elif command == 'restore':
        if len(sys.argv) < 3:
            print("❌ Please specify backup filename")
            return
        backup_filename = sys.argv[2]
        backup_path = os.path.join(BACKUP_DIR, backup_filename)
        restore_backup(backup_path)
    elif command == 'list':
        list_backups()
    elif command == 'cleanup':
        cleanup_old_backups()
    else:
        print(f"❌ Unknown command: {command}")

if __name__ == '__main__':
    main() 