from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import (
    create_employer,
    get_all_employer, get_employer
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')



# API Routes 

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
    employer = create_employer(data['username'], data['password'], data.get('company'))
    if employer:
        return jsonify({'message': f"Employer {employer.username} created with id {employer.id}"})
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