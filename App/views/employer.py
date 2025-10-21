from flask import Blueprint, render_template, jsonify, request, send_from_directory, flash, redirect, url_for
from App.controllers import (
    create_employer,
    get_all_employer
)

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')



# API Routes 

@employer_views.route('/api/employers', methods=['GET'])
def get_employers_json():
    employers = get_all_employer()
    return jsonify([
        {'id': e.id, 'username': e.username, 'company': e.company}
        for e in employers
    ])

@employer_views.route('/api/employers', methods=['POST'])
def create_employer_api():
    data = request.json
    employer = create_employer(data['username'], data['password'], data.get('company'))
    if employer:
        return jsonify({'message': f"Employer {employer.username} created with id {employer.id}"})
    return jsonify({'error': 'Could not create employer'}), 400


