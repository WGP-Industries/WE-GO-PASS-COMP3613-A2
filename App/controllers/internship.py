from App.models import Internship
from App.database import db

def create_internship(title, description, employer_id):
    new_internship = Internship(title=title, description=description, employer_id=employer_id)
    try:
        db.session.add(new_internship)
        db.session.commit()
        return new_internship
    except Exception as e:
        print(e)
        return None
    
def get_internship(id):
    return Internship.query.get(id)

def is_internship(id):
    return Internship.query.get(id) != None

def get_all_internship():
    return Internship.query.all()