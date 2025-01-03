import sys
import canvas

courseId = "320100"
school = "byui"
single = "0";
num = 0

# Run the function
if len(sys.argv) > 2:
    school   = sys.argv[1]
    courseId = sys.argv[2]
else:
    school   = input("Enter School: ")
    courseId = input("Enter Course: ")

canvas.setSchool(school)

def listUnfinishedAssignments(courseId):
    students    = canvas.getStudents(courseId)
    assignments = canvas.getAssignments(courseId)
    studentAssignments = {student['id']: {"name": student['name'], "unsubmitted": []} for student in students}

    for assignment in assignments:
        submissions = canvas.getSubmissionByStatus(courseId, assignment['id'], 'unsubmitted')
        for submission in submissions:
            studentId = submission['user_id']
            if studentId in studentAssignments:
                studentAssignments[studentId]["unsubmitted"].append(assignment['name'])

    return studentAssignments

# Example usage:
unfinished_assignments = listUnfinishedAssignments(courseId)

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
    print()