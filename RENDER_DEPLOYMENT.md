# 🚀 Render Deployment Guide for FOUND IT

## Quick Setup

### 1. Build Command
```bash
pip install -r requirements-minimal.txt
```

### 2. Start Command
```bash
gunicorn wsgi:app
```

### 3. Environment Variables
- `PORT`: Automatically set by Render
- `SECRET_KEY`: Optional (app will use default if not set)

## Troubleshooting

### If Build Fails with Pillow:
Use the minimal requirements file:
```bash
pip install -r requirements-minimal.txt
```

### If Python Version Issues:
The app works with Python 3.11+ and 3.13+. Render will auto-detect.

### If Database Issues:
The SQLite database will be created automatically on first run.

## Features That Work Without Images:
- ✅ Smart Matching Algorithm
- ✅ Real-time Notifications
- ✅ Advanced Analytics Dashboard
- ✅ RESTful API Endpoints
- ✅ Enhanced Search & Filtering
- ✅ User Management
- ✅ Category Management

## Default Admin Credentials:
- **Username**: `admin`
- **Password**: `admin123`

## URLs:
- **Public Site**: `https://your-app-name.onrender.com/`
- **Admin Panel**: `https://your-app-name.onrender.com/admin/login`

## File Structure:
```
found-it-app/
├── app.py                 # Main application
├── wsgi.py               # WSGI entry point
├── requirements-minimal.txt  # Dependencies (no Pillow)
├── runtime.txt           # Python version
├── Procfile             # Process definition
└── static/              # Static files
    └── uploads/         # Upload directory
```

## Deployment Status:
- ✅ Core functionality works without image processing
- ✅ Smart matching algorithm functional
- ✅ Analytics dashboard operational
- ✅ API endpoints available
- ✅ Admin panel accessible

## For Production:
1. Change default admin password
2. Set environment variables for security
3. Consider using PostgreSQL for production database
4. Add SSL certificate (automatic with Render)

---
**Computer Engineering Final Year Project - Smart Lost and Found System** 