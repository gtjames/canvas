import canvas
import requests

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
    for course in courses:
        groups = canvas.getGroups(course['id'])
        for group in groups:
            if group['members_count'] == 0:
                continue
            members = canvas.getGroupMembers(group['id'])
            for member in members:
                lastName, rest = member['sortable_name'].split(", ")
                firstName = rest.split(" ")[0]
                students.append({"name": member["name"], "first": firstName, "last": lastName, "id": member["id"], "group": group["name"]})
    sortBy = input("Sort By (first, last, group): ")
    group = ""
    while len(sortBy) > 0:
        students = canvas.sortByAttr(students, sortBy)
        for student in students:
            if sortBy == "first":       #   first
                print(f"{student["first"].ljust(10)[:10]} {student["last"].ljust(15)[:15]} : {student["group"]}")
            elif sortBy == "last":      #   last
                print(f"{student["last"].ljust(15)[:15]} {student["first"].ljust(10)[:10]} : {student["group"]}")
            elif sortBy == "group":     #   group
                if group != student["group"]:       #   did the group change?
                    print(f"{student["group"]}")    #   print the group name
                lastLogin = getLastLogin(student["id"])
                canvas.showStudent(student['id'], student["name"])
                # activity  = getTotalActivityTime(student["id"])    {activity}
                # print(f"    {student["first"].ljust(10)[:10]} {student["last"].ljust(15)[:15]} - {lastLogin}")
                group = student["group"]            #   save current group
        sortBy = input("Sort By (first, last, group): ")

# Get Last Login
def getLastLogin(studentId):
    params = { "include[]": "last_login" }
    response = requests.get(f"{canvas.canvasURL}/users/{studentId}", headers=canvas.headers, params=params)
    userStats = response.json()
    return userStats["last_login"]

# Get Total Activity Time
def getTotalActivityTime(studentId):
    response = requests.get(f"{canvas.canvasURL}/courses/{canvas.courseId}/users/{studentId}", headers=canvas.headers)
    stats = response.json()
    activityTime = stats.get("total_activity_time", "N/A")
    return activityTime
# total_activity_time = analytics_data.get("total_activity_time", "N/A")
