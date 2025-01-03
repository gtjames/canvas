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
else:
    school   = input("Enter School: ")
    courseId = input("Enter Course: ")

if len(sys.argv) > 3:
    single = sys.argv[3]

canvas.setSchool(school)

# Main code
def listTeamMembers(courseId):
    courses = canvas.getCategories(courseId)
    for course in courses:
        print(f"{course['name']} (ID: {course['id']})")
        # if we are only interestin 'U'nassigned this is the route to take
        if single == "u":
            members = canvas.getUnassigned(course['id'])
            for member in members:
                canvas.showStudent(member['id'], member["name"])
            break

        # if we want the group membership this is the place
        groups = canvas.getGroups(course['id'])
        for group in groups:
            if group['members_count'] == 0:
                continue

            if (group['members_count'] == 1 and single == "1") or single == "0":
                canvas.listMembers(group)

listTeamMembers(courseId)
