from app import create_app, db
from models.user import User
from models.farm import Farm
from models.variety import Variety
from models.inventory import Inventory
import sys
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

def init_db():
    try:
        app = create_app()
        print("Database URL:", app.config['SQLALCHEMY_DATABASE_URI'])
        print("App created successfully")
        
        # Create database if it doesn't exist
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        if not database_exists(engine.url):
            print("Creating database...")
            create_database(engine.url)
            print("Database created")
        
        with app.app_context():
            print("\nCreating database tables...")
            
            # Drop all tables first (for development only)
            try:
                db.drop_all()
                print("Dropped existing tables")
            except Exception as e:
                print("Error dropping tables:", str(e))
            
            # Create all tables
            try:
                db.create_all()
                print("Created new tables")
                
                # Verify tables were created
                print("\nTables created:")
                for table in db.metadata.tables.keys():
                    print(f"- {table}")
                
                # Try to insert a test record
                try:
                    test_user = User(
                        firebase_id="test",
                        email="test@example.com",
                        name="Test User"
                    )
                    db.session.add(test_user)
                    db.session.commit()
                    print("\nSuccessfully inserted test user")
                except Exception as e:
                    print("Error inserting test user:", str(e))
                    print("Full error details:", str(e.__dict__))
            
            except Exception as e:
                print("Error creating tables:", str(e))
                print("Full error details:", str(e.__dict__))
                sys.exit(1)
            
    except Exception as e:
        print("Error in init_db:", str(e))
        print("Full error details:", str(e.__dict__))
        sys.exit(1)

if __name__ == '__main__':
    init_db()
    print("\nDatabase initialization completed!") 