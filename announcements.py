import canvas
import sys

courseId = "320100"
school = "byui"
# 119069    119066

# get set up params
if len(sys.argv) > 2:
    school   = sys.argv[1]
    courseId = sys.argv[2]
else:
    school = input("Enter School: ")
    courseId = input("Enter Course: ")

canvas.setSchool(school)

assignments = canvas.getAnnouncements(courseId)
for assignment in assignments:
    #       url message
    print(f"{assignment['id']}  {assignment['title']}")
    delete = input("Delete?: ")
    if delete == "y":
        deleted = canvas.deleteAnnouncements(courseId, assignment['id'])
        print(f"{deleted["discussion_topic"]["id"]}  {deleted["discussion_topic"]["title"]} {deleted["discussion_topic"]["workflow_state"]}")

# announcementId = input("Enter Announcement: ")
# #   "2252198"
# deleted = deleteAnnouncements(courseId, announcementId)
# print(f"{deleted["discussion_topic"]["id"]}  {deleted["discussion_topic"]["title"]} {deleted["discussion_topic"]["workflow_state"]}")

assignments = canvas.getAnnouncements(courseId)
for assignment in assignments:
    #       url message
    print(f"{assignment['id']}  {assignment['title']}")
