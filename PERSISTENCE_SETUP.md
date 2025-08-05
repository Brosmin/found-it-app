# Database Persistence Setup for Found-It App

## Problem
Render uses ephemeral storage, which means your SQLite database gets wiped on each deployment, causing users and items to be lost.

## Solution
This setup implements persistent storage using Render's disk feature and environment variables.

## Files Added/Modified

### 1. `app.py` - Database Configuration
- Added persistent database path configuration
- Uses environment variable `DATABASE_PATH` or defaults to `/tmp/persistent_database.db`
- Ensures database directory exists

### 2. `render.yaml` - Render Configuration
- Configures persistent disk storage (1GB)
- Sets `DATABASE_PATH` environment variable
- Mounts persistent storage at `/opt/render/project/src`

### 3. `deploy.sh` - Deployment Script
- Creates persistent storage directory
- Sets database path to persistent location
- Handles database initialization
- Starts the application with proper configuration

### 4. `Procfile` - Updated
- Now uses `deploy.sh` instead of direct gunicorn
- Ensures database persistence on deployment

### 5. `migrate_db.py` - Migration Script
- Handles database schema updates
- Preserves existing data during migrations
- Creates backups before changes

## How It Works

1. **Persistent Storage**: Render allocates 1GB of persistent disk space
2. **Database Location**: Database is stored at `/opt/render/project/src/persistent_data/found_it.db`
3. **Environment Variable**: `DATABASE_PATH` points to the persistent location
4. **Deployment Script**: `deploy.sh` ensures proper setup on each deployment

## Deployment Steps

1. **Push to GitHub**: All changes are committed and pushed
2. **Render Auto-Deploy**: Render detects changes and starts deployment
3. **Persistent Storage**: Database survives deployment
4. **Data Preservation**: Users and items remain intact

## Benefits

✅ **Data Persistence**: Users and items survive deployments
✅ **Automatic Setup**: No manual intervention needed
✅ **Backup System**: Migration script creates backups
✅ **Scalable**: Can handle growing data needs

## Monitoring

- Check Render logs for deployment status
- Database location: `/opt/render/project/src/persistent_data/found_it.db`
- Backup location: Same directory with `.backup` extension

## Troubleshooting

If data is still being lost:
1. Check Render logs for deployment errors
2. Verify `DATABASE_PATH` environment variable
3. Ensure persistent disk is properly mounted
4. Run migration script if needed: `python migrate_db.py`

## Next Steps

After deployment:
1. Test user registration
2. Test item posting
3. Verify data persists across deployments
4. Monitor Render dashboard for any issues

Your app will now maintain all user registrations and posted items across deployments! 🚀 