from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from App.controllers import (
    add_student_to_shortlist,
    get_student_shortlisted_positions,
    accept_student_from_shortlist,
    reject_student_from_shortlist,
    list_shortlisted_students,
    get_all_shortlists,
    get_shortlist, get_internship
)

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')


@shortlist_views.route('/shortlists/students/<int:student_id>', methods=['GET'])
@jwt_required()
def get_shortlists_students_json(student_id):
    model_type = get_jwt()
    user_id = int(get_jwt_identity())

    if model_type['type'] != 'employer':
        return jsonify({'error': 'Unauthorized access'}), 403

    shortlists = get_student_shortlisted_positions(student_id)

    if model_type['type'] == 'employer':
        shortlists = [s for s in shortlists if s["employer_id"] == user_id]

    return jsonify([
        {
            "id": s["shortlist_id"],
            "internship_id": s["internship_id"],
            "employer_id": s["employer_id"],
            "title": s.get("title"),
            "description": s.get("description")
        } for s in shortlists
    ]), 200



@shortlist_views.route('/shortlists/internships/<int:internship_id>', methods=['GET'])
@jwt_required()
def get_shortlists_internships_json(internship_id):
    model_type = get_jwt()
    user_id = int(get_jwt_identity())

    if model_type['type'] != 'employer':
        return jsonify({'error': 'Unauthorized access'}), 403

    internship = get_internship(internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404

    if internship.employer_id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403

    shortlists = list_shortlisted_students(internship_id)

    return jsonify([
        {
            "id": s["shortlist_id"],
            "student_id": s["student_id"],
            "username": s.get("username"),
            "name": s.get("name"),
            "employer_id": s.get("employer_id")
        } for s in shortlists
    ]), 200



@shortlist_views.route('/shortlists', methods=['GET'])
@jwt_required()
def get_all_shortlists_json():
    model_type = get_jwt()
    user_id = int(get_jwt_identity())

        
    if model_type['type'] == 'employer':
        shortlists = [
            s for s in get_all_shortlists()
            if s.internship and s.internship.employer_id == user_id
        ]
    else:
        return jsonify({'error': 'Unauthorized access'}), 403

    return jsonify([
        {
            'id': s.id,
            'student_id': s.student_id,
            'internship_id': s.internship_id,
            'employer_id': s.internship.employer_id if s.internship else None
        } for s in shortlists
    ]), 200


@shortlist_views.route('/shortlists/<int:shortlist_id>', methods=['GET'])
@jwt_required()
def get_single_shortlist_json(shortlist_id):
    model_type = get_jwt()
    user_id = int(get_jwt_identity())

    shortlist = get_shortlist(shortlist_id)
    if not shortlist:
        return jsonify({'error': 'Shortlist not found'}), 404

    internship = get_internship(shortlist.internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404

 
    if model_type['type'] == 'employer':
        if internship.employer_id != user_id:
            return jsonify({'error': 'Unauthorized access'}), 403
    else:
        return jsonify({'error': 'Unauthorized access'}), 403

    return jsonify({
        'id': shortlist.id,
        'student_id': shortlist.student_id,
        'internship_id': shortlist.internship_id,
        'employer_id': internship.employer_id
    }), 200


@shortlist_views.route('/shortlists', methods=['POST'])
@jwt_required()
def add_shortlist_api():
    model_type = get_jwt()
    if model_type['type'] != 'employer':
        return jsonify({'error': 'Unauthorized access'}), 403

    data = request.get_json()
    student_id = data.get('student_id')
    internship_id = data.get('internship_id')

    if not student_id or not internship_id:
        return jsonify({'error': 'Missing student_id or internship_id'}), 400

    
    internship = get_internship(internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404

    current_employer_id = int(get_jwt_identity())
    if internship.employer_id != current_employer_id:
        return jsonify({'error': 'Unauthorized access — not your internship'}), 403

  
    shortlist = add_student_to_shortlist(student_id, internship_id)
    if not shortlist:
        return jsonify({'error': 'Could not add to shortlist'}), 400

    return jsonify({
        'message': f"Student {student_id} shortlisted for internship {internship_id}."
    }), 200



@shortlist_views.route('/shortlists/<int:shortlist_id>/accept', methods=['POST'])
@jwt_required()
def accept_shortlist(shortlist_id):
    model_type = get_jwt()
    if model_type['type'] != 'employer':
        return jsonify({'error': 'Unauthorized access'}), 403

    shortlist = get_shortlist(shortlist_id)
    if not shortlist:
        return jsonify({'error': 'Shortlist not found'}), 404

    internship = get_internship(shortlist.internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404


    if internship.employer_id != int(get_jwt_identity()):
        return jsonify({'error': 'Unauthorized access'}), 403

    if accept_student_from_shortlist(shortlist_id):
        return jsonify({'message': 'Student accepted for internship.'}), 200

    return jsonify({'error': 'Could not accept student.'}), 400


@shortlist_views.route('/shortlists/<int:shortlist_id>/reject', methods=['POST'])
@jwt_required()
def reject_shortlist(shortlist_id):
    model_type = get_jwt()
    if model_type['type'] != 'employer':
        return jsonify({'error': 'Unauthorized access'}), 403

    shortlist = get_shortlist(shortlist_id)
    if not shortlist:
        return jsonify({'error': 'Shortlist not found'}), 404

    internship = get_internship(shortlist.internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404

   
    if internship.employer_id != int(get_jwt_identity()):
        return jsonify({'error': 'Unauthorized access'}), 403

    if reject_student_from_shortlist(shortlist_id):
        return jsonify({'message': 'Student rejected for internship.'}), 200

    return jsonify({'error': 'Could not reject student.'}), 400
