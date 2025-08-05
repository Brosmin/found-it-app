#!/usr/bin/env python3
"""
Database Backup and Restore Utility for Found-It App
This script helps maintain data persistence across Render deployments
"""

import os
import sqlite3
import shutil
from datetime import datetime
import json

def backup_database(source_path, backup_dir='backups'):
    """Backup the current database"""
    if not os.path.exists(source_path):
        print(f"Database not found at {source_path}")
        return False
    
    # Create backup directory
    os.makedirs(backup_dir, exist_ok=True)
    
    # Create timestamped backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(backup_dir, f"database_backup_{timestamp}.db")
    
    try:
        shutil.copy2(source_path, backup_path)
        print(f"✅ Database backed up to: {backup_path}")
        
        # Also create a metadata file
        metadata = {
            'backup_time': timestamp,
            'source_path': source_path,
            'backup_path': backup_path,
            'file_size': os.path.getsize(backup_path)
        }
        
        metadata_path = backup_path.replace('.db', '_metadata.json')
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        return True
    except Exception as e:
        print(f"❌ Backup failed: {e}")
        return False

def restore_database(backup_path, target_path):
    """Restore database from backup"""
    if not os.path.exists(backup_path):
        print(f"Backup not found at {backup_path}")
        return False
    
    try:
        # Create target directory if it doesn't exist
        os.makedirs(os.path.dirname(target_path), exist_ok=True)
        
        shutil.copy2(backup_path, target_path)
        print(f"✅ Database restored from: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Restore failed: {e}")
        return False

def list_backups(backup_dir='backups'):
    """List available backups"""
    if not os.path.exists(backup_dir):
        print("No backups directory found")
        return []
    
    backups = []
    for file in os.listdir(backup_dir):
        if file.endswith('.db'):
            backup_path = os.path.join(backup_dir, file)
            metadata_path = backup_path.replace('.db', '_metadata.json')
            
            backup_info = {
                'file': file,
                'path': backup_path,
                'size': os.path.getsize(backup_path),
                'modified': datetime.fromtimestamp(os.path.getmtime(backup_path))
            }
            
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        backup_info['metadata'] = json.load(f)
                except:
                    pass
            
            backups.append(backup_info)
    
    return sorted(backups, key=lambda x: x['modified'], reverse=True)

def main():
    """Main function for command line usage"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python database_backup.py backup <database_path>")
        print("  python database_backup.py restore <backup_path> <target_path>")
        print("  python database_backup.py list")
        return
    
    command = sys.argv[1]
    
    if command == 'backup':
        if len(sys.argv) < 3:
            print("Please provide database path")
            return
        database_path = sys.argv[2]
        backup_database(database_path)
    
    elif command == 'restore':
        if len(sys.argv) < 4:
            print("Please provide backup path and target path")
            return
        backup_path = sys.argv[2]
        target_path = sys.argv[3]
        restore_database(backup_path, target_path)
    
    elif command == 'list':
        backups = list_backups()
        if not backups:
            print("No backups found")
            return
        
        print("Available backups:")
        for backup in backups:
            print(f"  {backup['file']} ({backup['size']} bytes, {backup['modified']})")
    
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main() 