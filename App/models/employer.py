from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .internship import Internship

class Employer(db.Model):
    __tablename__ = "employer"
    
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(256), nullable=False)

#    internships = db.relationship("Internship", backref="employer", lazy=True)

    def __init__(self, username, password, company):
        self.username = username
        self.set_password(password)
        self.company = company
    
    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)
    
    def __repr__(self):
        return f'<Employer {self.company}>'
    