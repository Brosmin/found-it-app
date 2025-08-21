# FOUND IT Project Overview

## Project Purpose
FOUND IT is a smart lost and found system designed to help users report, search, and claim lost or found items, with an admin approval workflow and analytics. The system is web-based (Flask/Python backend) and previously included a mobile app (now removed).

## Key Features
- Post lost or found items (immediately visible to public)
- Admin approval for claims and item status changes
- Item statuses: found, lost, claimed, archived, recovered
- Claiming system: users submit claims, admin approves/rejects
- Analytics dashboard for admins
- User authentication (admin/staff roles)
- Category management
- Notification system
- Smart matching for similar items

## Item Status Workflow
- Items can be posted as 'found' or 'lost'
- Users can claim found items; claim is 'pending' until admin approval
- Upon admin approval, item status changes to 'claimed'
- Items can be marked as 'archived' (e.g., found by owner) or 'recovered' (new feature)
- Admin can remove or recover items as needed

## Admin Features
- Approve/unapprove items
- Approve/reject claims
- Manage users, categories, messages
- View analytics and notifications

## Public Features
- Browse/search items by status, category, or keywords
- View recent items
- Submit claims for found items
- Register/login as user

## Technical Stack
- Python 3, Flask, SQLAlchemy, SQLite
- HTML/CSS/Bootstrap (Jinja2 templates)
- No mobile app or APK download (removed for simplicity)

## Directory Structure (after cleanup)
- app.py: Main Flask app and backend logic
- templates/: HTML templates for web UI
- static/: Static files (CSS, images)
- instance/: SQLite database (lost_and_found.db)
- test_*.py: Test scripts for backend logic
- requirements.txt: Python dependencies
- README.md: Project overview

## Recent Enhancements
- Item status now only changes to 'claimed' after admin approval
- Added 'recovered' status and public button to view recovered items
- Removed mobile app and related download links
- Cleaned up unnecessary folders/files

## How to Use
1. Run the Flask app (`python app.py`)
2. Access the web UI to post, search, and claim items
3. Admins log in to approve items/claims and manage the system

## Documentation Guidance
- Use this file as a summary for ChatGPT or any documentation tool
- For detailed structure, see the codebase and templates
- For citation, use in-text references to code files and features as needed

---
This file provides a complete, up-to-date summary of your FOUND IT project for documentation purposes.
