import sys
import requests
import json
from utilities import sendMessage, sortByAttr, getCanvasData
from datetime import datetime, timezone, timedelta

school   = ""
courseId  = ""
canvasURL = ""      # attn: 
headers   = ""      # attn: 

_announcements = {}
_assignments   = {}
_categories    = {}
_enrollments   = {}         #   the whole works which we do not need
_groupMembers  = {}
_groups        = {}
_lastLogin     = {}
_studentEnrollment  = {}    #   just the few details we need
_students      = {}
_submissionByStatus = {}
_unassigned    = {}

def clearCache():
    global _announcements
    global _assignments
    global _categories
    global _enrollments
    global _groupMembers
    global _groups
    global _lastLogin
    global _studentEnrollment
    global _students
    global _submissionByStatus
    global _unassigned

    _announcements = {}
    _assignments = {}
    _categories = {}
    _enrollments   = {}
    _groupMembers = {}
    _groups = {}
    _lastLogin = {}
    _studentEnrollment  = {}
    _students = {}
    _submissionByStatus = {}
    _unassigned = {}

def setParams():
    global school
    global courseId
    if (len(school) == 0 and len(sys.argv) > 1):
        courseId = sys.argv[1]
    else:
        school   = input("Enter School: ")
        courseId = input("Enter Course: ")
    school   = "byupw" if school   == "" else school
    courseId = "7113"  if courseId == "" else courseId

    setSchool(school)
    return courseId

# Canvas API details
def setSchool(school):
    global canvasURL
    global headers

    canvasURL = f"https://{school}.instructure.com/api/v1"

    # Load the JSON key file
    with open('keys.json', 'r') as file:
        data = json.load(file)

    headers = { "Authorization": f"Bearer {data[f"{school}"]}" }

def startUp():
    getAnnouncements(courseId)      #   _announcements
    getAssignments  (courseId)      #   _assignments
    getCategories   (courseId)      #   _categories
    list = getStudents     (courseId)      #   _students
    getEnrollments  (courseId, list)      #   _enrollments        _studentEnrollment
    getGroups       (1706)          #   _groups
                                    #  _groupMembers  = {}
                                    #  _lastLogin     = {}
    # getSubmissionByStatus(courseId, 4205, 'unsubmitted')      _submissionByStatus
    # getUnfinishedAssignments(courseId)
    getUnassigned   (1706)          #   _unassigned

def getAnnouncements(courseId):
    global _announcements

    if courseId not in _announcements:
        _announcements[courseId] = getCanvasData(f"{canvasURL}/courses/{courseId}/discussion_topics?only_announcements=true", params={"per_page": 100})
    return _announcements[courseId]

def listAnnouncements():
    announcements = getAnnouncements(courseId)
    for announcement in announcements:
        print(f"{announcement['id']}  {announcement['title']}")

def getAssignments(courseId):
    global _assignments
    
    if courseId not in _assignments:
        response = requests.get(f"{canvasURL}/courses/{courseId}/assignments", headers=headers, params={"per_page": 100})
        _assignments[courseId] = response.json()
    return _assignments[courseId]

def getStudents(courseId):
    global _students

    if courseId not in _students:
        params = {
            "enrollment_type[]": "student",
            "per_page": 100,  # Maximum allowed per page
        }
        response = requests.get(f"{canvasURL}/courses/{courseId}/users", headers=headers, params=params)
        _students[courseId] = response.json()
        for student in _students[courseId]:
            lastName, rest = student['sortable_name'].split(", ")
            firstName = rest.split(" ")[0].ljust(10)[:10]
            student['first'] = firstName.ljust(10)[:10]
            student['last']  = lastName.ljust(15)[:15]
            student['email'] = student['email'].ljust(30)
            student['group'] = "Team XX"
            student['lastLogin'] = "2025-01-01T01:00:00-06:00"
            student['login'] = "01-01 01:00"
            student['score'] = 0
            student['grade'] = 'F'
            student['tz']    = "Not Set"
            student['activityTime'] = 0
    return _students[courseId]

def getStudent(studentId):
    global _students

    if studentId not in _students:
        response = requests.get( f"{canvasURL}/users/{studentId}/profile", headers=headers )
        _students[studentId] = response.json()
    return _students[studentId]

