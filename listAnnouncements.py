import canvas

def listAnnouncements():
    courseId = canvas.getParams()

    announcements = canvas.getAnnouncements(courseId)
    for announcement in announcements:
        #       url message
        print(f"{announcement['id']}  {announcement['title']}")
        delete = input("Delete?: ")
        if delete == "y":
            deleted = canvas.deleteAnnouncements(courseId, announcement['id'])
            print(f"{deleted["discussion_topic"]["id"]}  {deleted["discussion_topic"]["title"]} {deleted["discussion_topic"]["workflow_state"]}")

    announcements = canvas.getAnnouncements(courseId)
    for announcement in announcements:
        #       url message
        print(f"{announcement['id']}  {announcement['title']}")
