from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import get_jwt, jwt_required, get_jwt_identity
from App.controllers import (
    create_internship,
    get_all_internship,  get_internship 
)

internship_views = Blueprint('internship_views', __name__, template_folder='../templates')




# API Routes 

@internship_views.route('/internships', methods=['GET'])
def get_internships_json():
    internships = get_all_internship()
    return jsonify([
        {
            'id': i.id,
            'title': i.title,
            'description': i.description,
            'status': i.status,
            'employer_id': i.employer_id
        } for i in internships
    ])

@internship_views.route('/internships', methods=['POST'])
@jwt_required()
def create_internship_api():
    model_type = get_jwt()
    emp_id = get_jwt_identity()

    if model_type['type'] != 'employer':
        return jsonify({'error': 'Unauthorized access'}), 403  

    data = request.json
    if not data or 'title' not in data or 'description' not in data:
        return jsonify({'error': 'Missing required fields'}), 400


    internship = create_internship(data['title'], data['description'], emp_id)

    if internship:
        return jsonify({
            'message': f"Internship created: '{internship.title}' with ID {internship.id}"
        }), 201

    return jsonify({'error': 'Could not create internship'}), 400


# Get single internship
@internship_views.route('/internships/<int:internship_id>', methods=['GET'])
def get_internship_json(internship_id):
    internship = get_internship(internship_id)
    if internship:
        return jsonify({
            'id': internship.id,
            'title': internship.title,
            'description': internship.description,
            'status': internship.status,
            'employer_id': internship.employer_id
        }), 200
    return jsonify({'error': 'Internship not found'}), 404