from .user import create_user
from .staff import create_staff
from .student import create_student
from .employer import create_employer
from .internship import create_internship
from App.database import db


def initialize():
    db.drop_all()
    db.create_all()
    create_user('bob', 'bobpass')
    create_staff('staff1', 'staffpass')
    create_staff('staff2', 'staffpass2')
    create_staff('staff3', 'staffpass3')
    create_staff('staff4', 'staffpass4')
    create_staff('staff5', 'staffpass5')

    create_student('student1', 'studentpass')
    create_student('student2', 'studentpass2')
    create_student('student3', 'studentpass3')
    create_student('student4', 'studentpass4')
    create_student('student5', 'studentpass5')
    
    create_employer('employer1', 'employerpass', 'Company Inc')
    create_employer('employer2', 'employerpass2', 'Business LLC')
    create_employer('employer3', 'employerpass3', 'Enterprise Ltd')
    create_employer('employer4', 'employerpass4', 'Startup Co')
    create_employer('employer5', 'employerpass5', 'Tech Corp')

    create_internship('Software Engineer Intern', 'Work on developing software solutions.', 1)
    create_internship('Data Analyst Intern', 'Analyze data and generate reports.', 2)
    create_internship('Marketing Intern', 'Assist in marketing campaigns and strategies.', 3)
    create_internship('Product Management Intern', 'Support product managers in their tasks.', 4)
    create_internship('UX/UI Design Intern', 'Help design user interfaces and experiences.', 5)