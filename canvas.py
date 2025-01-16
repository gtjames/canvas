import requests
import json
from datetime import datetime, timezone

school   = ""
canvasURL = ""
headers   = ""
courseId  = ""
color = {"3252": "\033[30m", "4205": "\033[30m", "reset": "\033[0m"}


_announcements = {}
_assignments = {}
_categories = {}
_groups = {}
_groupMembers = {}
_lastLogin = {}
_students = {}
_submissionByStatus = {}
_unassigned = {}

def clearCache():
    global _announcements
    global _assignments
    global _categories
    global _groups
    global _groupMembers
    global _lastLogin
    global _students
    global _submissionByStatus
    global _unassigned
    global color

    _announcements = {}
    _assignments = {}
    _categories = {}
    _groups = {}
    _groupMembers = {}
    _lastLogin = {}
    _students = {}
    _submissionByStatus = {}
    _unassigned = {}
    color = {"3252": "\033[30m", "4205": "\033[30m", "reset": "\033[0m"}

def setColor(rgb):
    color[courseId] = f"\033[3{rgb}m"
    print(f"{color[courseId]}Course color for {courseId}\033[0m")

def setParams():
    global school
    global courseId

    school   = input("Enter School: ")
    courseId = input("Enter Course: [3252, 4205, 119066, 119069]: ")
    courses = ["3252", "4205", "119066", "119069"]
    if (int(courseId) < 10):
        courseId = courses[int(courseId)]
        print(f"{color[courseId]}{courseId}")
    setSchool(school)
    if courseId not in color:
        setColor(4)
    return courseId

# Canvas API details
def setSchool(schoolId):
    global school
    global canvasURL
    global headers

    if (schoolId == ""):
        school = "byupw"
    else:
        school = schoolId

    canvasURL = f"https://{school}.instructure.com/api/v1"

    # Load the JSON key file
    with open('keys.json', 'r') as file:
        data = json.load(file)

    headers = { "Authorization": f"Bearer {data[f"{school}"]}" }

def getCanvasURL():
    return canvasURL

def getAuthorization():
    return headers

def getAnnouncements(courseId):
    global _announcements

    if courseId not in _announcements:
        response = requests.get(f"{canvasURL}/courses/{courseId}/discussion_topics?only_announcements=true", headers=headers, params={"per_page": 100})
        _announcements[courseId] = response.json()
    return _announcements[courseId]

def getAssignments(courseId):
    global _assignments

    if courseId not in _assignments:
        response = requests.get(f"{canvasURL}/courses/{courseId}/assignments", headers=headers, params={"per_page": 100})
        _assignments[courseId] = response.json()
    return _assignments[courseId]

# Get group categories
def getCategories(courseId):
    global _categories

    if courseId not in _categories:
        response = requests.get( f"{canvasURL}/courses/{courseId}/group_categories", headers=headers )
        _categories[courseId] = response.json()
    return _categories[courseId]

# Get all groups within the specified group category
def getGroups(catId):
    global _groups

    if catId not in _groups:
        response = requests.get( f"{canvasURL}/group_categories/{catId}/groups?per_page=20", headers=headers )
        _groups[catId] = response.json()
    return _groups[catId]

# Get members in each group
def getGroupMembers(groupId):
    global _groupMembers

    if groupId not in _groupMembers:
        response = requests.get( f"{canvasURL}/groups/{groupId}/users", headers=headers )
        _groupMembers[groupId] = response.json()
    return _groupMembers[groupId]

# Get Last Login
def getLastLogin(studentId):
    global _lastLogin

    if studentId not in _lastLogin:
        params = { "include[]": "last_login" }
        response = requests.get(f"{canvasURL}/users/{studentId}", headers=headers, params=params)
        _lastLogin[studentId] = response.json()
    return _lastLogin[studentId]["last_login"]

def getStudent(studentId):
    global _students

    if studentId not in _students:
        response = requests.get( f"{canvasURL}/users/{studentId}/profile", headers=headers )
        _students[studentId] = response.json()
    return _students[studentId]

