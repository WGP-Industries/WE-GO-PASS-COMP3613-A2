from flask import Blueprint, render_template, jsonify, request, redirect, url_for, flash
from App.controllers import (
    add_student_to_shortlist,
    get_student_shortlisted_positions,
    accept_student_from_shortlist,
    reject_student_from_shortlist
)

shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')


    

# API Routes 

@shortlist_views.route('/shortlists/<int:student_id>', methods=['GET'])
def get_shortlists_json(student_id):
    shortlists = get_student_shortlisted_positions(student_id)
    return jsonify(shortlists)

@shortlist_views.route('/shortlists', methods=['POST'])
def add_shortlist_api():
    data = request.json
    student_id = data.get('student_id')
    internship_id = data.get('internship_id')
    shortlist = add_student_to_shortlist(student_id, internship_id)
    if shortlist:
        return jsonify({'message': f"Student {student_id} shortlisted for internship {internship_id}."})
    return jsonify({'error': 'Could not add to shortlist'}), 400

@shortlist_views.route('/shortlists/<int:shortlist_id>/accept', methods=['POST'])
def accept_shortlist(shortlist_id):
    if accept_student_from_shortlist(shortlist_id):
        return jsonify({'message': 'Student accepted for internship.'})
    return jsonify({'error': 'Could not accept student.'}), 400

@shortlist_views.route('/shortlists/<int:shortlist_id>/reject', methods=['POST'])
def reject_shortlist(shortlist_id):
    if reject_student_from_shortlist(shortlist_id):
        return jsonify({'message': 'Student rejected for internship.'})
    return jsonify({'error': 'Could not reject student.'}), 400
