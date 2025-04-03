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
_missing       = {}
_studentList   = {}
_studentsById  = {}
_studentAssignments = {}
_studentAllAssignments = {}
_submissionsByStudent = {}
_allSubmission = {}
_unassigned    = {}

def clearCache():
    global _announcements
    global _assignments
    global _categories
    global _enrollments
    global _groupMembers
    global _groups
    global _lastLogin
    global _missing
    global _studentList
    global _studentsById
    global _studentAssignments
    global _studentAllAssignments
    global _allSubmission
    global _unassigned

    _announcements      = {}
    _assignments        = {}
    _categories         = {}
    _enrollments        = {}
    _groupMembers       = {}
    _groups             = {}
    _lastLogin          = {}
    _missing            = {}
    _studentList        = {}
    _studentsById       = {}
    _studentAssignments = {}
    _studentAllAssignments = {}
    _allSubmission = {}
    _unassigned         = {}

def listTeamMembersByGroup():
    categories = getStudentGroups(courseId)
    grpType = input("(1) Solo, (0) All, (u) Unassigned: ")

    while len(grpType) > 0:
        cnt = 0
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
                        print(f"{group['name']}")
                        continue

                    if (group['members_count'] == 1 and grpType == "1") or grpType == "0":
                        cnt = listMembers(group, grpType) + cnt
                print(f"Members: {cnt}")
        grpType = input("(1) Solo, (0) All, (u) Unassigned: ")

# Get group categories
def getStudentGroups(courseId):
    global _categories

    studentsById = getAllStudentDetails(courseId)

    if courseId not in _categories:
        _categories[courseId] = getCanvasData(f"/courses/{courseId}/group_categories", {}, "categories")

        for category in _categories[courseId]:
            if category['name'] == "Who is Here":
                continue
            
            groups = getGroups(category['id'])
            for group in groups:
                if group['members_count'] == 0:
                    continue

                members = getGroupMembers(group['id'])
                for member in members:
                    student = studentsById[member["id"]]
                    student["group"]     = group["name"][:7] 

    return _categories[courseId]

# Get members not in a group
def getUnassigned(groupId):
    global _unassigned

    if groupId not in _unassigned:
        _unassigned[groupId] = getCanvasData(f"/group_categories/{groupId}/users", {"unassigned":True, "per_page": 100}, "unassigned")
    return _unassigned[groupId]

def studentSearch():
    studentList = getStudentList(courseId)

    notifyNoneParticipating = False
    if input("Email Non Participating?: ") == 'y':
        notifyNoneParticipating = True

    group = ""
    sortBy = input("Sort By (first, last, group, score, login, tz, email, id): ")
    size = 0
    while len(sortBy) > 0:
        if sortBy == "search":
            name = input("Enter First or Last Name: ")
            students = [s for s in studentList if name in s.name]
        else:
            sortBy, students = sortByAttr(studentList, sortBy)
        print(f"# of Students: {len(students)}")
        for student in students:
            match sortBy:
                case "group":                       #   sorting by group
                    if group != student["group"]:           #   did the group change?
                        if size > 0:                        #   if so, print the group size
                            print(f"Members in Group {size}")
                        print(f"\t\t{student["group"]}")    #   print the group name
                        group = student["group"]            #   save current group
                        size = 0                            #   reset the group size
                    size += 1                               #   increment the group size
                    print(f"{student["first"]} {student["last"]} : {student["login"]} : {student["email"]} : {student["tz"]}")
                case "login" | "lastActivity":
                    print(f"{student["first"]} {student["last"]} : {student["login"]} : {student["group"]} : {student["lastActivity"]}");
                    lastLogin = datetime.fromisoformat(student["lastLogin"])
                    aWeekAgo = datetime.now(lastLogin.tzinfo) - timedelta(days=7)
                    if lastLogin < aWeekAgo and notifyNoneParticipating:
                        sendMessage([student["id"]], "You have not participated in the class this week",
                            "Please let me know if you are having trouble with the class")
                case "id":
                    print(f"{student["first"]} {student["last"]} : {student["login"]} : {student["email"]} : {student["id"]}");
                case "score" | "activityTime" | "grade":
                    print(f"{student["first"]} {student["last"]} : {student["score"]:-7.2f} : {student["grade"]} : {student["activityTime"]}");
                case "first" | "tz":
                    print(f"{student["first"]} {student["last"]} : {student["group"]} : {student["email"]} : {student["tz"]}")
                case _:
                    print(f"{student["first"]} {student["last"]} : {student["email"]} : {student["id"]}")
        sortBy = input("Sort By (first, last, group, score, login, tz, email, id): ")

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
    getAllStudentDetails (courseId)       #   _studentList
    getStudentGroups      (courseId)       #   _categories

def getAnnouncements(courseId):
    global _announcements

    if courseId not in _announcements:
        _announcements[courseId] = getCanvasData(f"/courses/{courseId}/discussion_topics?only_announcements=true", params={"per_page": 100})
    return _announcements[courseId]

