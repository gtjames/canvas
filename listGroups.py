import canvas

single = "0";

# Main code
def listTeamMembers():
    single = input("(1) Solo, (0) All, (u) Unassigned: ")
    cnt = 0;
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

                if (group['members_count'] == 1 and single == "1") or single == "0":
                    cnt = canvas.listMembers(group) + cnt
            print(f"Members: {cnt}")

def studentInTeam():
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
                students.append({"name": member["name"], "first": firstName, "last": lastName, "id": member["id"], "login": lastLogin.replace('T', ' ')[5:16], "group": group["name"][:7]})
    sortBy = input("Sort By (first, last, group, login): ")
    group = ""
    while len(sortBy) > 0:
        students = canvas.sortByAttr(students, sortBy)
        for student in students:
            if sortBy == "group":     #   group
                if group != student["group"]:       #   did the group change?
                    print(f"{student["group"]}")    #   print the group name
                group = student["group"]            #   save current group
                canvas.showStudent(student['id'], student["name"])
                # activity  = getTotalActivityTime(student["id"])    {activity}
                # print(f"    {student["first"].ljust(10)[:10]} {student["last"].ljust(15)[:15]} - {lastLogin}")
            else:
                print(f"{student["first"]} {student["last"]} : {student["group"]} : {student["login"]}")
        sortBy = input("Sort By (first, last, group, login): ")
