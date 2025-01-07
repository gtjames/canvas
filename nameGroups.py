import requests
import canvas

def nameGroups():
    times = [" 1 PM UTC --  6 AM Mtn",  " 3 PM UTC --  8 AM Mtn",  " 5 PM UTC -- 10 AM Mtn",
            " 7 PM UTC --  Noon Mtn",  " 9 PM UTC --  2 PM Mtn",  "11 PM UTC --  4 PM Mtn",
            " 1 AM UTC --  6 PM Mtn",  " 3 AM UTC --  8 PM Mtn",]

    courses = canvas.getCategories(canvas.courseId)
    for course in courses:
        print(f"{course['name']} (ID: {course['id']})")

        groups = canvas.getGroups(course['id'])

        grpNum = 0
        teamNum=0
        for group in groups:
            print(f"{group['name']}")
            teamName = f"Team {teamNum:02d} WDD330 {"Tuesday" if grpNum < 8 else "Thursday"} {times[grpNum%8]} "
            print(teamName)
            # Data for the PUT request
            data = { "name": teamName, "max_membership": 6 }
            # print(f"{url}{group["id"]}")
            response = requests.put(f"{canvas.canvasURL}/groups/{group["id"]}", headers=canvas.headers, data=data)
            grpNum=grpNum+1
            teamNum=teamNum+1
            if teamNum == 8:
                teamNum=teamNum+2
