from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from App.controllers import (
    create_student,
    get_all_student,
    get_student,
    get_staff,
    get_student_by_username,
)

student_views = Blueprint('student_views', __name__, template_folder='../templates')




# GET all students

@student_views.route('/students', methods=['GET'])
@jwt_required()
def get_students_action():
    staff = get_staff(get_jwt_identity()) 
    student = get_student(get_jwt_identity())

    if not staff and not student:
        return jsonify({'error': 'Unauthorized access'}), 403

    students = get_all_student()
    return jsonify([{
        'id': s.id,
        'username': s.username,
        'name': s.name
    } for s in students]), 200



# CREATE a new student

@student_views.route('/students', methods=['POST'])
def create_student_action():
  

    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    existing_student = get_student_by_username(data['username'])
    if existing_student:
        return jsonify({'error': 'Username already exists'}), 400

    student = create_student(
        data['username'],
        data['password'],
        data.get('name')
    )

    if not student:
        return jsonify({'error': 'Could not create student'}), 400

    return jsonify({
        'message': f"Student {student.username} created successfully",
        'id': student.id
    }), 201



# GET a single student by ID

@student_views.route('/students/<int:student_id>', methods=['GET'])
def get_student_action(student_id):
    
    student = get_student(student_id)
    if not student:
        return jsonify({'error': 'Student not found'}), 404

    return jsonify({
        'id': student.id,
        'username': student.username,
        'name': student.name
    }), 200
