import requests
import canvas

def renameGroups():
    times = [
            " 1 PM UTC --  6 AM Mtn",  " 3 PM UTC --  8 AM Mtn",  " 5 PM UTC -- 10 AM Mtn",
            " 7 PM UTC --  Noon Mtn",  " 9 PM UTC --  2 PM Mtn",  "11 PM UTC --  4 PM Mtn",
            " 1 AM UTC --  6 PM Mtn",  " 3 AM UTC --  8 PM Mtn",
            ]

    categories = canvas.getCategories(canvas.courseId)

    for category in categories:
        print(f"{category.get('name')}")
        groups = canvas.getGroups(category['id'])
        if len(groups) == 1:
            continue

        grpNum  = 0
        teamNum = 0
        first=True

        for group in groups:
            print(f"{group['name']}")
            if first:
                teamName = "People Dropping the Class",
            else:
                teamName = f"Team {teamNum:02d} WDD330 {"Tuesday" if grpNum < 8 else "Wednesday"} {times[grpNum%8]} "
            
            print(teamName)

            data = { "name": teamName, "max_membership": 6 }
            requests.put(f"{canvas.canvasURL}/groups/{group["id"]}", headers=canvas.headers, data=data)

            if first:
                first = False
                continue
            grpNum=grpNum+1
            teamNum=teamNum+1
            if teamNum == 8:
                teamNum=teamNum+2
