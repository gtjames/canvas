import sys
import canvas

single = "0";

# Main code
def listTeamMembers():
    single = input("(1) Solo, (0) All, (u) Unassigned: ")

    courses = canvas.getCategories(canvas.courseId)
    for course in courses:
        print(f"{course['name']} (ID: {course['id']})")
        # if we are only interestin 'U'nassigned this is the route to take
        if single == "u":
            members = canvas.getUnassigned(course['id'])
            for member in members:
                canvas.showStudent(member['id'], member["name"])
            print(f"{len(members)} - unassigned")
        else:
            # if we want the group membership this is the place
            groups = canvas.getGroups(course['id'])
            for group in groups:
                if group['members_count'] == 0:
                    continue

                if (group['members_count'] <= 2 and single == "1") or single == "0":
                    canvas.listMembers(group)