def listAnnouncements():
    announcements = getAnnouncements(courseId)
    for announcement in announcements:
        print(f"{announcement['id']}  {announcement['title']}")

def getAssignments(courseId):
    global _assignments
    
    if courseId not in _assignments:
        tmp = getCanvasData(f"/courses/{courseId}/assignments", {"per_page": 100}, "assignments")

        sub = [        {
            "id"             : a["id"],
            "dueAt"          : a["due_at"],
            "lockAt"         : a["lock_at"],
            "possiblePts"    : a["points_possible"],
            "title"          : a["name"].ljust(50),
            "hasSubmissions" : a["has_submitted_submissions"]
        } for a in tmp]

        _assignments[courseId] = sub;

    return _assignments[courseId]

def getStudentList(courseId):
    global _studentList
    return _studentList[courseId]

def getAllStudentDetails(courseId):
    global _studentList
    global _studentsById

    if courseId not in _studentList:
        params = {
            "enrollment_type[]": "student",
            "per_page": 100,  # Maximum allowed per page
        }
        _studentList[courseId] = getCanvasData(f"/courses/{courseId}/users", params, "students")
        _studentsById = {}
        _studentsById[courseId] = {}

        scores = getEnrollments(courseId)

        tmp = {
            student['id']: {
        } for student in _studentList[courseId]}

        for student in _studentList[courseId]:
            profile   = getStudentProfile(student['id'])
            lastLogin = getLastLogin(student['id'])

            lastName, rest = student["sortable_name"].split(", ")
            firstName = rest.split(" ")[0].ljust(10)[:10]
            tm  = scores[student["id"]]["activityTime"]

            student['activityTime'] = f"{int(tm/60):5d}.{tm%60:02d}"
            student['email']        = student['email'].ljust(30)
            student['first']        = firstName.ljust(10)[:10]
            student['last']         = lastName.ljust(15)[:15]
            student["lastActivity"] = scores[student['id']]['lastActivity']
            student['lastLogin']    = lastLogin
            student['login']        = lastLogin.replace('T', ' ')[5:16]
            student['tz']           = profile['time_zone']
            student["grade"]        = scores[student['id']]['grade']
            student["group"]        = "Team XX"
            student["name"]         = student['sortable_name']
            student["score"]        = scores[student['id']]['score']
            _studentsById[courseId][student.get('id')] = student

    return _studentsById[courseId]

def getStudentProfile(studentId):
    return getCanvasData(f"/users/{studentId}/profile", {}, ""+str(studentId))

def getStudent(courseId, studentId):
    global _studentsById

    # studentRec = next((_studentsById[courseId][student] for student in _studentList[courseId] if student == studentId), None)
    # if studentRec == None:
    #     print(f"    - {studentId} not found")
    #     studentRec = getStudentProfile(studentId)
    # return studentRec
    return _studentsById[courseId][studentId];

# Get details on a student
def showStudent(studentId, name):
    try:
        student = getStudent(courseId, studentId)
        print(f"    - {student.get('first')} {student.get('last')} {student.get('email')} - {student.get('tz')} ")
    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"    - {name} has dropped the course")

# Get Last Login
def getEnrollments(courseId):
    global _enrollments

    if courseId not in _enrollments:
        _enrollments[courseId] = getCanvasData(f"/courses/{courseId}/enrollments", {"per_page": 100, "type[]": "StudentEnrollment"}, "activity") 
        tmp = {
            student['user_id']: {
                "lastActivity": f"{student['last_activity_at'].replace('T', ' ')[5:16]}",
                "activityTime":    student['total_activity_time'],
                "grade"       : f"{student['grades']['current_grade'].ljust(2)}",
                "score"       :    student['grades']['current_score'],
        } for student in _enrollments[courseId]}
    _enrollments[courseId] = tmp
    return _enrollments[courseId]


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
        _groups[catId] = getCanvasData(f"/group_categories/{catId}/groups", {"per_page": 100}, "groups")

    return _groups[catId]

# Get members in each group
def getGroupMembers(groupId):
    global _groupMembers

    if groupId not in _groupMembers:
        _groupMembers[groupId] = getCanvasData(f"/groups/{groupId}/users", {"per_page": 100}, "groupMembers"+str(groupId))
    return _groupMembers[groupId]

def sendStatusLetters():
    studentList = getStudentList(courseId)
    unfinishedAssignments = getUnfinishedAssignments(courseId)
    _, studentList = sortByAttr(studentList, "score")

    statusLetter(studentList, 90, 101, unfinishedAssignments,
                 "Keep up the good work!: Current Score: ",
                "\nYou are doing very well in the class keep up the good work")
    statusLetter(studentList, 70, 90, unfinishedAssignments,
                "You are doing well but might be missing a few assignments: Current Score: ",
                "\nYou can still turn these in until the end of week four")
    statusLetter(studentList, 0, 70, unfinishedAssignments,
                 "How are you doing in the class? It looks like you are struggling: Current Score: ",
                "\nHere is a list of your missing assignments. You can still turn these in until the end of week four\nDon't forget there is tutoring available for the class.")

