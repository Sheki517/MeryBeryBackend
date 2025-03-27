from datetime import datetime
from .base import db

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firebase_id = db.Column(db.String(128), unique=True, nullable=False)  # Firebase UID
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))  # Optional
    phone_number = db.Column(db.String(20))  # Optional
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'firebase_id': self.firebase_id,
            'email': self.email,
            'name': self.name,
            'location': self.location,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def create_user(cls, firebase_id, email, name, location=None, phone_number=None):
        """Create a new user with required and optional fields"""
        user = cls(
            firebase_id=firebase_id,
            email=email,
            name=name,
            location=location,
            phone_number=phone_number
        )
        db.session.add(user)
        db.session.commit()
        return user

    @classmethod
    def get_by_firebase_id(cls, firebase_id):
        """Get user by Firebase ID"""
        return cls.query.filter_by(firebase_id=firebase_id).first()

    @classmethod
    def get_by_email(cls, email):
        """Get user by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def update_user(cls, firebase_id, **kwargs):
        """Update user fields"""
        user = cls.get_by_firebase_id(firebase_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
            db.session.commit()
        return user

    @classmethod
    def delete_user(cls, firebase_id):
        """Delete user by Firebase ID"""
        user = cls.get_by_firebase_id(firebase_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False 