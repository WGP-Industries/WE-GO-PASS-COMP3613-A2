from App.models import Shortlist, Internship, Student
from App.database import db

def get_student_shortlisted_positions(student_id):
    shortlists = Shortlist.query.filter_by(student_id=student_id).all()
    results = []
    for shortlist in shortlists:
        internship = Internship.query.get(shortlist.internship_id)
        if internship:
            results.append({
                "internship_id": internship.id,
                "title": internship.title,
                "description": internship.description,
                "status": internship.status  
            })
    return results


def add_student_to_shortlist(student_id, internship_id):
    new_shortlist = Shortlist(student_id=student_id, internship_id=internship_id)
    try:
        db.session.add(new_shortlist)
        db.session.commit()
        return new_shortlist
    except Exception as e:
        print(e)
        return None
    
def accept_student_from_shortlist(shortlist_id):
    shortlist = Shortlist.query.get(shortlist_id)
    if not shortlist:
        return False
    internship = Internship.query.get(shortlist.internship_id)
    if not internship:
        return False
    internship.accept()
    db.session.commit()
    return True

def reject_student_from_shortlist(shortlist_id):
    shortlist = Shortlist.query.get(shortlist_id)
    if not shortlist:
        return False
    internship = Internship.query.get(shortlist.internship_id)
    if not internship:
        return False
    internship.reject()
    db.session.commit()
    return True



def list_shortlisted_students(internship_id):
    shortlists = Shortlist.query.filter_by(internship_id=internship_id).all()
    results = []
    for s in shortlists:
        student = Student.query.get(s.student_id)
        if student:
            results.append({
                "id": student.id,
                "username": student.username,
                "name": getattr(student, 'name', None)
            })
    return results
