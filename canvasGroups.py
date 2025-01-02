import requests
import sys
import canvas

courseId = "320100"
school = "byui"
single = "0";

# Run the function
if len(sys.argv) > 2:
    school   = sys.argv[1]
    courseId = sys.argv[2]
if len(sys.argv) > 3:
    single = sys.argv[3]

canvas.setSchool(school)

# Get details on a student
def getStudent(studentId, member):
    try:
        student= canvas.getStudent(studentId)
        # Get the last and first names
        lastName, rest = student['sortable_name'].split(", ")
        firstName = rest.split(" ")[0]
        # - {st['time_zone'].ljust(15)[:15]} 
        print(f"\t- {firstName.ljust(10)[:10]} {lastName.ljust(15)} {student['primary_email']} - {student['time_zone'].ljust(15)[:15]} ")

    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"\t- {member["name"]} has dropped the course")

# Main code
def listTeamMembers(courseId):
    courses = canvas.getCategories(courseId)
    for course in courses:
        print(f"{course['name']} (ID: {course['id']})")
        # if we are only interestin 'U'nassigned this is the route to take
        if single == "u":
            canvas.getUnassignedMbr(course['id'])
            break

        groups = canvas.getGroups(course['id'])
        for group in groups:
            if group['members_count'] == 0:
                continue

            if (group['members_count'] == 1 and single == "1") or single == "0":
                canvas.listMembers(group)

listTeamMembers(courseId)
