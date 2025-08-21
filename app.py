import os
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from functools import wraps
import re
from difflib import SequenceMatcher
import json
from collections import Counter
import math
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Enhanced database configuration for better persistence
# Use environment variable for database path or default to persistent location
DATABASE_PATH = os.environ.get('DATABASE_PATH', '/opt/render/project/src/data/found_it.db')

# Fallback paths for different environments
if not os.path.exists(os.path.dirname(DATABASE_PATH)):
    # Try alternative paths
    alternative_paths = [
        '/opt/render/project/src/data/found_it.db',  # Render persistent storage
        '/tmp/found_it.db',  # Local development fallback
        './instance/found_it.db',  # Flask default instance folder
        './found_it.db'  # Current directory fallback
    ]
    
    for alt_path in alternative_paths:
        if os.path.exists(os.path.dirname(alt_path)) or os.path.dirname(alt_path) == '.':
            DATABASE_PATH = alt_path
            break

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Ensure the database directory exists with better error handling
try:
    db_dir = os.path.dirname(DATABASE_PATH)
    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir, exist_ok=True)
        print(f"✅ Created database directory: {db_dir}")
except Exception as e:
    print(f"⚠️ Warning: Could not create database directory: {e}")
    # Fallback to current directory
    DATABASE_PATH = './found_it.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
    print(f"🔄 Fallback database path: {DATABASE_PATH}")

print(f"🗄️ Database path: {DATABASE_PATH}")

# Upload folder configuration
app.config['UPLOAD_FOLDER'] = 'static/uploads'
# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Enhanced Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='staff')  # admin or staff
    phone = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    icon = db.Column(db.String(50))
    color = db.Column(db.String(7))  # Hex color code
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    status = db.Column(db.String(20), default='found')  # found, lost, claimed, archived
    location = db.Column(db.String(200))
    contact_info = db.Column(db.String(200))
    image_path = db.Column(db.String(500))
    is_approved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    category = db.relationship('Category', backref='items')
    
    # Enhanced fields for smart matching
    keywords = db.Column(db.Text)  # Extracted keywords for matching
    color = db.Column(db.String(50))  # Item color
    brand = db.Column(db.String(100))  # Brand name
    model = db.Column(db.String(100))  # Model number
    size = db.Column(db.String(50))  # Size information
    material = db.Column(db.String(100))  # Material type
    condition = db.Column(db.String(50))  # New, used, damaged, etc.
    
    # Claiming system fields
    claimed_at = db.Column(db.DateTime)  # When item was claimed
    claimed_by = db.Column(db.String(200))  # Name of person claiming
    claimer_email = db.Column(db.String(120))  # Email of person claiming
    claimer_phone = db.Column(db.String(20))  # Phone of person claiming
    claim_proof = db.Column(db.Text)  # Description of proof provided
    claim_notes = db.Column(db.Text)  # Admin notes about the claim
    
    # Matching fields
    matched_items = db.relationship('ItemMatch', foreign_keys='ItemMatch.item1_id', backref='item1')
    matched_with = db.relationship('ItemMatch', foreign_keys='ItemMatch.item2_id', backref='item2')

class ItemMatch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item1_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item2_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    similarity_score = db.Column(db.Float, nullable=False)
    match_type = db.Column(db.String(50))  # exact, similar, potential
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_notified = db.Column(db.Boolean, default=False)

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # match, system, alert
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', backref='notifications')

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(200))
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_read = db.Column(db.Boolean, default=False)

class SystemInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    site_name = db.Column(db.String(200), default='FOUND IT')
    about_content = db.Column(db.Text)
    contact_email = db.Column(db.String(120))
    contact_phone = db.Column(db.String(20))
    contact_address = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    total_items = db.Column(db.Integer, default=0)
    found_items = db.Column(db.Integer, default=0)
    lost_items = db.Column(db.Integer, default=0)
    claimed_items = db.Column(db.Integer, default=0)
    matches_found = db.Column(db.Integer, default=0)
    new_users = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Claim(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    claimer_name = db.Column(db.String(200), nullable=False)
    claimer_email = db.Column(db.String(120), nullable=False)
    claimer_phone = db.Column(db.String(20))
    claim_proof = db.Column(db.Text, nullable=False)
    claim_reason = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, approved, rejected
    admin_notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime)
    processed_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    # Relationships
    item = db.relationship('Item', backref='claims')
    admin_user = db.relationship('User', backref='processed_claims')

