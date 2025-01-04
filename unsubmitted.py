import canvas

def reviewUnsubmitted():
    courseId = canvas.getParams()

    # Example usage:
    unfinished_assignments = canvas.getUnfinishedAssignments(courseId)

    # Display results
    row = 0
    for studentId, info in unfinished_assignments.items():
        row += 1
        print(f"Student: {row} {info['name']}")
        if info['unsubmitted']:
            print("  unSubmitted Assignments:")
            for assignment in info['unsubmitted']:
                print(f"    - {assignment}")
        else:
            print("  All assignments completed!")
