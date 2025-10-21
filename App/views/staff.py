from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import (
    create_staff,
    get_all_staff,
    get_staff
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


# API Routes 


@staff_views.route('/staff', methods=['POST'])
@jwt_required()
def create_staff_action():
  
    staff_user = get_staff(get_jwt_identity())
    if not staff_user:
        return jsonify({'error': 'User not authorized to perform this action'}), 403

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    staff = create_staff(username=data['username'], password=data['password'])
    if staff:
        return jsonify({'message': f"Staff {staff.username} created with id {staff.id}"}), 201
    return jsonify({'error': 'Could not create staff'}), 400



@staff_views.route('/staff/<int:staff_id>', methods=['GET'])
@jwt_required()
def get_single_staff(staff_id):
 
    staff_user = get_staff(get_jwt_identity())
    if not staff_user:
        return jsonify({'error': 'Unauthorized access'}), 403

    staff = get_staff(staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    return jsonify({
        'id': staff.id,
        'username': staff.username
    }), 200


