from App.database import db
from App.models.internship import Internship

class Shortlist(db.Model):
    __tablename__ = "shortlist"
    
    id = db.Column(db.Integer, primary_key=True)
    
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    internship_id = db.Column(db.Integer, db.ForeignKey('internship.id'), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    def __init__(self, student_id, internship_id, employer_id):
        self.student_id = student_id
        self.internship_id = internship_id
        self.employer_id = employer_id

    def __repr__(self):
        return f'<Shortlist Student ID: {self.student_id}, Internship ID: {self.internship_id}>'
    
