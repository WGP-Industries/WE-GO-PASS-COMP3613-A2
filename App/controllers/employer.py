from App.models import Employer
from App.database import db


def create_employer(username, password, company=None):
    if company is None:
        company = username  # or some default

    
    newuser = Employer(username=username, password=password, company=company)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except Exception as e:
        print(e)
        return None
    
def get_employer(id):
    return Employer.query.get(id)

def get_employer_by_username(username):
    result = db.session.execute(db.select(Employer).filter_by(username=username))
    return result.scalar_one_or_none()

def is_employer(id):
    return Employer.query.get(id) != None

def get_all_employer():
    return Employer.query.all()