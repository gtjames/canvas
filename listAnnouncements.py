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
    studentIds = set()
    # Display results
    notify = input("Notify?: ")
    for studentId, info in unfinished_assignments.items():
        if info['unsubmitted']:
            studentIds.add(studentId)
            print(f"{info['name'].ljust(50)[:50]} : {info['email']}")
            for assignment in info['unsubmitted']:
                print(f"    - {assignment}")
            if notify == "y":
                missed = "\n\t".join(map(str,unfinished_assignments[studentId].get('unsubmitted')))  # Convert each number to a string
                canvas.sendMessage(studentId, "\tThe Following assignments have not been submitted", f"\t{missed}")
        # else:
        #     print("  All assignments completed!")
