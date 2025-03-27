from datetime import datetime
from .base import db, farm_variety

class Farm(db.Model):
    __tablename__ = 'farms'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    varieties = db.relationship('Variety', secondary=farm_variety,
                              backref=db.backref('farms', lazy='dynamic'),
                              lazy='dynamic')
    inventory_items = db.relationship('Inventory', backref='farm', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'phone_number': self.phone_number,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'varieties': [variety.to_dict() for variety in self.varieties],
            'inventory': [item.to_dict() for item in self.inventory_items]
        }

    @classmethod
    def create_farm(cls, email, phone_number):
        """Create a new farm"""
        farm = cls(
            email=email,
            phone_number=phone_number
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

    def add_variety(self, variety):
        """Add a variety to the farm"""
        if variety not in self.varieties:
            self.varieties.append(variety)
            db.session.commit()
            return True
        return False

    def remove_variety(self, variety):
        """Remove a variety from the farm"""
        if variety in self.varieties:
            self.varieties.remove(variety)
            db.session.commit()
            return True
        return False 