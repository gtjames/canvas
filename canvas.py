import requests
import json
from datetime import datetime, timezone

school   = ""
canvasURL = ""
headers   = ""
courseId  = ""

def getParams():
    global school
    global courseId

    school   = input("Enter School: ")
    courseId = input("Enter Course: [3252, 4205, 119066, 119069]: ")

    courses = ["3252", "4205", "119066", "119069"]
    if (int(courseId) < 10):
        courseId = courses[int(courseId)]
        print(F"{courseId}")
    setSchool(school)
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
    response = requests.get(f"{canvasURL}/courses/{courseId}/discussion_topics?only_announcements=true", headers=headers, params={"per_page": 100})
    return response.json()

def getAssignments(courseId):
    response = requests.get(f"{canvasURL}/courses/{courseId}/assignments", headers=headers, params={"per_page": 100})
    return response.json()

# Get group categories
def getCategories(courseId):
    response = requests.get( f"{canvasURL}/courses/{courseId}/group_categories", headers=headers )
    return response.json()

# Get all groups within the specified group category
def getGroups(catId):
    response = requests.get( f"{canvasURL}/group_categories/{catId}/groups?per_page=20", headers=headers )
    return response.json()

# Get members in each group
def getGroupMembers(group_id):
    response = requests.get( f"{canvasURL}/groups/{group_id}/users", headers=headers )
    return response.json()

def getStudent(studentId):
    response = requests.get( f"{canvasURL}/users/{studentId}/profile", headers=headers )
    return response.json()

def getStudents(courseId):
    params = {
        "enrollment_type[]": "student",
        "per_page": 100,  # Maximum allowed per page
    }
    response = requests.get(f"{canvasURL}/courses/{courseId}/users", headers=headers, params=params)
    return response.json()

def sortByAttr(data, attribute):
    try:
        # Use sorted with the attribute as the key
        return sorted(data, key=lambda item: item[attribute])
    except KeyError:
        print(f"Invalid attribute: {attribute}")
        return data

def studentRoster():
    sortBy = input("Sort By (name, email): ")
    students = getStudents(courseId)
    students = sortByAttr(students, sortBy)

    for student in students:
        showStudent(student['id'], student["name"])
    print(f"# Enrolled: {len(students)}")

def getSubmissionByStatus(courseId, assignmentId, state):
    response = requests.get(f"{canvasURL}/courses/{courseId}/assignments/{assignmentId}/submissions", headers=headers, params={"per_page": 100})
    submissions = response.json()
    
    # uniqueStates = {s['workflow_state'] for s in submissions}
    # print(uniqueStates)
    # return [s for s in submissions if s['workflow_state'] == state]
    return [s for s in submissions if s['missing'] == 1]

# Get members not in a group
def getUnassigned(groupId):
    params = { "per_page": 100 }  # Maximum allowed per page 
    response = requests.get( f"{canvasURL}/group_categories/{groupId}/users?unassigned=true", headers=headers, params=params )
    response.raise_for_status()
    return response.json()

def getUnfinishedAssignments(courseId):
    students    = getStudents(courseId)
    assignments = getAssignments(courseId)
    pastDueAssignments = []
    studentAssignments = {student['id']: {"name": student['name'], "unsubmitted": []} for student in students}

    for assignment in assignments:
        dueDate = assignment.get('due_at')
        if dueDate:
            dueDate = datetime.fromisoformat(dueDate.replace('Z', '+00:00'))
            # Skip assignments that aren't past due
            if dueDate > datetime.now(timezone.utc):
                continue
        # print(f"assignmentName: {assignment['name']}, dueDate: {dueDate}")
        submissions = getSubmissionByStatus(courseId, assignment['id'], 'unsubmitted')
        for submission in submissions:
            studentId = submission['user_id']
            if studentId in studentAssignments:
                studentAssignments[studentId]["unsubmitted"].append(assignment['name'])
                # pastDueAssignments.append({
                #     'assignmentName': assignment['name'],
                #     'studentId': submission['user_id'],
                #     'dueDate': dueDate.isoformat(),
                # })
    # print(pastDueAssignments)
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
        print(f"    - {firstName.ljust(10)[:10]} {lastName.ljust(15)} {student['primary_email'].ljust(30)} - {student['time_zone'].ljust(15)[:15]} ")

    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"    - {name} has dropped the course")

