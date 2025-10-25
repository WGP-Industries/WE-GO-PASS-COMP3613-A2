from App.models import Shortlist, Internship, Student
from App.database import db


# Get shortlisted internships for a student
def get_student_shortlisted_positions(student_id):
    shortlists = Shortlist.query.filter_by(student_id=student_id).all()
    results = []

    for shortlist in shortlists:
        internship = Internship.query.get(shortlist.internship_id)
        if internship:
            results.append({
                "shortlist_id": shortlist.id,
                "internship_id": internship.id,
                "title": internship.title,
                "description": internship.description,
                "status": internship.status,
                "employer_id": internship.employer_id,
            })
    return results


# Get all shortlists
def get_all_shortlists():
    return Shortlist.query.all()


# Get a single shortlist
def get_shortlist(shortlist_id):
    return Shortlist.query.get(shortlist_id)


def add_student_to_shortlist(student_id, internship_id):
    internship = Internship.query.get(internship_id)
    if not internship:
        return None

    existing = Shortlist.query.filter_by(
        student_id=student_id,
        internship_id=internship_id
    ).first()

    if existing:
        return None

    try:
        new_shortlist = Shortlist(student_id=student_id, internship_id=internship_id)
        db.session.add(new_shortlist)
        db.session.commit()
        return new_shortlist
    except Exception:
        db.session.rollback()
        return None



# Accept student from shortlist
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


# Reject student from shortlist
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


# List students shortlisted for a given internship
def list_shortlisted_students(internship_id):
    shortlists = Shortlist.query.filter_by(internship_id=internship_id).all()
    results = []

    for s in shortlists:
        student = Student.query.get(s.student_id)
        internship = Internship.query.get(s.internship_id)
        if student and internship:
            results.append({
                "shortlist_id": s.id,
                "student_id": student.id,
                "username": student.username,
                "name": getattr(student, 'name', None),
                "employer_id": internship.employer_id,
                "internship_title": internship.title,
            })
    return results
