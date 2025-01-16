import canvas

def listAnnouncements():
    print(f"{canvas.color[canvas.courseId]}")
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
        print(f"{announcement['id']}  {announcement['title']}")

def reviewUnsubmitted():
    print(f"{canvas.color[canvas.courseId]}")
    # Example usage:
    unfinished_assignments = canvas.getUnfinishedAssignments(canvas.courseId)

    # Display results
    row = 0
    for studentId, info in unfinished_assignments.items():
        if info['unsubmitted']:
            print(f"Student: {row} {info['name']}")
            row += 1
            for assignment in info['unsubmitted']:
                print(f"    - {assignment}")
        # else:
        #     print("  All assignments completed!")
