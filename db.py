from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association table for Farm-Variety many-to-many relationship
farm_variety = db.Table('farm_variety',
    db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'), primary_key=True),
    db.Column('variety_id', db.Integer, db.ForeignKey('varieties.id'), primary_key=True)
)

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
    