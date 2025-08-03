#!/usr/bin/env python3
"""
Download Sample Images for FOUND IT System
This script downloads sample images for demonstration items.
"""

import os
import requests
from urllib.parse import urlparse

def download_image(url, filename):
    """Download an image from URL and save it"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        # Ensure upload directory exists
        upload_dir = 'static/uploads'
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save the image
        file_path = os.path.join(upload_dir, filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        
        print(f"✅ Downloaded {filename}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filename}: {e}")
        return False

def create_sample_images():
    """Create sample images for demo items"""
    print("🔄 Downloading sample images...")
    
    # Sample images from Unsplash (free stock photos)
    sample_images = {
        'iphone_sample.jpg': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop',
        'laptop_sample.jpg': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop',
        'keys_sample.jpg': 'https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=300&fit=crop',
        'wallet_sample.jpg': 'https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=400&h=300&fit=crop',
        'book_sample.jpg': 'https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400&h=300&fit=crop',
        'watch_sample.jpg': 'https://images.unsplash.com/photo-1524592094714-0f0654e20314?w=400&h=300&fit=crop',
        'backpack_sample.jpg': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=400&h=300&fit=crop',
        'glasses_sample.jpg': 'https://images.unsplash.com/photo-1577803645773-f96470509666?w=400&h=300&fit=crop'
    }
    
    success_count = 0
    for filename, url in sample_images.items():
        if download_image(url, filename):
            success_count += 1
    
    print(f"✅ Downloaded {success_count}/{len(sample_images)} sample images")
    
    # Create placeholder images for any failed downloads
    create_placeholder_images()
    
    return success_count

def create_placeholder_images():
    """Create simple placeholder images for any missing files"""
    upload_dir = 'static/uploads'
    os.makedirs(upload_dir, exist_ok=True)
    
    placeholder_files = [
        'iphone_sample.jpg', 'laptop_sample.jpg', 'keys_sample.jpg',
        'wallet_sample.jpg', 'book_sample.jpg', 'watch_sample.jpg',
        'backpack_sample.jpg', 'glasses_sample.jpg'
    ]
    
    for filename in placeholder_files:
        file_path = os.path.join(upload_dir, filename)
        if not os.path.exists(file_path):
            # Create a simple SVG placeholder
            svg_content = f'''<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
                <rect width="400" height="300" fill="#f8f9fa"/>
                <text x="200" y="150" font-family="Arial" font-size="24" text-anchor="middle" fill="#6c757d">
                    {filename.replace('_sample.jpg', '').title()} Image
                </text>
            </svg>'''
            
            # Save as HTML file (will be converted to image by browser)
            html_path = file_path.replace('.jpg', '.html')
            with open(html_path, 'w') as f:
                f.write(svg_content)
            
            print(f"✅ Created placeholder for {filename}")

if __name__ == "__main__":
    create_sample_images() 