# Get details on a student
def showStudent(studentId, name):
    try:
        student = getStudent(studentId)
        # Get the last and first names
        lastName, rest = student['sortable_name'].split(", ")
        firstName = rest.split(" ")[0]
        print(f"    - {firstName.ljust(10)[:10]} {lastName.ljust(15)} {student['primary_email'].ljust(30)} - {student['time_zone'].ljust(15)[:15]} ")
    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"    - {name} has dropped the course")

# Get group categories
def getCategories(courseId):
    global _categories

    studentList = getStudents(courseId)

    if courseId not in _categories:
        response = requests.get( f"{canvasURL}/courses/{courseId}/group_categories", headers=headers )
        _categories[courseId] = response.json()

        for category in _categories[courseId]:
            if category['name'] == "Who is Here":
                continue
            groups = getGroups(category['id'])
            for group in groups:
                if group['members_count'] == 0:
                    continue

                members = getGroupMembers(0+group['id'])
                for member in members:
                    student   = getStudent(member["id"])
                    tz = student['time_zone'].ljust(15)[:15]
                    lastLogin = getLastLogin(member["id"])
                    lastLogin = lastLogin if lastLogin else "2025-01-01T01:00:00-06:00"
                    
                    student = next((student for student in studentList if student["id"] == member["id"]), None)

                    student["lastLogin"] = lastLogin
                    student["login"]     = lastLogin.replace('T', ' ')[5:16]
                    student["group"]     = group["name"][:7] 
                    student["tz"]        = tz
                    

    return _categories[courseId]

# Get members not in a group
def getUnassigned(groupId):
    global _unassigned

    if groupId not in _unassigned:
        params = { "per_page": 100 }  # Maximum allowed per page 
        response = requests.get( f"{canvasURL}/group_categories/{groupId}/users?unassigned=true&per_page=20", headers=headers, params=params )
        _unassigned[groupId] = response.json()
    return _unassigned[groupId]

def listTeamMembers():
    categories = getCategories(courseId)
    grpType = input("(1) Solo, (0) All, (u) Unassigned: ")
    while len(grpType) > 0:
        cnt = 0;
        for category in categories:
            if category['name'] == "Who is Here":
                continue
            print(f"{category['name']}")
            # if we are only interestin 'U'nassigned this is the route to take
            if grpType == "u":
                members = getUnassigned(category['id'])
                for member in members:
                    showStudent(member['id'], member["name"])
                print(f"{len(members)} - unassigned")
                if input("Email the Unassigned?: ") == 'y':
                    studentIds = [student['id'] for student in members]
                    sendMessage(studentIds, "You have not yet found a team", "Please identify a team that works for your schedule and add your name to the group")
            else:
                # if we want the group membership this is the place
                groups = getGroups(category['id'])
                for group in groups:
                    if group['members_count'] == 0:
                        continue

                    if (group['members_count'] == 1 and grpType == "1") or grpType == "0":
                        cnt = listMembers(group, grpType) + cnt
                print(f"Members: {cnt}")
        grpType = input("(1) Solo, (0) All, (u) Unassigned: ")

# Get Last Login
def getEnrollments(courseId, studentList):
    global _enrollments
    global _studentEnrollment

    if courseId not in _enrollments:
        response = requests.get(f"{canvasURL}/courses/{courseId}/enrollments?type[]=StudentEnrollment", headers=headers, params={"per_page": 100})

        _enrollments[courseId] = response.json()
        
        _studentEnrollment = {}
        _studentEnrollment[courseId] = {
            student['user_id']: {
                "lastActivity": student['last_activity_at'],
                "activityTime": student['total_activity_time'],
                "grade":        student['grades']['current_grade'],
                "score":        student['grades']['current_score'],
        } 
        for student in _enrollments[courseId]}

            # Merge data by adding enrollment details to matching students
        for student in studentList:
            id = student.get('id')
            if id in _studentEnrollment[courseId]:
                student["lastActivity"] = _studentEnrollment[courseId][id]["lastActivity"]
                student["activityTime"] = _studentEnrollment[courseId][id]["activityTime"]
                student["grade"]        = _studentEnrollment[courseId][id]["grade"]
                student["score"]        = _studentEnrollment[courseId][id]["score"]

    return _studentEnrollment[courseId]

