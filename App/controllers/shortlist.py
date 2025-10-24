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
                "status": internship.status,
                "employer_id": internship.employer_id,
                "id": shortlist.id
            })
    return results

def get_all_shortlists():
    return Shortlist.query.all()

def get_shortlist(shortlist_id):
    return Shortlist.query.get(shortlist_id)


def add_student_to_shortlist(student_id, internship_id, employer_id):
    new_shortlist = Shortlist(student_id=student_id, internship_id=internship_id, employer_id=employer_id)

    ShortlistExists = db.session.execute(
        db.select(Shortlist).filter_by(student_id=student_id, internship_id=internship_id, employer_id=employer_id)
    ).scalar_one_or_none()

    if ShortlistExists:
        return None  # Student already shortlisted for this internship
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
                "id": s.id,
                "username": student.username,
                "name": getattr(student, 'name', None),
                "employer_id": s.employer_id,
                "student_id": s.student_id,
            })
    return results