# Smart Matching Algorithm
class SmartMatcher:
    def __init__(self):
        self.keywords_weight = 0.4
        self.category_weight = 0.2
        self.location_weight = 0.15
        self.description_weight = 0.25
    
    def extract_keywords(self, text):
        """Extract important keywords from text"""
        if not text:
            return []
        
        # Remove common words and extract meaningful terms
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        
        # Clean text and extract words
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter out common words and short words
        keywords = [word for word in words if word not in common_words and len(word) > 2]
        
        return keywords
    
    def calculate_similarity(self, item1, item2):
        """Calculate similarity score between two items"""
        score = 0.0
        
        # Title similarity
        if item1.title and item2.title:
            title_similarity = SequenceMatcher(None, item1.title.lower(), item2.title.lower()).ratio()
            score += title_similarity * 0.3
        
        # Description similarity
        if item1.description and item2.description:
            desc_similarity = SequenceMatcher(None, item1.description.lower(), item2.description.lower()).ratio()
            score += desc_similarity * 0.2
        
        # Category match
        if item1.category_id == item2.category_id:
            score += 0.2
        
        # Location similarity
        if item1.location and item2.location:
            location_similarity = SequenceMatcher(None, item1.location.lower(), item2.location.lower()).ratio()
            score += location_similarity * 0.1
        
        # Keywords similarity
        keywords1 = self.extract_keywords(item1.title + ' ' + (item1.description or ''))
        keywords2 = self.extract_keywords(item2.title + ' ' + (item2.description or ''))
        
        if keywords1 and keywords2:
            common_keywords = set(keywords1) & set(keywords2)
            total_keywords = set(keywords1) | set(keywords2)
            if total_keywords:
                keyword_similarity = len(common_keywords) / len(total_keywords)
                score += keyword_similarity * 0.2
        
        return min(score, 1.0)
    
    def find_matches(self, item, threshold=0.6):
        """Find potential matches for an item"""
        matches = []
        
        # Get items with opposite status
        opposite_status = 'lost' if item.status == 'found' else 'found'
        potential_matches = Item.query.filter_by(status=opposite_status, is_approved=True).all()
        
        for potential_match in potential_matches:
            if potential_match.id != item.id:
                similarity = self.calculate_similarity(item, potential_match)
                
                if similarity >= threshold:
                    matches.append({
                        'item': potential_match,
                        'similarity': similarity,
                        'match_type': 'exact' if similarity >= 0.8 else 'similar' if similarity >= 0.6 else 'potential'
                    })
        
        # Sort by similarity score
        matches.sort(key=lambda x: x['similarity'], reverse=True)
        return matches

# Initialize smart matcher
smart_matcher = SmartMatcher()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Helper Functions
def backup_database():
    """Create a backup of the database before making changes"""
    try:
        if os.path.exists(DATABASE_PATH):
            backup_path = f"{DATABASE_PATH}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            import shutil
            shutil.copy2(DATABASE_PATH, backup_path)
            print(f"✅ Database backed up to: {backup_path}")
            return backup_path
    except Exception as e:
        print(f"⚠️ Warning: Could not create database backup: {e}")
    return None

def get_system_info():
    try:
        info = SystemInfo.query.first()
        if not info:
            info = SystemInfo(
                site_name='FOUND IT',
                about_content='Welcome to FOUND IT - Your Smart Lost and Found System!',
                contact_email='admin@foundit.com',
                contact_phone='+234 810 678 1706',
                contact_address='ABU Zaria, Main Campus, Nigeria'
            )
            db.session.add(info)
            db.session.commit()
        return info
    except Exception as e:
        print(f"get_system_info error: {e}")
        # Return a fallback object
        return type('SystemInfo', (), {
            'site_name': 'FOUND IT',
            'about_content': 'Welcome to FOUND IT - Your Smart Lost and Found System!',
            'contact_email': 'admin@foundit.com',
            'contact_phone': '+234 810 678 1706',
            'contact_address': 'ABU Zaria, Main Campus, Nigeria'
        })()

def create_notification(user_id, title, message, notification_type='system'):
    """Create a new notification"""
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        type=notification_type
    )
    db.session.add(notification)
    db.session.commit()
    return notification

def update_analytics():
    """Update daily analytics"""
    today = datetime.now().date()
    analytics = Analytics.query.filter_by(date=today).first()
    
    if not analytics:
        analytics = Analytics(date=today)
        db.session.add(analytics)
    
    # Update counts
    analytics.total_items = Item.query.count()
    analytics.found_items = Item.query.filter_by(status='found').count()
    analytics.lost_items = Item.query.filter_by(status='lost').count()
    analytics.claimed_items = Item.query.filter_by(status='claimed').count()
    analytics.matches_found = ItemMatch.query.count()
    analytics.new_users = User.query.filter(User.created_at >= today).count()
    
    db.session.commit()

def get_analytics_data():
    """Get analytics data for dashboard"""
    # Last 30 days
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=30)
    
    analytics = Analytics.query.filter(
        Analytics.date >= start_date,
        Analytics.date <= end_date
    ).order_by(Analytics.date).all()
    
    return {
        'dates': [a.date.strftime('%Y-%m-%d') for a in analytics],
        'total_items': [a.total_items for a in analytics],
        'found_items': [a.found_items for a in analytics],
        'lost_items': [a.lost_items for a in analytics],
        'matches': [a.matches_found for a in analytics]
    }

