from flask import jsonify
from . import main

@main.route('/')
def index():
    return jsonify({"message": "Welcome to MeryBery API"})

@main.route('/health')
def health_check():
    return jsonify({"status": "healthy"}) 