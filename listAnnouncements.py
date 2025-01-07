import canvas

def listAnnouncements():
    announcements = canvas.getAnnouncements(canvas.courseId)
    for announcement in announcements:
        #       url message
        print(f"{announcement['id']}  {announcement['title']}")
        delete = input("Delete?: ")
        if delete == "y":
            deleted = canvas.deleteAnnouncements(canvas.courseId, announcement['id'])
            print(f"{deleted["discussion_topic"]["id"]}  {deleted["discussion_topic"]["title"]} {deleted["discussion_topic"]["workflow_state"]}")

    announcements = canvas.getAnnouncements(canvas.courseId)
    for announcement in announcements:
        #       url message
        print(f"{announcement['id']}  {announcement['title']}")
