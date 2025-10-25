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
    create_student,
    create_staff,
    create_employer,
    create_internship,
    get_student_shortlisted_positions,
    list_shortlisted_students,
    add_student_to_shortlist,
    accept_student_from_shortlist,
    reject_student_from_shortlist,
    get_internship
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

class StudentUnitTests(unittest.TestCase):

    @patch('App.controllers.student.db')
    @patch('App.controllers.student.Student')
    def test_create_student_success(self, mock_student, mock_db):
        mock_student.return_value = MagicMock(username='stud1')
        mock_db.session.add.return_value = None
        mock_db.session.commit.return_value = None

        result = create_student('stud1', 'pass')

        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'stud1')

class StaffUnitTests(unittest.TestCase):

    @patch('App.controllers.staff.db')
    @patch('App.controllers.staff.Staff')
    def test_create_staff_success(self, mock_staff, mock_db):
        mock_staff.return_value = MagicMock(username='staff1')
        mock_db.session.add.return_value = None
        mock_db.session.commit.return_value = None

        result = create_staff('staff1', 'pass')

        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'staff1')

class EmployerUnitTests(unittest.TestCase):

    @patch('App.controllers.employer.db')
    @patch('App.controllers.employer.Employer')
    def test_create_employer_success(self, mock_employer, mock_db):
        mock_employer.return_value = MagicMock(username='emp1', company='TechCorp')
        employer = mock_employer(username='emp1', password='123', company='TechCorp')
        mock_db.session.add.return_value = None
        mock_db.session.commit.return_value = None

        result = create_employer('emp1', '123', 'TechCorp')

        self.assertIsNotNone(result)
        self.assertEqual(result.username, 'emp1')
        self.assertEqual(result.company, 'TechCorp')

class InternshipUnitTests(unittest.TestCase):

    @patch('App.controllers.internship.db')
    @patch('App.controllers.internship.Internship')
    def test_create_internship_success(self, mock_internship, mock_db):
        mock_internship.return_value = MagicMock(title='Intern1', employer_id=1)
        mock_db.session.execute.return_value.scalar_one_or_none.return_value = None

        result = create_internship('Intern1', 'Test desc', 1)

        self.assertIsNotNone(result)
        self.assertEqual(result.title, 'Intern1')

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
        self.assertEqual(results[0]['title'], 'internship 1')
        self.assertEqual(results[1]['internship_id'], 2)

    @patch('App.controllers.shortlist.Shortlist')
    def test_list_shortlisted_students(self, mock_shortlist):
        
        mock_shortlist.query.filter_by.return_value.all.return_value = [
            MagicMock(student_id=1, id=10, internship_id=101),
            MagicMock(student_id=2, id=11, internship_id=102)
        ]

        with patch('App.controllers.shortlist.Student') as mock_student, patch('App.controllers.shortlist.Internship') as mock_internship:

            mock_student.query.get.side_effect = [
                MagicMock(id=1, username='john', **{'name': 'John Doe'}),
                MagicMock(id=2, username='jane', **{'name': 'Jane Doe'})
            ]

            mock_internship.query.get.side_effect = [
                MagicMock(id=101, title='Internship 1', employer_id=100),
                MagicMock(id=102, title='Internship 2', employer_id=101)
            ]

            results = list_shortlisted_students(20)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]['username'], 'john')
        self.assertEqual(results[0]['employer_id'], 100)
        self.assertEqual(results[0]['internship_title'], 'Internship 1')
        self.assertEqual(results[1]['name'], 'Jane Doe')
        self.assertEqual(results[1]['employer_id'], 101)
        self.assertEqual(results[1]['internship_title'], 'Internship 2')

    @patch('App.controllers.shortlist.db')
    @patch('App.controllers.shortlist.Shortlist')
    def test_add_student_to_shortlist_success(self, mock_shortlist, mock_db):
        mock_shortlist.return_value = MagicMock(student_id=1, internship_id=2)
        mock_db.session.execute.return_value.scalar_one_or_none.return_value = None

        result = add_student_to_shortlist(1, 2)

        self.assertIsNotNone(result)
        self.assertEqual(result.student_id, 1)

    @patch('App.controllers.shortlist.db')
    @patch('App.controllers.shortlist.Shortlist')
    def test_add_student_to_shortlist_already_exists(self, mock_shortlist, mock_db):
        mock_db.session.execute.return_value.scalar_one_or_none.return_value = True

        result = add_student_to_shortlist(1, 2)

        self.assertIsNone(result)

    @patch('App.controllers.shortlist.db')
    @patch('App.controllers.shortlist.Internship')
    @patch('App.controllers.shortlist.Shortlist')

    def test_accept_student_from_shortlist_success(self, mock_shortlist, mock_internship, mock_db):
        mock_shortlist.query.get.return_value = MagicMock(internship_id=1)
        mock_internship.query.get.return_value = MagicMock(accept=MagicMock())

        result = accept_student_from_shortlist(1)

        self.assertTrue(result)
        mock_internship.query.get.return_value.accept.assert_called_once()
        mock_db.session.commit.assert_called_once()

    @patch('App.controllers.shortlist.db')
    @patch('App.controllers.shortlist.Internship')
    @patch('App.controllers.shortlist.Shortlist')
    def test_reject_student_from_shortlist_success(self, mock_shortlist, mock_internship, mock_db):
        mock_shortlist.query.get.return_value = MagicMock(internship_id=1)
        mock_internship.query.get.return_value = MagicMock(reject=MagicMock())

        result = reject_student_from_shortlist(1)

        self.assertTrue(result)
        mock_internship.query.get.return_value.reject.assert_called_once()
        mock_db.session.commit.assert_called_once()

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








