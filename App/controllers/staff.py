from App.models import Staff
from App.database import db


def create_staff(username, password):
    newuser = Staff(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None


def get_staff(id):
    return Staff.query.get(id)

def is_staff(id):
    return Staff.query.get(id) != None

def get_all_staff():
    return Staff.query.all()