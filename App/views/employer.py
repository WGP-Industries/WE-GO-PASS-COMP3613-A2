from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import (
    create_employer,
    get_all_employer, get_employer, get_employer_by_username, login
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')



# API Routes 


# Login employer
@employer_views.route('/employers/login', methods=['POST'])
def employer_login():
    data = request.json
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing username or password'}), 400

    token = login(data['username'], data['password'], user_type='employer')
    if token:
        return jsonify({'access_token': token}), 200
    return jsonify({'error': 'Invalid credentials'}), 401

# Get all employers


@employer_views.route('/employers', methods=['GET'])
def get_employers_json():
    employers = get_all_employer()
    return jsonify([
        {'id': e.id, 'username': e.username, 'company': e.company}
        for e in employers
    ])

@employer_views.route('/employers', methods=['POST'])
def create_employer_api():
    data = request.json
    
    existing_employer = get_employer_by_username(data['username'])

    if existing_employer:
        return jsonify({'error': 'Username already exists'}), 400

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    employer = create_employer(data['username'], data['password'], data.get('company'))
    if employer:
        return jsonify({'message': f"Employer {employer.username} created with id {employer.id}"}), 201
    
    return jsonify({'error': 'Could not create employer'}), 400


# Get single employer
@employer_views.route('/employers/<int:employer_id>', methods=['GET'])
def get_single_employer_json(employer_id):
    employer = get_employer(employer_id)
    if not employer:
        return jsonify({'error': 'Employer not found'}), 404
    return jsonify({
        'id': employer.id,
        'username': employer.username,
        'company': employer.company
    })  