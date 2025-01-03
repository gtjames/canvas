import requests
import json

school = ""
canvasURL = ""
headers = ""

# Canvas API details
def setSchool(schoolId):
    global school
    global canvasURL
    global headers

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

def getSubmissionByStatus(courseId, assignmentId, state):
    response = requests.get(f"{canvasURL}/courses/{courseId}/assignments/{assignmentId}/submissions", headers=headers, params={"per_page": 100})
    submissions = response.json()
    
    # uniqueStates = {s['workflow_state'] for s in submissions}
    # print(uniqueStates)
    return [s for s in submissions if s['workflow_state'] == state]

# Get members not in a group
def getUnassigned(groupId):
    response = requests.get( f"{canvasURL}/group_categories/{groupId}/users?unassigned=true", headers=headers )
    response.raise_for_status()
    return response.json()

# traverse from the categories in a course to the groups to the members
def listMembers(group):
    print(f"{group['name']} # in Group: {group['members_count']} ")
    members = getGroupMembers(group['id'])
    for member in members:
        showStudent(member['id'], member["name"])

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
        # - {st['time_zone'].ljust(15)[:15]} 
        print(f"\t- {firstName.ljust(10)[:10]} {lastName.ljust(15)} {student['primary_email']} - {student['time_zone'].ljust(15)[:15]} ")

    except requests.exceptions.RequestException as e:
        # Handle any HTTP or connection errors
        print(f"\t- {name} has dropped the course")

