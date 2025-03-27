from datetime import datetime
from .base import db

class Variety(db.Model):
    __tablename__ = 'varieties'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship with inventory
    inventory_items = db.relationship('Inventory', backref='variety', lazy='dynamic')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

    @classmethod
    def create_variety(cls, name):
        """Create a new variety"""
        variety = cls(name=name)
        db.session.add(variety)
        db.session.commit()
        return variety

    @classmethod
    def get_by_id(cls, variety_id):
        """Get variety by ID"""
        return cls.query.get(variety_id)

    @classmethod
    def get_by_name(cls, name):
        """Get variety by name"""
        return cls.query.filter_by(name=name).first()

    @classmethod
    def update_variety(cls, variety_id, **kwargs):
        """Update variety fields"""
        variety = cls.get_by_id(variety_id)
        if variety:
            for key, value in kwargs.items():
                if hasattr(variety, key):
                    setattr(variety, key, value)
            db.session.commit()
        return variety

    @classmethod
    def delete_variety(cls, variety_id):
        """Delete variety by ID"""
        variety = cls.get_by_id(variety_id)
        if variety:
            db.session.delete(variety)
            db.session.commit()
            return True
        return False 