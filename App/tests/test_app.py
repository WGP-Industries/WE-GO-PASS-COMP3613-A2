import os, tempfile, pytest, logging, unittest
from unittest.mock import patch, MagicMock
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user,
    get_student_shortlisted_positions,
    list_shortlisted_students
)


LOGGER = logging.getLogger(__name__)

'''
   Unit Tests
'''
class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"

    # pure function no side effects or integrations called
    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)

class ShortlistUnitTests(unittest.TestCase):

    @patch('App.controllers.shortlist.Shortlist')
    def test_get_student_shortlisted_postions(self, mock_shortlist):

        mock_shortlist.query.filter_by.return_value.all.return_value =[
            MagicMock(internship_id=1, id=1),
            MagicMock(internship_id=2, id=2),
        ]

        with patch('App.controllers.shortlist.Internship') as mock_internship:
            mock_internship.query.get.side_effect = [
                MagicMock(id=1, title = 'internship 1',description = 'Description 1', status = 'pending', employer_id = 100),
                MagicMock(id=2, title = 'internship 2',description = 'Description 2', status = 'pending', employer_id = 100)
            ]

            results = get_student_shortlisted_positions(5)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['title'], 'Internship 1')
        self.assertEqual(results[1]['internship_id'], 2)



'''
    Integration Tests
'''

# This fixture creates an empty database for the test and deletes it after the test
# scope="class" would execute the fixture once and resued for all methods in the class
@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)

    # Tests data changes in the database
    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"


    # Test creating users
    def test_create_staff(self):
        staff = create_staff("staff1", "staff1pass")
        assert staff.username == "staff1"

    def test_create_student(self):
        student = create_student("student1", "student1pass")
        assert student.username == "student1"

    def test_create_employer(self):
        employer = create_student("employer1", "employer1pass")
        assert employer.username == "employer1"

    # Internship testing
    def test_create_internship(self):
        employer = create_employer("employer1", "pass", "Company1")
        assert employer.username == "employer1"
        internship = create_internship("Internship1", "Test i guess", employer.id)
        assert internship is not None
        assert internship.title == "Internship1"

    # Add student to a shortlist
    def test_add_student_to_shortlist_and_get_positions(self):
        internship_owner = create_employer("employer2", "employerpass", "Company2")
        internship = create_internship("Test Intern 2", "Test i guess", internship_owner.id)
        staff = create_staff("Staff2", "staffpass")
        student = create_student("short_student_a", "studentpass")
        shortlist = add_student_to_shortlist(student.id, internship.id)
        assert shortlist is not None
        positions = get_student_shortlisted_positions(student.id)
        assert isinstance(positions, list)
        assert any(p['internship_id'] == internship.id for p in positions)

    #Accept and Reject a Student from the shortlist
    def test_accept_student_from_shortlist(self):
        emp = create_employer("employer_accept", "pass", "Company3")
        internship = create_internship("Accept.Co", "accept i guess", emp.id)
        student = create_student("student_accept", "pass")
        shortlist = add_student_to_shortlist(student.id, internship.id)
        assert shortlist is not None
        check = accept_student_from_shortlist(shortlist.id)
        assert check is True
        refreshed = get_internship(internship.id)
        assert refreshed.status == 'accepted'

    def test_reject_student_from_shortlist(self):
        emp = create_employer("employer_reject", "pass", "Company4")
        internship = create_internship("Reject.Co", "reject i guess", emp.id)
        student = create_student("student_reject", "pass")
        shortlist = add_student_to_shortlist(student.id, internship.id)
        assert shortlist is not None
        check = reject_student_from_shortlist(shortlist.id)
        assert check is True
        refreshed = get_internship(internship.id)
        assert refreshed.status == 'rejected'







