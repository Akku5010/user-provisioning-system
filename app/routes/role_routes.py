from flask import Blueprint, request, jsonify  # Add request and jsonify
from app import db
from app.models import Role

# Create a Blueprint for role-related routes
role_routes = Blueprint('role_routes', __name__)

@role_routes.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()  # Get JSON data from the request
    name = data.get('name')
    description = data.get('description', '')  # Default to empty string if not provided

    # Check if the role name already exists
    if Role.query.filter_by(name=name).first():
        return jsonify({'message': 'Role name already exists'}), 400

    # Create a new Role
    new_role = Role(name=name, description=description)
    db.session.add(new_role)
    db.session.commit()

    return jsonify({'message': 'Role created successfully', 'role': {'id': new_role.id, 'name': new_role.name, 'description': new_role.description}}), 200
# GET /roles - Fetch all roles
@role_routes.route('/roles', methods=['GET'])
def get_roles():
    roles = Role.query.all()  # Fetch all roles
    return jsonify({'roles': [role.to_dict() for role in roles]}), 200


# GET /roles/{id} - Fetch a role by its ID
@role_routes.route('/roles/<int:id>', methods=['GET'])
def get_role(id):
    role = Role.query.get(id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    return jsonify({'role': role.to_dict()}), 200


# PUT /roles/{id} - Update a role by its ID
@role_routes.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get(id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    data = request.get_json()
    role.name = data.get('name', role.name)
    role.description = data.get('description', role.description)
    db.session.commit()

    return jsonify({'message': 'Role updated successfully', 'role': role.to_dict()}), 200


# DELETE /roles/{id} - Soft delete a role
@role_routes.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get(id)
    if not role:
        return jsonify({'message': 'Role not found'}), 404

    db.session.delete(role)  # Alternatively, mark it inactive if you prefer soft deletion
    db.session.commit()

    return jsonify({'message': 'Role deleted successfully'}), 200