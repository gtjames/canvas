import canvas

def reviewUnsubmitted():
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
