from App.models import Student
from App.database import db




def create_student(username, password, name=None):
    if name is None:
        name = username  # or some default
    newuser = Student(username=username, password=password, name=name)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except Exception as e:
        print(e)
        return None
    
def get_student(id):
    return Student.query.get(id)

def get_student_by_username(username):
    result = db.session.execute(db.select(Student).filter_by(username=username))
    return result.scalar_one_or_none()

def is_student(id):
    return Student.query.get(id) != None

def get_all_student():
    return Student.query.all()