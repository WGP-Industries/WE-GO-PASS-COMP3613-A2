import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import ( User, Staff, Student, Employer, Internship, Shortlist)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize, 
                             create_staff, get_all_staff,
                             create_student, get_all_student,
                             create_employer, get_all_employer,
                             create_internship, get_all_internship,
                             get_student_shortlisted_positions, add_student_to_shortlist, reject_student_from_shortlist, accept_student_from_shortlist) 


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Staff Commands
'''

staff_cli = AppGroup('staff', help='Staff object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@staff_cli.command("create", help="Creates a staff user")
@click.argument("username", default="alice")
@click.argument("password", default="alicepass")
def create_user_command(username, password):
    create_staff(username, password)
    print(f'{username} created!')


@staff_cli.command("list", help="Lists the staff in the database")
def list_user_command():
    print(get_all_staff())


app.cli.add_command(staff_cli) # add the group to the cli


'''
Student Commands
'''

student_cli = AppGroup('student', help='student object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@student_cli.command("create", help="Creates a student user")
@click.argument("username", default="john")
@click.argument("password", default="johnpass")
def create_user_command(username, password):
    create_student(username, password)
    print(f'{username} created!')


@student_cli.command("list", help="Lists the students in the database")
def list_user_command():
    print(get_all_student())


app.cli.add_command(student_cli) # add the group to the cli


'''
Employer Commands
'''

employer_cli = AppGroup('employer', help='employer object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@employer_cli.command("create", help="Creates a employer user")
@click.argument("username", default="sam")
@click.argument("password", default="Sampass")
def create_user_command(username, password):
    create_employer(username, password)
    print(f'{username} created!')


@employer_cli.command("list", help="Lists the employers in the database")
def list_user_command():
    print(get_all_employer())


app.cli.add_command(employer_cli) # add the group to the cli



'''
Internship Commands
'''

internship_cli = AppGroup('internship', help='internship object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@internship_cli.command("create", help="Creates a internship object")
@click.argument("title", default="software dev")
@click.argument("description", default="software developer")
@click.argument("employer_id", default=1)
def create_user_command(title, description, employer_id):
    create_internship(title, description, employer_id)
    print(f'{title} created!')


@internship_cli.command("list", help="Lists the internships in the database")
def list_user_command():
    print(get_all_internship())


app.cli.add_command(internship_cli) # add the group to the cli


'''
Shortlist Commands
'''

shortlist_cli = AppGroup('shortlist', help='shortlist object commands') 

@shortlist_cli.command("view", help="View shortlisted positions and employer responses for a student")
@click.argument("student_id", type=int)
def view_shortlisted_positions(student_id):
    results = get_student_shortlisted_positions(student_id)
    if not results:
        print(f"No shortlisted positions found for student {student_id}.")
    else:
        for r in results:
            print(f"Internship ID: {r['internship_id']}, Title: {r['title']}, Status: {r['status']}")

@shortlist_cli.command("add", help="Add a student to an internship's shortlist")
@click.argument("student_id", type=int)
@click.argument("internship_id", type=int)
def add_student_shortlist(student_id, internship_id):
    result = add_student_to_shortlist(student_id, internship_id)
    if result:
        print(f"Student {student_id} added to internship {internship_id} shortlist.")
    else:
        print(f"Failed to add student {student_id} to internship {internship_id} shortlist.")

@shortlist_cli.command("accept", help="Employer accepts a student from shortlist (by shortlist_id)")
@click.argument("shortlist_id", type=int)
def accept_student(shortlist_id):
    if accept_student_from_shortlist(shortlist_id):
        print(f"Shortlist entry {shortlist_id} accepted.")
    else:
        print(f"Failed to accept shortlist entry {shortlist_id}.")

@shortlist_cli.command("reject", help="Employer rejects a student from shortlist (by shortlist_id)")
@click.argument("shortlist_id", type=int)
def reject_student(shortlist_id):
    if reject_student_from_shortlist(shortlist_id):
        print(f"Shortlist entry {shortlist_id} rejected.")
    else:
        print(f"Failed to reject shortlist entry {shortlist_id}.")


app.cli.add_command(shortlist_cli) # add the group to the cli


'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)