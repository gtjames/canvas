import canvas

# Main code
def listTeamMembers():
    grpType = input("(1) Solo, (0) All, (u) Unassigned: ")
    while len(grpType) > 0:
        cnt = 0;
        courses = canvas.getCategories(canvas.courseId)
        for course in courses:
            print(f"{course['name']}")
            # if we are only interestin 'U'nassigned this is the route to take
            if grpType == "u":
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

                    if (group['members_count'] == 1 and grpType == "1") or grpType == "0":
                        cnt = canvas.listMembers(group) + cnt
                print(f"Members: {cnt}")
        grpType = input("(1) Solo, (0) All, (u) Unassigned: ")

def studentInTeam():
    print(f"{canvas.color[canvas.courseId]}")
    students=[]
    courses = canvas.getCategories(canvas.courseId)
    # studentsInCourse = canvas.getStudents(canvas.courseId)    ATTN:  remember this

    for course in courses:
        groups = canvas.getGroups(course['id'])
        for group in groups:
            if group['members_count'] == 0:
                continue

            members = canvas.getGroupMembers(group['id'])
            for member in members:
                lastName, rest = member['sortable_name'].split(", ")
                firstName = rest.split(" ")[0].ljust(10)[:10]
                lastName = lastName.ljust(15)[:15]
                lastLogin = canvas.getLastLogin(member["id"])
                student = canvas.getStudent(member["id"])
                students.append({"name": member["name"], "first": firstName, "last": lastName, "id": member["id"], 
                                 "login": lastLogin.replace('T', ' ')[5:16], "group": group["name"][:7],
                                 "email": student['primary_email'].ljust(30), "tz": student['time_zone'].ljust(15)[:15]})
    sortBy = input("Sort By (first, last, group, login): ")
    group = ""
    while len(sortBy) > 0:
        students = canvas.sortByAttr(students, sortBy)
        for student in students:
            if sortBy == "group":     #   group
                if group != student["group"]:       #   did the group change?
                    print(f"\t\t{student["group"]}")    #   print the group name
                group = student["group"]            #   save current group
                print(f"{student["first"]} {student["last"]} : {student["email"]} : {student["tz"]}")
            else:
                print(f"{student["first"]} {student["last"]} : {student["group"]} : {student["login"]} : {student["tz"]}")
        sortBy = input("Sort By (first, last, group, login, tz): ")
