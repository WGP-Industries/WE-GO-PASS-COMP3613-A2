from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity, set_access_cookies
from App.controllers import (
    create_staff,
    get_all_staff,
    get_staff,
    get_staff_by_username, login
)

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')


# API Routes 


# login route for staff
@staff_views.route('/staff/login', methods=['POST'])
def staff_login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    token = login(data['username'], data['password'], user_type='staff')
    if token:
        response = jsonify({'access_token': token})
        set_access_cookies(response, token)
        return response, 200   
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

# GET all staff

@staff_views.route('/staff', methods=['GET'])
@jwt_required()
def get_staff_action():
    
    model_type = get_jwt()

    if model_type['type'] != 'staff':
        return jsonify({'error': 'Unauthorized access'}), 403   
    
    existing_staff =  get_staff(get_jwt_identity())
    if not existing_staff:
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
 
    model_type = get_jwt()

    if model_type['type'] != 'staff':
        return jsonify({'error': 'Unauthorized access'}), 403  

    staff = get_staff(staff_id)
    if not staff:
        return jsonify({'error': 'Staff not found'}), 404

    return jsonify({
        'id': staff.id,
        'username': staff.username
    }), 200