def statusLetter(studentScores, lo, hi, unfinishedAssignments, subject, body):
    list = [ student for student in studentScores   if lo <= student["score"] < hi ]

    go = input("go/no go? ")

    for s in list:
        print(f"{s['score']:6.1f} - {s['name']} {" dropped" if s['id'] not in unfinishedAssignments else ""}")

        # Check if the student ID is in the unfinishedAssignments dictionary
        if s['id'] not in unfinishedAssignments or go != 'go':
            continue

        missed = "\n\t".join(map(str,unfinishedAssignments[s['id']]['unsubmitted']))

        sendMessage([s['id']],  f"{subject} {s['score']}",
                                f"\n{s['firstName']},\n{body}\nMissing Assignments(if any)\n\t{missed}\n\nBro. James")

def listUnsubmitted():
    unfinishedAssignments = getUnfinishedAssignments(courseId)

    notify = input("Notify?: ")
    msg = input("Message?: ")
    msg = msg if msg else "\tThe Following assignments have not been submitted.\n\tThese can all be submitted up to the end of Week 4."
    missing = input("(A)ll / (M)issing?: ")

    for studentId, unsub in unfinishedAssignments.items():
        print(f"{unsub['name'].ljust(50)[:50]} : {len(unsub)}")
        displayList = unsub['submissions']
        if missing == "m":
            missingWork = [asgn for asgn in displayList if asgn.get("missed")]
            missingList = "\n".join(f"\t{a['title']}" for a in missingWork) if missingWork else "\tAll Assignments are Submitted"                                          
            print(missingList);
            if notify == "y" and len(missingWork) > 0:
                missed = "\n\t".join(map(str,unfinishedAssignments[studentId]['unsubmitted']))  # Convert each number to a string
                sendMessage([f"'{studentId}'"], "Missing Assignments", f"{msg}\n\n\t{missed}")
            else:
                for assignment in displayList:
                    if assignment.missed:
                        print(f"              {assignment}")
                    else:
                        print(f" ${assignment['score']}  {(assignment.get('submittedAt', '          T').replace('T', ' '))[5:11]} ${assignment['title']} ")

# Get Last Login
def getLastLogin(studentId):
    global _lastLogin

    if studentId not in _lastLogin:
        _lastLogin[studentId] = getCanvasData(f"/users/{studentId}", { "include[]": "last_login" }, "lastLogin"+str(studentId))

    return _lastLogin[studentId]["last_login"]

def getUnfinishedAssignments(courseId):
    if courseId not in _submissionsByStudent:

        students    = getStudentList(courseId)
        assignments = getAssignments(courseId)

        allSubmissions = {}

        submissionsByStudent = {
            student['id']: { "name": student["name"], "submissions": [] } for student in students
        }

        today = datetime.now(timezone.utc)  # Make 'today' timezone-aware
        pastAssignments = [a for a in assignments if datetime.fromisoformat(a["dueAt"]) < today]
        
        for assignment in pastAssignments:
            # Fetch all submissions for the assignment
            allSubmissions[assignment["id"]] = getSubmissions(courseId, assignment['id'], assignment['title'])
            for submission in allSubmissions[assignment["id"]]:
                studentId = submission['userId']
                if studentId in submissionsByStudent:
                    submission["title"] = assignment["title"];
                    submissionsByStudent[studentId]["submissions"].append(assignment['title'])

        _submissionsByStudent[courseId] = submissionsByStudent;

    return _submissionsByStudent[courseId]

def getSubmissions(courseId, assignmentId, title):
    global _allSubmission

    if assignmentId not in _allSubmission:
        tmp = getCanvasData(f"/courses/{courseId}/assignments/{assignmentId}/submissions", {"per_page": 100}, "sub"+str(assignmentId))
        _allSubmission[assignmentId] = []
        for a in tmp:
            b = {}
            b['grade']         = a["grade"]
            b['gradedAt']      = a["graded_at"]
            b['id']            = a["id"]
            b['score']         = a["score"]
            b['submittedAt']   = a["submitted_at"]
            b['userId']        = a["user_id"]
            b['workflowState'] = a["workflow_state"]
            b["assignmentId"]  = a["assignment_id"]
            b["late"]          = a["late"]
            b["missed"]        = a["missing"]
            b["missing"]       = a["missing"] if a["missing"] else "done   "
            b["secondsLate"]   = a["seconds_late"]
            b["title"]         = title.ljust(50)
            _allSubmission[assignmentId].append(b)

        _missing[assignmentId] = [s for s in _allSubmission[assignmentId] if s['missing'] == True]
        
    return _missing[assignmentId]
