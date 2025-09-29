from App.database import db

class Internship(db.Model):
    __tablename__ = "internship"
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)

    shortlists = db.relationship("Shortlist", backref="internship", lazy=True)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'), nullable=False)

    status = db.Column(db.String(20), default="pending")

    def accept(self):
        self.status = "accepted"

    def reject(self):
        self.status = "rejected"

    def __init__(self, title, description, employer_id=None):
        self.title = title
        self.description = description
        if employer_id:
            self.employer_id = employer_id

    def __repr__(self):
        return f'<Internship {self.title} employer_id: {self.employer_id}>'
         