def studentInTeam():
    studentList = getStudents(courseId)
    getEnrollments(courseId, studentList)   #  merge enrollemnt data with studentList
    getCategories(courseId)    #  merge group data with studentList

    notifyNoneParticipating = False
    if input("Email Non Participating?: ") == 'y':
        notifyNoneParticipating = True

    group = ""
    sortBy = input("Sort By (first, last, group, login, tz, email, id): ")
    size = 0
    while len(sortBy) > 0:
        students = sortByAttr(studentList, sortBy)
        for student in students:
            if sortBy == "group":                       #   sorting by group
                if group != student["group"]:           #   did the group change?
                    if size > 0:                        #   if so, print the group size
                        print(f"Members in Group {size}")
                    print(f"\t\t{student["group"]}")    #   print the group name
                    group = student["group"]            #   save current group
                    size = 0                            #   reset the group size
                size += 1                               #   increment the group size
                print(f"{student["first"]} {student["last"]} : {student["login"]} : {student["email"]} : {student["tz"]}")
            elif sortBy == "login":
                print(f"{student["first"]} {student["last"]} : {student["login"]} : {student["group"]} : {student["tz"]}");
                lastLogin = datetime.fromisoformat(student["lastLogin"])
                aWeekAgo = datetime.now(lastLogin.tzinfo) - timedelta(days=7)
                if lastLogin < aWeekAgo and notifyNoneParticipating:
                    sendMessage([student["id"]], "You have not participated in the class this week",
                        "Please let me know if you are having trouble with the class")
            elif sortBy == "id":
                print(f"{student["first"]} {student["last"]} : {student["login"]} : {student["email"]} : {student["id"]}");
            elif sortBy == "score":
                print(f"{student["first"]} {student["last"]} : {student["score"]} : {student["grade"]} : {student["activityTime"]}");
            elif sortBy == "first" or sortBy == "tz":
                print(f"{student["first"]} {student["last"]} : {student["group"]} : {student["email"]} : {student["tz"]}")
            else:
                print(f"{student["first"]} {student["last"]} : {student["email"]} : {student["id"]}")
        sortBy = input("Sort By (first, last, group, login, tz, email, id): ")

def studentsInClass():
    studentList = getStudents(courseId)

    sortBy = input("Sort By (first, last, email, id): ")
    while len(sortBy) > 0:
        students = sortByAttr(studentList, sortBy)
        for student in students:
            print(f"{student["first"]} {student["last"]} : {student["email"]} : {student["id"]}")
        sortBy = input("Sort By (first, last, email, id): ")

# traverse from the categories in a course to the groups to the members
def listMembers(group, grpType):
    print(f"{group['name']} # in Group: {group['members_count']} ")
    members = getGroupMembers(group['id'])
    studentIds = [student['id'] for student in members]
    for member in members:
        showStudent(member['id'], member["name"])
    if len(members) == 1 and grpType == "1":
        if input("Email Lonely People?: ") == 'y':
            sendMessage(studentIds, "You are currently the only member of the team", 
                                "Please identify a team that has others enrolled already that works for your schedule and add your name to the group")            
    if grpType == "0" and input("Email Class?: ") == 'y':
        subject = input("Subject: ")
        body    = input("What do you want to say?: ")
        sendMessage(studentIds, subject, body)
        
    return len(members)

# Get all groups within the specified group category
def getGroups(catId):
    global _groups

    if catId not in _groups:
        response = requests.get( f"{canvasURL}/group_categories/{catId}/groups?per_page=70", headers=headers )
        _groups[catId] = response.json()
    return _groups[catId]

# Get members in each group
def getGroupMembers(groupId):
    global _groupMembers

    if groupId not in _groupMembers:
        response = requests.get( f"{canvasURL}/groups/{groupId}/users?per_page=70", headers=headers )
        _groupMembers[groupId] = response.json()
    return _groupMembers[groupId]

def sendStatusLetters():
    status = getEnrollments()
    unfinishedAssignments = getUnfinishedAssignments(courseId)
    statusLetter(status, 90, 101, unfinishedAssignments,
                 "Keep up the good work!: Current Score: ",
                "\nYou are doing very well in the class keep up the good work")
    statusLetter(status, 70, 90, unfinishedAssignments,
                "You are doing well but might be missing a few assignments: Current Score: ",
                "\nYou can still turn these in until the end of week four")
    statusLetter(status, 0, 70, unfinishedAssignments,
                 "How are you doing in the class? It looks like you are struggling: Current Score: ",
                "\nHere is a list of your missing assignments. You can still turn these in until the end of week four\nDon't forget there is tutoring available for the class.")