# Custom filter for newlines to <br> tags
@app.template_filter('nl2br')
def nl2br_filter(text):
    if text:
        return text.replace('\n', '<br>')
    return text

# Context processor to make system_info available globally
@app.context_processor
def inject_system_info():
    try:
        with app.app_context():
            system_info = get_system_info()
            if system_info:
                return {'system_info': system_info}
            else:
                raise Exception("SystemInfo not found")
    except Exception as e:
        print(f"Context processor error: {e}")
        # Fallback if system_info fails
        fallback_info = type('SystemInfo', (), {
            'site_name': 'FOUND IT',
            'about_content': 'Welcome to FOUND IT - Your Smart Lost and Found System!',
            'contact_email': 'admin@foundit.com',
            'contact_phone': '+234 810 678 1706',
            'contact_address': 'ABU Zaria, Main Campus, Nigeria'
        })()
        return {'system_info': fallback_info}

# Error handlers
@app.errorhandler(500)
def internal_error(error):
    try:
        return render_template('errors/500.html'), 500
    except:
        return """
        <html>
        <head><title>500 Internal Server Error</title></head>
        <body>
        <h1>Internal Server Error</h1>
        <p>The server encountered an internal error and was unable to complete your request.</p>
        <a href="/">Go Home</a>
        </body>
        </html>
        """, 500

@app.errorhandler(404)
def not_found_error(error):
    try:
        return render_template('errors/404.html'), 404
    except:
        return """
        <html>
        <head><title>404 Not Found</title></head>
        <body>
        <h1>Page Not Found</h1>
        <p>The page you're looking for doesn't exist.</p>
        <a href="/">Go Home</a>
        </body>
        </html>
        """, 404

@app.errorhandler(403)
def forbidden_error(error):
    try:
        return render_template('errors/403.html'), 403
    except:
        return """
        <html>
        <head><title>403 Forbidden</title></head>
        <body>
        <h1>Access Denied</h1>
        <p>You don't have permission to access this page.</p>
        <a href="/">Go Home</a>
        </body>
        </html>
        """, 403

# Public Routes
@app.route('/')
def home():
    categories = Category.query.all()
    # Only show active items (found/lost) on public pages
    items = Item.query.filter(
        Item.is_approved == True,
        Item.status.in_(['found', 'lost'])
    ).order_by(Item.created_at.desc()).limit(10).all()
    system_info = get_system_info()
    
    # Update analytics
    update_analytics()
    
    return render_template('public/home.html', items=items, categories=categories, system_info=system_info)

@app.route('/items')
def items():
    # Enhanced search and filtering
    search = request.args.get('search', '')
    category_id = request.args.get('category', '')
    status = request.args.get('status', '')
    sort_by = request.args.get('sort', 'newest')
    
    # Only show active items (found/lost) on public pages
    query = Item.query.filter(
        Item.is_approved == True,
        Item.status.in_(['found', 'lost'])
    )
    
    if search:
        query = query.filter(
            db.or_(
                Item.title.ilike(f'%{search}%'),
                Item.description.ilike(f'%{search}%'),
                Item.location.ilike(f'%{search}%'),
                Item.brand.ilike(f'%{search}%'),
                Item.model.ilike(f'%{search}%')
            )
        )
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    if status and status in ['found', 'lost']:
        query = query.filter_by(status=status)
    
    # Sorting
    if sort_by == 'newest':
        query = query.order_by(Item.created_at.desc())
    elif sort_by == 'oldest':
        query = query.order_by(Item.created_at.asc())
    elif sort_by == 'title':
        query = query.order_by(Item.title.asc())
    
    items = query.all()
    categories = Category.query.all()
    system_info = get_system_info()
    
    return render_template('public/items.html', items=items, categories=categories, 
                         search=search, selected_category=category_id, selected_status=status, 
                         sort_by=sort_by, system_info=system_info)

