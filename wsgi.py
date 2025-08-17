from app import app

# Ensure database is properly initialized
with app.app_context():
    try:
        from app import db
        db.create_all()
        print("✅ Database tables created successfully in wsgi!")
    except Exception as e:
        print(f"❌ Database initialization error in wsgi: {e}")

if __name__ == "__main__":
    app.run() 