def getStudents(courseId):
    global _students

    if courseId not in _students:
        params = {
            "enrollment_type[]": "student",
            "per_page": 100,  # Maximum allowed per page
        }
        response = requests.get(f"{canvasURL}/courses/{courseId}/users", headers=headers, params=params)
        _students[courseId] = response.json()
    return _students[courseId]

def sortByAttr(data, attribute):
    try:
        # Use sorted with the attribute as the key
        return sorted(data, key=lambda item: item[attribute])
    except KeyError:
        print(f"{color[courseId]}Invalid attribute: {attribute}")
        return data

# def studentRoster():
#     students = getStudents(courseId)
#     sortBy = input(f"{color['reset']}Sort By (name, email): ")
#     while len(sortBy) > 0:
#         students = sortByAttr(students, sortBy)

#         for student in students:
#             showStudent(student['id'], student["name"])
#         print(f"{color[courseId]}# Enrolled: {len(students)}")
#         sortBy = input(f"{color['reset']}Sort By (name, email): ")

def getSubmissionByStatus(courseId, assignmentId, state):
    global _submissionByStatus

    if assignmentId not in _submissionByStatus:
        response = requests.get(f"{canvasURL}/courses/{courseId}/assignments/{assignmentId}/submissions", headers=headers, params={"per_page": 100})
        _submissionByStatus[assignmentId] = response.json()
    return [s for s in _submissionByStatus[assignmentId] if s['missing'] == 1]

# Get Total Activity Time
def getTotalActivityTime(studentId):
    response = requests.get(f"{canvasURL}/courses/{courseId}/users/{studentId}", headers=headers)
    stats = response.json()
    activityTime = stats.get("total_activity_time", "N/A")
    return activityTime
# total_activity_time = analytics_data.get("total_activity_time", "N/A")

# Get members not in a group
def getUnassigned(groupId):
    global _unassigned

    if groupId not in _unassigned:
        params = { "per_page": 100 }  # Maximum allowed per page 
        response = requests.get( f"{canvasURL}/group_categories/{groupId}/users?unassigned=true", headers=headers, params=params )
        _unassigned[groupId] = response.json()
    return _unassigned[groupId]

def getUnfinishedAssignments(courseId):
    students    = getStudents(courseId)
    assignments = getAssignments(courseId)
    studentAssignments = {student['id']: {"name": student['name'], "unsubmitted": []} for student in students}

    for assignment in assignments:
        dueDate = assignment.get('due_at')
        if dueDate:
            dueDate = datetime.fromisoformat(dueDate.replace('Z', '+00:00'))
            # Skip assignments that aren't past due
            if dueDate > datetime.now(timezone.utc):
                continue
        # print(f"{color[courseId]}assignmentName: {assignment['name']}, dueDate: {dueDate}")
        submissions = getSubmissionByStatus(courseId, assignment['id'], 'unsubmitted')
        for submission in submissions:
            studentId = submission['user_id']
            if studentId in studentAssignments:
                studentAssignments[studentId]["unsubmitted"].append(assignment['name'])
    return studentAssignments

# traverse from the categories in a course to the groups to the members
def listMembers(group):
    print(f"{group['name']} # in Group: {group['members_count']} ")
    members = getGroupMembers(group['id'])
    for member in members:
        showStudent(member['id'], member["name"])
    return len(members)

def deleteAnnouncements(courseId, topicId):
    response = requests.delete(f"{canvasURL}/courses/{courseId}/discussion_topics/{topicId}", headers=headers)
    return response.json()

# Get details on a student
def showStudent(studentId, name):
    try:
        student = getStudent(studentId)
        # Get the last and first names
        lastName, rest = student['sortable_name'].split(", ")
        firstName = rest.split(" ")[0]
        print(f"{color[courseId]}    - {firstName.ljust(10)[:10]} {lastName.ljust(15)} {student['primary_email'].ljust(30)} - {student['time_zone'].ljust(15)[:15]} ")
    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"{color[courseId]}    - {name} has dropped the course")