@app.route('/post_item', methods=['GET', 'POST'])
def post_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        status = request.form.get('status')
        location = request.form.get('location')
        contact_info = request.form.get('contact_info')
        
        # Enhanced fields
        brand = request.form.get('brand', '')
        model = request.form.get('model', '')
        color = request.form.get('color', '')
        size = request.form.get('size', '')
        material = request.form.get('material', '')
        condition = request.form.get('condition', '')
        
        if not all([title, category_id, status]):
            flash('Please fill in all required fields.', 'error')
            return redirect(url_for('post_item'))
        
        # Extract keywords for smart matching
        keywords = smart_matcher.extract_keywords(title + ' ' + (description or ''))
        
        item = Item(
            title=title,
            description=description,
            category_id=category_id,
            status=status,
            location=location,
            contact_info=contact_info,
            brand=brand,
            model=model,
            color=color,
            size=size,
            material=material,
            condition=condition,
            keywords=','.join(keywords),
            is_approved=True  # Items are automatically approved and visible
        )
        
        # Handle image upload (optional - gracefully handle errors)
        try:
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    # Ensure upload directory exists
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    
                    # Validate file type
                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        item.image_path = f'uploads/{filename}'
                    else:
                        flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).', 'warning')
        except Exception as e:
            # Log error but don't fail the entire submission
            print(f"Image upload error: {e}")
            flash('Image upload failed, but item was posted successfully.', 'warning')
        
        db.session.add(item)
        db.session.commit()
        
        # Find potential matches immediately
        matches = smart_matcher.find_matches(item)
        
        # Create matches in database
        for match in matches:
            item_match = ItemMatch(
                item1_id=item.id,
                item2_id=match['item'].id,
                similarity_score=match['similarity'],
                match_type=match['match_type']
            )
            db.session.add(item_match)
        
        db.session.commit()
        
        # Create notifications for matches
        if matches:
            match_count = len(matches)
            flash(f'Item posted successfully! Found {match_count} potential match(es).', 'success')
            
            # Notify admin about matches
            admin_users = User.query.filter_by(role='admin').all()
            for admin in admin_users:
                create_notification(
                    admin.id,
                    f'New Match Found - {item.title}',
                    f'Found {match_count} potential match(es) for "{item.title}". Check the matches section.',
                    'match'
                )
        else:
            flash('Item posted successfully! It will be reviewed by admin.', 'success')
        
        return redirect(url_for('items'))
    
    categories = Category.query.all()
    system_info = get_system_info()
    return render_template('public/post_item.html', categories=categories, system_info=system_info)

@app.route('/about')
def about():
    system_info = get_system_info()
    return render_template('public/about.html', system_info=system_info)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message_text = request.form.get('message')
        
        message = Message(name=name, email=email, subject=subject, message=message_text)
        db.session.add(message)
        db.session.commit()
        flash('Message sent successfully!', 'success')
        return redirect(url_for('contact'))
    
    system_info = get_system_info()
    return render_template('public/contact.html', system_info=system_info)

@app.route('/mobile-app')
def mobile_app():
    system_info = get_system_info()
    return render_template('public/mobile_app.html', system_info=system_info)

# Smart Matching Routes
@app.route('/matches')
def matches():
    """Show all matches found by the system"""
    matches = ItemMatch.query.order_by(ItemMatch.similarity_score.desc()).all()
    return render_template('public/matches.html', matches=matches)

@app.route('/item/<int:id>/matches')
def item_matches(id):
    """Show matches for a specific item"""
    item = Item.query.get_or_404(id)
    matches = ItemMatch.query.filter(
        db.or_(ItemMatch.item1_id == id, ItemMatch.item2_id == id)
    ).order_by(ItemMatch.similarity_score.desc()).all()
    
    return render_template('public/item_matches.html', item=item, matches=matches)

@app.route('/api/matches/<int:item_id>')
def api_item_matches(item_id):
    """API endpoint for getting matches for an item"""
    item = Item.query.get_or_404(item_id)
    matches = smart_matcher.find_matches(item)
    
    return jsonify({
        'item_id': item_id,
        'matches': [
            {
                'id': match['item'].id,
                'title': match['item'].title,
                'description': match['item'].description,
                'similarity': match['similarity'],
                'match_type': match['match_type'],
                'status': match['item'].status,
                'location': match['item'].location
            }
            for match in matches
        ]
    })

