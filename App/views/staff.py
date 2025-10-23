from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import (
    create_staff,
    get_all_staff,
    get_staff,
    get_staff_by_username,
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


# API Routes 


# GET all staff

@staff_views.route('/staff', methods=['GET'])
@jwt_required()
def get_staff_action():
 
    user = get_staff(get_jwt_identity()) 
    if not user:
        return jsonify({'error': 'Unauthorized access'}), 403

    staff = get_all_staff()
    return jsonify([{
        'id': s.id,
        'username': s.username,
    } for s in staff]), 200




@staff_views.route('/staff', methods=['POST'])
def create_staff_action():
  

    data = request.get_json()
    
    existing_staff = get_staff_by_username(data['username'])

    if existing_staff:
        return jsonify({'error': 'Username already exists'}), 400


    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    staff = create_staff(username=data['username'], password=data['password'])
    if staff:
        return jsonify({'message': f"Staff created with id: {staff.id}, username: {staff.username}"}), 201
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


