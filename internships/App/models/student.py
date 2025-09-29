from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db

class Student(db.Model):
    __tablename__ = "student"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)

#    shortlists = db.relationship("Shortlist", backref="student", lazy=True)

    def __init__(self, username, password, name):
        self.username = username
        self.set_password(password)
        self.name = name
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Student {self.name}>'
    
        