@app.route('/api/search')
def api_search():
    """API endpoint for advanced search"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    status = request.args.get('status', '')
    
    items_query = Item.query.filter_by(is_approved=True)
    
    if query:
        items_query = items_query.filter(
            db.or_(
                Item.title.ilike(f'%{query}%'),
                Item.description.ilike(f'%{query}%'),
                Item.brand.ilike(f'%{query}%'),
                Item.model.ilike(f'%{query}%'),
                Item.color.ilike(f'%{query}%')
            )
        )
    
    if category:
        items_query = items_query.filter_by(category_id=category)
    
    if status:
        items_query = items_query.filter_by(status=status)
    
    items = items_query.order_by(Item.created_at.desc()).all()
    
    return jsonify({
        'items': [
            {
                'id': item.id,
                'title': item.title,
                'description': item.description,
                'status': item.status,
                'location': item.location,
                'category': item.category.name,
                'created_at': item.created_at.isoformat()
            }
            for item in items
        ]
    })

@app.route('/api/analytics')
@login_required
def api_analytics():
    """API endpoint for analytics data"""
    if current_user.role != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    
    analytics_data = get_analytics_data()
    
    # Additional statistics
    total_items = Item.query.count()
    found_items = Item.query.filter_by(status='found').count()
    lost_items = Item.query.filter_by(status='lost').count()
    claimed_items = Item.query.filter_by(status='claimed').count()
    total_matches = ItemMatch.query.count()
    total_users = User.query.count()
    
    return jsonify({
        'analytics': analytics_data,
        'summary': {
            'total_items': total_items,
            'found_items': found_items,
            'lost_items': lost_items,
            'claimed_items': claimed_items,
            'total_matches': total_matches,
            'total_users': total_users
        }
    })

# Custom decorator for admin-only access
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if current_user.role != 'admin':
            flash('Access denied. Admin privileges required.', 'error')
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

# Public Authentication Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    system_info = get_system_info()
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if not username or not email or not password:
            flash('All fields are required.', 'error')
            return render_template('auth/register.html', system_info=system_info)
        
        if password != confirm_password:
            flash('Passwords do not match.', 'error')
            return render_template('auth/register.html', system_info=system_info)
        
        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'error')
            return render_template('auth/register.html', system_info=system_info)
        
        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists.', 'error')
            return render_template('auth/register.html', system_info=system_info)
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'error')
            return render_template('auth/register.html', system_info=system_info)
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='staff'  # Default role for new registrations
        )
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('auth/register.html', system_info=system_info)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    system_info = get_system_info()
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            next_page = request.args.get('next')
            if next_page and url_for('static', filename='') not in next_page:
                return redirect(next_page)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('auth/login.html', system_info=system_info)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    # Update analytics
    update_analytics()
    
    # Basic statistics
    total_items = Item.query.count()
    found_items = Item.query.filter_by(status='found').count()
    lost_items = Item.query.filter_by(status='lost').count()
    claimed_items = Item.query.filter_by(status='claimed').count()
    archived_items = Item.query.filter_by(status='archived').count()
    total_categories = Category.query.count()
    total_users = User.query.count()
    total_messages = Message.query.count()
    unread_messages = Message.query.filter_by(is_read=False).count()
    total_matches = ItemMatch.query.count()
    
    # Recent activity
    recent_items = Item.query.order_by(Item.created_at.desc()).limit(5).all()
    recent_matches = ItemMatch.query.order_by(ItemMatch.created_at.desc()).limit(5).all()
    recent_claims = Claim.query.order_by(Claim.created_at.desc()).limit(5).all()
    
    # Analytics data for charts
    analytics_data = get_analytics_data()
    
    # Unread notifications
    unread_notifications = Notification.query.filter_by(is_read=False).count()
    
    # Pending claims
    pending_claims = Claim.query.filter_by(status='pending').count()
    
    return render_template('admin/dashboard.html', 
                         total_items=total_items,
                         found_items=found_items,
                         lost_items=lost_items,
                         claimed_items=claimed_items,
                         archived_items=archived_items,
                         total_categories=total_categories,
                         total_users=total_users,
                         total_messages=total_messages,
                         unread_messages=unread_messages,
                         total_matches=total_matches,
                         unread_notifications=unread_notifications,
                         pending_claims=pending_claims,
                         recent_items=recent_items,
                         recent_matches=recent_matches,
                         recent_claims=recent_claims,
                         analytics_data=analytics_data)

# Category Management
@app.route('/admin/categories')
@login_required
def admin_categories():
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/add', methods=['GET', 'POST'])
@login_required
def add_category():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        flash('Category added successfully!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/add_category.html')

@app.route('/admin/categories/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_category(id):
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        category.name = request.form.get('name')
        category.description = request.form.get('description')
        db.session.commit()
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories'))
    
    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/categories/delete/<int:id>')
@login_required
def delete_category(id):
    category = Category.query.get_or_404(id)
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully!', 'success')
    return redirect(url_for('admin_categories'))

# Item Management
@app.route('/admin/items')
@login_required
def admin_items():
    # Show all items with status filtering
    status_filter = request.args.get('status', '')
    if status_filter:
        items = Item.query.filter_by(status=status_filter).order_by(Item.created_at.desc()).all()
    else:
        items = Item.query.order_by(Item.created_at.desc()).all()
    
    return render_template('admin/items.html', items=items, selected_status=status_filter)

@app.route('/admin/items/add', methods=['GET', 'POST'])
@login_required
def add_item():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        status = request.form.get('status')
        location = request.form.get('location')
        contact_info = request.form.get('contact_info')
        is_approved = 'is_approved' in request.form
        
        item = Item(
            title=title,
            description=description,
            category_id=category_id,
            status=status,
            location=location,
            contact_info=contact_info,
            is_approved=is_approved
        )
        
        # Handle image upload (optional - gracefully handle errors)
        try:
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    # Ensure upload directory exists
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    
                    # Validate file type
                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        item.image_path = f'uploads/{filename}'
                    else:
                        flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).', 'warning')
        except Exception as e:
            # Log error but don't fail the entire submission
            print(f"Image upload error: {e}")
            flash('Image upload failed, but item was added successfully.', 'warning')
        
        db.session.add(item)
        db.session.commit()
        flash('Item added successfully!', 'success')
        return redirect(url_for('admin_items'))
    
    categories = Category.query.all()
    return render_template('admin/add_item.html', categories=categories)

@app.route('/admin/items/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_item(id):
    item = Item.query.get_or_404(id)
    if request.method == 'POST':
        item.title = request.form.get('title')
        item.description = request.form.get('description')
        item.category_id = request.form.get('category_id')
        item.status = request.form.get('status')
        item.location = request.form.get('location')
        item.contact_info = request.form.get('contact_info')
        item.is_approved = 'is_approved' in request.form
        
        # Handle image upload (optional - gracefully handle errors)
        try:
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename:
                    # Ensure upload directory exists
                    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
                    
                    # Validate file type
                    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
                    if '.' in file.filename and file.filename.rsplit('.', 1)[1].lower() in allowed_extensions:
                        filename = secure_filename(file.filename)
                        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                        file.save(file_path)
                        item.image_path = f'uploads/{filename}'
                    else:
                        flash('Invalid file type. Please upload an image (PNG, JPG, JPEG, GIF, WEBP).', 'warning')
        except Exception as e:
            # Log error but don't fail the entire submission
            print(f"Image upload error: {e}")
            flash('Image upload failed, but item was updated successfully.', 'warning')
        
        db.session.commit()
        flash('Item updated successfully!', 'success')
        return redirect(url_for('admin_items'))
    
    categories = Category.query.all()
    return render_template('admin/edit_item.html', item=item, categories=categories)

@app.route('/admin/items/delete/<int:id>')
@login_required
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    flash('Item deleted successfully!', 'success')
    return redirect(url_for('admin_items'))

@app.route('/admin/items/approve/<int:id>')
@login_required
def approve_item(id):
    item = Item.query.get_or_404(id)
    item.is_approved = True
    db.session.commit()
    flash('Item approved successfully!', 'success')
    return redirect(url_for('admin_items'))

@app.route('/admin/items/unapprove/<int:id>')
@login_required
def unapprove_item(id):
    item = Item.query.get_or_404(id)
    item.is_approved = False
    db.session.commit()
    flash('Item unapproved successfully!', 'success')
    return redirect(url_for('admin_items'))

# User Management
@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role=role
        )
        db.session.add(user)
        db.session.commit()
        flash('User added successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/add_user.html')

@app.route('/admin/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.get_or_404(id)
    if request.method == 'POST':
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.role = request.form.get('role')
        
        if request.form.get('password'):
            user.password_hash = generate_password_hash(request.form.get('password'))
        
        db.session.commit()
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/users/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash('Cannot delete your own account!', 'error')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin_users'))

# Message Management
@app.route('/admin/messages')
@login_required
def admin_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return render_template('admin/messages.html', messages=messages)

@app.route('/admin/messages/view/<int:id>')
@login_required
def view_message(id):
    message = Message.query.get_or_404(id)
    message.is_read = True
    db.session.commit()
    return render_template('admin/view_message.html', message=message)

@app.route('/admin/messages/delete/<int:id>')
@login_required
def delete_message(id):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully!', 'success')
    return redirect(url_for('admin_messages'))

# System Settings
@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    if current_user.role != 'admin':
        flash('Access denied. Admin privileges required.', 'error')
        return redirect(url_for('admin_dashboard'))
    
    system_info = get_system_info()
    if request.method == 'POST':
        system_info.site_name = request.form.get('site_name')
        system_info.about_content = request.form.get('about_content')
        system_info.contact_email = request.form.get('contact_email')
        system_info.contact_phone = request.form.get('contact_phone')
        system_info.contact_address = request.form.get('contact_address')
        system_info.updated_at = datetime.utcnow()
        
        db.session.commit()
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', system_info=system_info)

# Match Management
@app.route('/admin/matches')
@login_required
def admin_matches():
    matches = ItemMatch.query.order_by(ItemMatch.similarity_score.desc()).all()
    return render_template('admin/matches.html', matches=matches)

@app.route('/admin/matches/delete/<int:id>')
@login_required
def delete_match(id):
    match = ItemMatch.query.get_or_404(id)
    db.session.delete(match)
    db.session.commit()
    flash('Match deleted successfully!', 'success')
    return redirect(url_for('admin_matches'))

# Notification Management
@app.route('/admin/notifications')
@login_required
def admin_notifications():
    notifications = Notification.query.order_by(Notification.created_at.desc()).all()
    return render_template('admin/notifications.html', notifications=notifications)

@app.route('/admin/notifications/mark_read/<int:id>')
@login_required
def mark_notification_read(id):
    notification = Notification.query.get_or_404(id)
    notification.is_read = True
    db.session.commit()
    flash('Notification marked as read!', 'success')
    return redirect(url_for('admin_notifications'))

@app.route('/admin/notifications/delete/<int:id>')
@login_required
def delete_notification(id):
    notification = Notification.query.get_or_404(id)
    db.session.delete(notification)
    db.session.commit()
    flash('Notification deleted successfully!', 'success')
    return redirect(url_for('admin_notifications'))

# Analytics Dashboard
@app.route('/admin/analytics')
@admin_required
def admin_analytics():
    analytics_data = get_analytics_data()
    
    # Category statistics
    categories = Category.query.all()
    category_stats = []
    for category in categories:
        item_count = Item.query.filter_by(category_id=category.id).count()
        category_stats.append({
            'name': category.name,
            'count': item_count
        })
    
    # Match statistics
    exact_matches = ItemMatch.query.filter_by(match_type='exact').count()
    similar_matches = ItemMatch.query.filter_by(match_type='similar').count()
    potential_matches = ItemMatch.query.filter_by(match_type='potential').count()
    
    return render_template('admin/analytics.html', 
                         analytics_data=analytics_data,
                         category_stats=category_stats,
                         exact_matches=exact_matches,
                         similar_matches=similar_matches,
                         potential_matches=potential_matches)

# Claim Management Routes
@app.route('/mark_found_by_owner/<int:item_id>')
def mark_found_by_owner(item_id):
    """Simple route to mark item as found by owner (archived)"""
    item = Item.query.get_or_404(item_id)
    
    if item.status != 'found':
        flash('This item cannot be marked as found by owner.', 'error')
        return redirect(url_for('items'))
    
    try:
        # Update item status to archived (found by owner)
        item.status = 'archived'
        item.claimed_at = datetime.utcnow()
        item.claimed_by = 'Found by Owner'
        item.claimer_email = 'owner@found.com'
        item.claim_notes = 'Item marked as found by owner'
        
        db.session.commit()
        
        flash('Item has been marked as found by owner and removed from the list.', 'success')
        return redirect(url_for('items'))
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating item: {str(e)}', 'error')
        print(f"Mark found by owner error: {e}")
        return redirect(url_for('items'))

@app.route('/claim_item/<int:item_id>', methods=['GET', 'POST'])
def claim_item(item_id):
    """Public route for users to claim items"""
    item = Item.query.get_or_404(item_id)
    
    # Check if item can be claimed
    if item.status != 'found':
        flash('This item cannot be claimed.', 'error')
        return redirect(url_for('items'))
    
    if request.method == 'POST':
        claimer_name = request.form.get('claimer_name')
        claimer_email = request.form.get('claimer_email')
        claimer_phone = request.form.get('claimer_phone')
        claim_proof = request.form.get('claim_proof')
        claim_reason = request.form.get('claim_reason')
        
        if not all([claimer_name, claimer_email, claim_proof]):
            flash('Please fill in all required fields.', 'error')
            return render_template('public/claim_item.html', item=item)
        
        try:
            # Create claim record
            claim = Claim(
                item_id=item.id,
                claimer_name=claimer_name,
                claimer_email=claimer_email,
                claimer_phone=claimer_phone,
                claim_proof=claim_proof,
                claim_reason=claim_reason,
                status='pending'
            )
            
            # Do not update item status here; status will be updated upon admin approval
            item.claimed_at = None
            item.claimed_by = None
            item.claimer_email = None
            item.claimer_phone = None
            item.claim_proof = None
            
            db.session.add(claim)
            db.session.commit()
            
            # Notify admins about the claim
            admin_users = User.query.filter_by(role='admin').all()
            for admin in admin_users:
                create_notification(
                    admin.id,
                    f'New Item Claim - {item.title}',
                    f'Item "{item.title}" has been claimed by {claimer_name}. Please review the claim.',
                    'alert'
                )
            
            flash('Your claim has been submitted successfully! An admin will review it shortly.', 'success')
            return redirect(url_for('items'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error submitting claim: {str(e)}', 'error')
            print(f"Claim submission error: {e}")
    
    system_info = get_system_info()
    return render_template('public/claim_item.html', item=item, system_info=system_info)

@app.route('/admin/claims')
@login_required
def admin_claims():
    """Admin interface for managing claims"""
    claims = Claim.query.order_by(Claim.created_at.desc()).all()
    return render_template('admin/claims.html', claims=claims)

@app.route('/admin/claims/view/<int:claim_id>')
@login_required
def view_claim(claim_id):
    """View detailed claim information"""
    claim = Claim.query.get_or_404(claim_id)
    return render_template('admin/view_claim.html', claim=claim)

@app.route('/admin/claims/approve/<int:claim_id>')
@login_required
def approve_claim(claim_id):
    """Approve a claim and archive the item"""
    claim = Claim.query.get_or_404(claim_id)
    
    if claim.status != 'pending':
        flash('This claim has already been processed.', 'error')
        return redirect(url_for('admin_claims'))
    
    # Update claim status
    claim.status = 'approved'
    claim.processed_at = datetime.utcnow()
    claim.processed_by = current_user.id
    
    # Update item status to claimed
    item = claim.item
    item.status = 'claimed'
    item.claimed_at = datetime.utcnow()
    item.claimed_by = claim.claimer_name
    item.claimer_email = claim.claimer_email
    item.claimer_phone = claim.claimer_phone
    item.claim_proof = claim.claim_proof
    item.claim_notes = f'Claim approved by {current_user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}'
    
    db.session.commit()
    
    # Create notification for claimer
    create_notification(
        claim.claimer_email,  # This would need to be a user ID in a real system
        f'Claim Approved - {item.title}',
        f'Your claim for "{item.title}" has been approved! Please contact the admin to arrange pickup.',
        'system'
    )
    
    flash('Claim approved successfully! Item has been archived.', 'success')
    return redirect(url_for('admin_claims'))

@app.route('/admin/claims/reject/<int:claim_id>', methods=['GET', 'POST'])
@login_required
def reject_claim(claim_id):
    """Reject a claim and return item to found status"""
    claim = Claim.query.get_or_404(claim_id)
    
    if claim.status != 'pending':
        flash('This claim has already been processed.', 'error')
        return redirect(url_for('admin_claims'))
    
    if request.method == 'POST':
        admin_notes = request.form.get('admin_notes', '')
        
        # Update claim status
        claim.status = 'rejected'
        claim.processed_at = datetime.utcnow()
        claim.processed_by = current_user.id
        claim.admin_notes = admin_notes
        
        # Return item to found status
        item = claim.item
        item.status = 'found'
        item.claimed_at = None
        item.claimed_by = None
        item.claimer_email = None
        item.claimer_phone = None
        item.claim_proof = None
        item.claim_notes = f'Claim rejected by {current_user.username} on {datetime.utcnow().strftime("%Y-%m-%d %H:%M")}. Reason: {admin_notes}'
        
        db.session.commit()
        
        flash('Claim rejected successfully! Item has been returned to found status.', 'success')
        return redirect(url_for('admin_claims'))
    
    return render_template('admin/reject_claim.html', claim=claim)

# Initialize database and create default data
with app.app_context():
    try:
        # Create backup before making changes
        backup_database()
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Create default admin user if none exists
        if not User.query.filter_by(role='admin').first():
            admin = User(
                username='admin',
                email='admin@foundit.com',
                password_hash=generate_password_hash('admin123'),
                role='admin'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created: username='admin', password='admin123'")
        
        # Create default categories if none exist
        if Category.query.count() == 0:
            categories = [
                Category(name='Electronics', description='Phones, laptops, tablets, etc.', icon='fas fa-mobile-alt', color='#007bff'),
                Category(name='Jewelry', description='Rings, necklaces, watches, etc.', icon='fas fa-gem', color='#ffc107'),
                Category(name='Clothing', description='Shirts, pants, jackets, etc.', icon='fas fa-tshirt', color='#28a745'),
                Category(name='Documents', description='IDs, cards, papers, etc.', icon='fas fa-file-alt', color='#dc3545'),
                Category(name='Keys', description='Car keys, house keys, etc.', icon='fas fa-key', color='#6c757d'),
                Category(name='Books', description='Textbooks, notebooks, etc.', icon='fas fa-book', color='#17a2b8'),
                Category(name='Sports', description='Sports equipment, gym items, etc.', icon='fas fa-futbol', color='#fd7e14'),
                Category(name='Other', description='Miscellaneous items', icon='fas fa-box', color='#6f42c1')
            ]
            for category in categories:
                db.session.add(category)
            db.session.commit()
            print("✅ Enhanced default categories created!")
        
        # Create system info if it doesn't exist
        system_info = get_system_info()
        if not system_info.about_content:
            system_info.about_content = """
            Welcome to FOUND IT - Your Smart Lost and Found System!
            
            Our AI-powered platform helps you find lost items and return found ones quickly and efficiently. 
            With advanced matching algorithms, real-time notifications, and comprehensive search capabilities, 
            we make the process of reuniting people with their belongings as simple as possible.
            
            Features:
            • Smart AI Matching
            • Real-time Notifications
            • Advanced Search & Filtering
            • Mobile-Ready APIs
            • Comprehensive Analytics
            • Item Claiming System
            
            Whether you've lost something or found an item, FOUND IT is here to help!
            """
            system_info.contact_email = "admin@foundit.com"
            system_info.contact_phone = "+234 810 678 1706"
            system_info.contact_address = "ABU Zaria, Main Campus, Nigeria"
            db.session.commit()
            print("✅ System information updated!")
        
        print("✅ Database initialization completed successfully!")
        print(f"🗄️ Database location: {DATABASE_PATH}")
        
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        print("🔄 Attempting to continue with existing database...")
        
        # Try to connect to existing database
        try:
            # Test database connection
            db.session.execute('SELECT 1')
            print("✅ Successfully connected to existing database!")
        except Exception as conn_error:
            print(f"❌ Cannot connect to database: {conn_error}")
            print("🔄 Creating in-memory database as fallback...")
            # Fallback to in-memory database
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
            db.init_app(app)
            with app.app_context():
                db.create_all()
                print("✅ In-memory database created as fallback")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 