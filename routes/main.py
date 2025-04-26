from flask import Blueprint, jsonify, request
from models.user import User
from models.farm import Farm
from models.variety import Variety
from models.inventory import Inventory

main = Blueprint('main', __name__)

# User routes
@main.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.create_user(
        firebase_id=data['firebase_id'],
        email=data['email'],
        name=data['name'],
        location=data.get('location'),
        phone_number=data.get('phone_number')
    )
    return jsonify(user.to_dict()), 201

@main.route('/users/<firebase_id>', methods=['GET'])
def get_user(firebase_id):
    user = User.get_by_firebase_id(firebase_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'error': 'User not found'}), 404

# Farm routes
@main.route('/farms', methods=['POST'])
def create_farm():
    data = request.get_json()
    farm = Farm.create_farm(
        name=data['name'],
        location=data['location'],
        owner_id=data['owner_id']
    )
    return jsonify(farm.to_dict()), 201

@main.route('/farms/<int:farm_id>', methods=['GET'])
def get_farm(farm_id):
    farm = Farm.get_by_id(farm_id)
    if farm:
        return jsonify(farm.to_dict())
    return jsonify({'error': 'Farm not found'}), 404

# Variety routes
@main.route('/varieties', methods=['POST'])
def create_variety():
    data = request.get_json()
    variety = Variety.create_variety(
        name=data['name'],
        description=data.get('description')
    )
    return jsonify(variety.to_dict()), 201

@main.route('/varieties/<int:variety_id>', methods=['GET'])
def get_variety(variety_id):
    variety = Variety.get_by_id(variety_id)
    if variety:
        return jsonify(variety.to_dict())
    return jsonify({'error': 'Variety not found'}), 404

# Inventory routes
@main.route('/inventory', methods=['POST'])
def create_inventory():
    data = request.get_json()
    inventory = Inventory.create_inventory(
        farm_id=data['farm_id'],
        variety_id=data['variety_id'],
        count=data['count'],
        price=data['price']
    )
    return jsonify(inventory.to_dict()), 201

@main.route('/inventory/<int:inventory_id>', methods=['GET'])
def get_inventory(inventory_id):
    inventory = Inventory.get_by_id(inventory_id)
    if inventory:
        return jsonify(inventory.to_dict())
    return jsonify({'error': 'Inventory not found'}), 404 