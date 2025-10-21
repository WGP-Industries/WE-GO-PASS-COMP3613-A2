from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from App.controllers import (
    create_internship,
    get_all_internship
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
def create_internship_api():
    data = request.json
    internship = create_internship(data['title'], data['description'], data.get('employer_id'))
    if internship:
        return jsonify({'message': f"Internship '{internship.title}' created with id {internship.id}"})
    return jsonify({'error': 'Could not create internship'}), 400
