from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from datetime import datetime

# Create a Blueprint instance for user-related routes
user_routes = Blueprint('user_routes', __name__)

# POST /users - Create a new user
@user_routes.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()  # Get data from the request body
    name = data.get('name')
    email = data.get('email')
    status = data.get('status', 'Active')  # Default to 'Active' if not provided
    created_date = datetime.now()

    # Ensure email is unique
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists'}), 400

    # Create a new User
    new_user = User(name=name, email=email, status=status, created_date=created_date)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully', 'user': new_user.to_dict()}), 201
# @user_routes.route('/users', methods=['GET'])
# def get_users():
 #   status = request.args.get('status', 'Active')  # Default to 'Active' if no status is provided
 #   users = User.query.filter_by(status=status).all()

@user_routes.route('/users', methods=['GET'])
def get_users():
    # Get query parameters for filtering
    name = request.args.get('name')
    email = request.args.get('email')
    status = request.args.get('status', 'Active')  # Default to 'Active' if no status is provided
    
    query = User.query.filter_by(status=status)
    
    if name:
        query = query.filter(User.name.ilike(f'%{name}%'))
    if email:
        query = query.filter(User.email.ilike(f'%{email}%'))
    
    users = query.all()

    return jsonify({'users': [user.to_dict() for user in users]}), 200
    return jsonify({'users': [user.to_dict() for user in users]}), 200
@user_routes.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    return jsonify({'user': user.to_dict()}), 200

# PUT /users/{id} - Update user details
@user_routes.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    data = request.get_json()
    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    user.status = data.get('status', user.status)
    db.session.commit()

    return jsonify({'message': 'User updated successfully', 'user': user.to_dict()}), 200
# DELETE /users/{id} - Soft delete a user (mark status as "Inactive")
@user_routes.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.status = 'Inactive'  # Change status to "Inactive"
    db.session.commit()

    return jsonify({'message': 'User marked as inactive'}), 200
