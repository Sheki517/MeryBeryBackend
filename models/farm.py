from datetime import datetime
from .base import db

class Farm(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    inventory_items = db.relationship('Inventory', backref='farm', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone_number': self.phone_number,
            'location': self.location,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'varieties': [variety.to_dict() for variety in self.varieties],
            'inventory': [item.to_dict() for item in self.inventory_items]
        }

    @classmethod
    def create_farm(cls, name, email, phone_number, location):
        """Create a new farm"""
        farm = cls(
            name=name,
            email=email,
            phone_number=phone_number,
            location=location
        )
        db.session.add(farm)
        db.session.commit()
        return farm

    @classmethod
    def get_by_id(cls, farm_id):
        """Get farm by ID"""
        return cls.query.get(farm_id)

    @classmethod
    def get_by_email(cls, email):
        """Get farm by email"""
        return cls.query.filter_by(email=email).first()

    @classmethod
    def update_farm(cls, farm_id, **kwargs):
        """Update farm fields"""
        farm = cls.get_by_id(farm_id)
        if farm:
            for key, value in kwargs.items():
                if hasattr(farm, key):
                    setattr(farm, key, value)
            db.session.commit()
        return farm

    @classmethod
    def delete_farm(cls, farm_id):
        """Delete farm by ID"""
        farm = cls.get_by_id(farm_id)
        if farm:
            db.session.delete(farm)
            db.session.commit()
            return True
        return False