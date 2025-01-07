import canvas

def reviewUnsubmitted():
    # Example usage:
    unfinished_assignments = canvas.getUnfinishedAssignments(canvas.courseId)

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
