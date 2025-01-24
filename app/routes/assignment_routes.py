from flask import Blueprint, request, jsonify
from app import db
from app.models import UserRoleAssignment, User, Role
from datetime import datetime

# Create a Blueprint for user-role assignment routes
assignment_routes = Blueprint('assignment_routes', __name__)

@assignment_routes.route('/user-roles', methods=['POST'])
def assign_role():
    data = request.get_json()

    user_id = data.get('user_id')
    role_id = data.get('role_id')

    # Validate inputs
    if not user_id or not role_id:
        return jsonify({'message': 'User ID and Role ID are required'}), 400

    # Check if the user and role exist
    user = User.query.get(user_id)
    role = Role.query.get(role_id)
    
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    if not role:
        return jsonify({'message': 'Role not found'}), 404
    
    # Check for existing duplicate assignment
    existing_assignment = UserRoleAssignment.query.filter_by(user_id=user_id, role_id=role_id).first()
    if existing_assignment:
        return jsonify({'message': 'Role already assigned to the user'}), 400

    # Create the assignment
    assignment = UserRoleAssignment(user_id=user_id, role_id=role_id, assigned_date=datetime.utcnow())
    db.session.add(assignment)
    db.session.commit()

    return jsonify({'message': 'Role assigned successfully', 'assignment': assignment.to_dict()}), 200
@assignment_routes.route('/user-roles', methods=['GET'])
def get_assignments():
    user_id = request.args.get('user_id')
    role_id = request.args.get('role_id')

    query = UserRoleAssignment.query
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    if role_id:
        query = query.filter_by(role_id=role_id)

    assignments = query.all()

    return jsonify({'assignments': [assignment.to_dict() for assignment in assignments]}), 200
@assignment_routes.route('/user-roles/<int:id>', methods=['DELETE'])
def delete_assignment(id):
    assignment = UserRoleAssignment.query.get(id)
    
    if not assignment:
        return jsonify({'message': 'Assignment not found'}), 404
    
    db.session.delete(assignment)
    db.session.commit()

    return jsonify({'message': 'Assignment deleted successfully'}), 200