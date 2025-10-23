from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_jwt_extended import jwt_required, get_jwt_identity
from App.controllers import (
    create_internship,
    get_all_internship,  get_employer
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
    emp_id = get_jwt_identity()
    employer = get_employer(id)
    if not employer:
        return jsonify({'error': 'User not authorized to perform this action'}), 403
    data = request.json
    internship = create_internship(data['title'], data['description'], emp_id)
    if internship:
        return jsonify({'message': f"Internship '{internship.title}' created with id {internship.id}"})
    return jsonify({'error': 'Could not create internship'}), 400
