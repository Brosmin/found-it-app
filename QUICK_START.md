# Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Step 1: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Run the Application
```bash
python app.py
```

### Step 3: Access the System
- **Public Site**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin/login
- **Default Admin**: username=`admin`, password=`admin123`

## 📋 What You Can Do

### Public Site Features
- ✅ Browse found items
- ✅ Filter items by category
- ✅ Post new found items (subject to approval)
- ✅ View "About Us" page
- ✅ Send contact messages

### Admin Panel Features
- ✅ Dashboard with statistics
- ✅ Manage categories (add, edit, delete)
- ✅ Manage items (add, edit, delete, approve)
- ✅ Manage users (add, edit, delete)
- ✅ View and respond to messages
- ✅ Update system settings

## 🔧 Quick Setup

### Add Sample Data
1. Login to admin panel
2. Go to Categories → Add Category
3. Add categories like: Electronics, Books, Clothing, etc.
4. Go to Items → Add Item
5. Add some sample items with images

### Customize Site
1. Go to Settings in admin panel
2. Update site name, contact info, and "About Us" content
3. Save changes

## 🧪 Test the System
```bash
python test_system.py
```

## 📁 Project Structure
```
lost-and-found-system/
├── app.py                 # Main application
├── requirements.txt       # Dependencies
├── README.md             # Full documentation
├── QUICK_START.md        # This file
├── test_system.py        # Test script
├── static/
│   ├── css/style.css     # Custom styles
│   └── uploads/          # Item images
└── templates/
    ├── public/           # Public site templates
    └── admin/            # Admin panel templates
```

## 🆘 Troubleshooting

### Port Already in Use
```bash
# Change port in app.py line 461
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database Issues
```bash
# Delete and recreate database
rm lost_and_found.db
python app.py
```

### Missing Dependencies
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## 🎯 Next Steps
1. Change default admin password
2. Add your own categories and items
3. Customize the site content
4. Deploy to production (optional)

## 📞 Support
- Check the full README.md for detailed documentation
- Review the code comments for implementation details
- Test with the provided test script

---

**Happy coding! 🎉** 