def statusLetter(status, lo, hi, unfinishedAssignments, subject, body):
    list = [ student for student in status if lo <= int(student["currentScore"] or 0) < hi ]

    go = input("go/no go? ")

    for s in list:
        print(f"{s.get('currentScore', 0):6.1f} - {s.get('name')} {" dropped" if s.get('id') not in unfinishedAssignments else ""}")

        # Check if the student ID is in the unfinishedAssignments dictionary
        if s.get('id') not in unfinishedAssignments or go != 'go':
            continue

        missed = "\n\t".join(map(str,unfinishedAssignments[s.get('id')].get('unsubmitted')))

        sendMessage([s['id']],  f"{subject} {s.get('currentScore')}",
                                f"\n{s.get('firstName')},\n{body}\nMissing Assignments(if any)\n\t{missed}\n\nBro. James")

def listUnsubmitted():
    unfinishedAssignments = getUnfinishedAssignments(courseId)
    studentIds = set()

    notify = input("Notify?: ")
    msg = input("Message?: ")
    msg = msg if msg else "\tThe Following assignments have not been submitted.\n\tThese can all be submitted up to the end of Week 4."

    for studentId, info in unfinishedAssignments.items():
        if info['unsubmitted']:
            studentIds.add(studentId)
            print(f"{info['name'].ljust(50)[:50]} : {studentId}")
            for assignment in info['unsubmitted']:
                print(f"    - {assignment}")
            if notify == "y":
                missed = "\n\t".join(map(str,unfinishedAssignments[studentId].get('unsubmitted')))  # Convert each number to a string
                sendMessage([f"'{studentId}'"], "Missing Assignments", f"{msg}\n\n\t{missed}")

# Get Last Login
def getLastLogin(studentId):
    global _lastLogin

    if studentId not in _lastLogin:
        params = { "include[]": "last_login" }
        response = requests.get(f"{canvasURL}/users/{studentId}", headers=headers, params=params)
        _lastLogin[studentId] = response.json()
    return _lastLogin[studentId]["last_login"]

def getUnfinishedAssignments(courseId):
    students    = getStudents(courseId)
    assignments = getAssignments(courseId)
    studentAssignments = {
        student['id']: {
            "name": student['name'], 
            "email": student["email"], 
            "unsubmitted": []} 
        for student in students}

    for assignment in assignments:
        dueDateStr = assignment.get('due_at')
        if dueDateStr:
            dueDate = datetime.fromisoformat(dueDateStr.replace('Z', '+00:00'))
            # Skip assignments that aren't past due
            if dueDate > datetime.now(timezone.utc):
                print(f"Not due yet: {dueDateStr.split('T')[0]} : {assignment['name']}")
                continue

        submissions = getSubmissionByStatus(courseId, assignment['id'], 'unsubmitted')
        for submission in submissions:
            studentId = submission['user_id']
            if studentId in studentAssignments:
                studentAssignments[studentId]["unsubmitted"].append(assignment['name'])
    return studentAssignments

def getSubmissionByStatus(courseId, assignmentId, state):
    global _submissionByStatus
    print(f"getSubmissionByStatus\t{courseId} {assignmentId} {state}")
    if assignmentId not in _submissionByStatus:
        response = requests.get(f"{canvasURL}/courses/{courseId}/assignments/{assignmentId}/submissions", headers=headers, params={"per_page": 100})
        _submissionByStatus[assignmentId] = response.json()
    # for s in _submissionByStatus[assignmentId]:
    #     print(f"Not due yet: {s['id']} : {s['missing']}")

    return [s for s in _submissionByStatus[assignmentId] if s['missing'] == True]


# # Get Total Activity Time
# def getTotalActivityTime(studentId):
#     response = requests.get(f"{canvasURL}/courses/{courseId}/users/{studentId}", headers=headers)
#     stats = response.json()
#     activityTime = stats.get("total_activity_time", "N/A")
#     return activityTime
# # total_activity_time = analytics_data.get("total_activity_time", "N/A")
