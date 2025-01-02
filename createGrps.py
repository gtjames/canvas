import requests
import sys
import canvas

courseId = "3252"
school = "byupw"

# Run the function
if len(sys.argv) > 2:
    school   = sys.argv[1]
    courseId = sys.argv[2]
else:
    school   = input("Enter School: ")
    courseId = input("Enter Course: ")

canvas.setSchool(school)
canvasURL = canvas.getCanvasURL(school)

times = [" 1 PM UTC --  6 AM MT",  " 3 PM UTC --  8 AM MT",  " 5 PM UTC -- 10 AM MT",   
         " 7 PM UTC --  Noon MT",  " 9 PM UTC --  2 PM MT",  "11 PM UTC --  4 PM MT",
         " 1 AM UTC --  6 PM MT",  " 3 AM UTC --  8 PM MT",]
days = ["Tuesday ", "Thursday"]

headers = canvas.getAuthorization(school)

courses = canvas.getCategories(courseId)
for course in courses:
    print(f"{course['name']} (ID: {course['id']})")

    groups = canvas.getGroups(course['id'])

    grpNum = 0
    teamNum=0
    for group in groups:
        print(f"{group['name']}")
        teamName = f"Team {teamNum:02d} WDD330 {"Tuesday" if grpNum < 8 else "Thursday"} {times[grpNum%8]} UTC"
        print(teamName)
        # Data for the PUT request
        data = { "name": teamName, "max_membership": 6 }
        # print(f"{url}{group["id"]}")
        response = requests.put(f"{canvasURL}/groups/{group["id"]}", headers=headers, data=data)
        grpNum=grpNum+1
        teamNum=teamNum+1
        if teamNum == 8:
            teamNum=teamNum+2

        # Handling the response
        # if response.status_code == 200:
        #     print("Group updated successfully!")
        #     print(response.json())  # Optional: Print the returned JSON
        # else:
        #     print(f"Failed to update the group. Status code: {response.status_code}")
        #     print(response.text)  # Optional: Print the error message