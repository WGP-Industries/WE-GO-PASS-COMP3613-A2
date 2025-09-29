## CLI Commands

```bash
$ flask init
```
## Create Student, Staff, Employer
```bash
$ flask staff create <username> <password>

$ flask student create <username> <password>

$ flask employer create <username> <password>
```

## Create Student, Staff, Employer
```bash
$ flask staff list

$ flask student list

$ flask employer list
```

## Create Internship and List
```bash
$ flask internship create <title> <description> <employer_id>

$ flask internship list
```

## Add a student to an internship's shortlist
```bash
$ flask shortlist add <student_id> <internship_id>
```

## View shortlisted positions for a student:
```bash
$ flask shortlist view <student_id>
```

## Accept and Reject a student from shortlist
```bash
$ flask shortlist accept <shortlist_id>

$ flask shortlist reject <shortlist_id>
