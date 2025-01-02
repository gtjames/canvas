import requests
import json

school = ""

def setSchool(schoolId):
    global school
    school = schoolId

# Canvas API details
def getCanvasURL(school):
    return  f"https://{school}.instructure.com/api/v1"

def getAuthorization(school):
    # Load the JSON key file
    with open('keys.json', 'r') as file:
        data = json.load(file)
        API_KEY = data[f"{school}"]
        # API_KEY = file.read()         # this is when I was just reading the file as a text file
        # API_KEY = API_KEY.rstrip("\r\n")

    return { "Authorization": f"Bearer {API_KEY}" }

# Get group categories
def getCategories(courseId):
    canvasURL = getCanvasURL(school)
    headers = getAuthorization(school)

    response = requests.get( f"{canvasURL}/courses/{courseId}/group_categories", headers=headers )
    response.raise_for_status()
    return response.json()

# Get all groups within the specified group category
def getGroups(catId):
    canvasURL = getCanvasURL(school)
    headers = getAuthorization(school)

    response = requests.get( f"{canvasURL}/group_categories/{catId}/groups?per_page=20", headers=headers )
    response.raise_for_status()
    return response.json()

# Get members in each group
def getGroupMembers(group_id):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    response = requests.get( f"{canvasURL}/groups/{group_id}/users", headers=headers )
    response.raise_for_status()
    return response.json()

def getStudent(studentId):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    response = requests.get( f"{canvasURL}/users/{studentId}/profile", headers=headers )
    response.raise_for_status()  # Raise an HTTPError if the response was unsuccessful
    return response.json()

def getStudents(courseId):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    url = f"{canvasURL}/courses/{courseId}/users"
    params = {
        "enrollment_type[]": "student",
        "per_page": 100,  # Maximum allowed per page
    }

    response = requests.get(url, headers=headers, params=params)
    students = response.json()
    return students

# Get members not in a group
def getUnassigned(groupId):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    response = requests.get( f"{canvasURL}/group_categories/{groupId}/users?unassigned=true", headers=headers )
    response.raise_for_status()
    return response.json()

# Get members not in a group
def getUnassignedMbr(groupId):
    members = getUnassigned(groupId)
    for member in members:
        getStudent(member['id'], member)

def getAnnouncements(courseId):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    url = f"{canvasURL}/courses/{courseId}/discussion_topics?only_announcements=true"

    response = requests.get(url, headers=headers, params={"per_page": 100})
    return response.json()

def deleteAnnouncements(courseId, topicId):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    url = f"{canvasURL}/courses/{courseId}/discussion_topics/{topicId}"
    response = requests.delete(url, headers=headers)
    deleted = response.json()
    return deleted


def getAssignments(courseId):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    assignments = []
    url = f"{canvasURL}/courses/{courseId}/assignments"
    
    response = requests.get(url, headers=headers, params={"per_page": 100})
    return response.json()

def getSubmissionByStatus(courseId, assignmentId, state):
    headers = getAuthorization(school)
    canvasURL = getCanvasURL(school)

    submissions = []
    
    url = f"{canvasURL}/courses/{courseId}/assignments/{assignmentId}/submissions"
    response = requests.get(url, headers=headers, params={"per_page": 100})
    submissions = response.json()
    
    # uniqueStates = {s['workflow_state'] for s in submissions}
    # print(uniqueStates)

    return [s for s in submissions if s['workflow_state'] == state]

# traverse from the categories in a course to the groups to the members
def listMembers(group):
    print(f"{group['name']} # in Group: {group['members_count']} ")
    members = getGroupMembers(group['id'])
    for member in members:
        getStudent(member['id'], member)

