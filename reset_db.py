from app import create_app
from models import db

# Create the Flask app
app = create_app()

# Drop and recreate all tables
with app.app_context():
    print("🔴 Dropping all tables...")
    db.drop_all()

    print("🛠 Recreating all tables...")
    db.create_all()

    print("✅ Database reset complete!")