from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Initialize SQLAlchemy
db = SQLAlchemy()

# Association table for Farm-Variety many-to-many relationship
farm_variety = db.Table('farm_variety',
    db.Column('farm_id', db.Integer, db.ForeignKey('farms.id'), primary_key=True),
    db.Column('variety_id', db.Integer, db.ForeignKey('varieties.id'), primary_key=True)
) 