from datetime import datetime
from .base import db

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    farm_id = db.Column(db.Integer, db.ForeignKey('farms.id'), nullable=False)
    variety_id = db.Column(db.Integer, db.ForeignKey('varieties.id'), nullable=False)
    price = db.Column(db.Float, nullable=False)
    count = db.Column(db.Integer, nullable=False, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Ensure unique combination of farm and variety
    __table_args__ = (
        db.UniqueConstraint('farm_id', 'variety_id', name='uix_farm_variety'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'farm_id': self.farm_id,
            'variety_id': self.variety_id,
            'price': self.price,
            'count': self.count,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'variety': self.variety.to_dict()
        }

    @classmethod
    def create_inventory_item(cls, farm_id, variety_id, price, count=0):
        """Create a new inventory item"""
        inventory_item = cls(
            farm_id=farm_id,
            variety_id=variety_id,
            price=price,
            count=count
        )
        db.session.add(inventory_item)
        db.session.commit()
        return inventory_item

    @classmethod
    def get_by_id(cls, inventory_id):
        """Get inventory item by ID"""
        return cls.query.get(inventory_id)

    @classmethod
    def get_by_farm_and_variety(cls, farm_id, variety_id):
        """Get inventory item by farm and variety"""
        return cls.query.filter_by(farm_id=farm_id, variety_id=variety_id).first()

    @classmethod
    def update_inventory_item(cls, inventory_id, **kwargs):
        """Update inventory item fields"""
        item = cls.get_by_id(inventory_id)
        if item:
            for key, value in kwargs.items():
                if hasattr(item, key):
                    setattr(item, key, value)
            db.session.commit()
        return item

    @classmethod
    def delete_inventory_item(cls, inventory_id):
        """Delete inventory item by ID"""
        item = cls.get_by_id(inventory_id)
        if item:
            db.session.delete(item)
            db.session.commit()
            return True
        return False

    @classmethod
    def update_count(cls, inventory_id, count_change):
        """Update the count of an inventory item"""
        item = cls.get_by_id(inventory_id)
        if item:
            new_count = item.count + count_change
            if new_count >= 0:  # Prevent negative inventory
                item.count = new_count
                db.session.commit()
                return True
        return False 