from app import create_app, db
from models import User, Product, Order, OrderItem

app = create_app()

def init_db():
    with app.app_context():
        # Create all tables
        db.create_all()
        print("Database tables created successfully!")

if __name__ == '__main__':
    init_db() 