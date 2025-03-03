from  nameGroups import renameGroups
from  canvas import courseId, test, setParams, clearCache, getStudents, listAnnouncements, reviewUnsubmitted, sendStatusLetters, sendMessage, setColor, listTeamMembers, studentInTeam, studentsInClass

def main():
    setParams()
    while True:
        print("\nMain Menu")
        print("0. Student Roster")
        print("1. Team Status")
        print("2. Students in Team")
        print("3. Review Unsubmitted")
        print("4. Delete old Announcements")
        print("5. Rename Groups")
        print("6. Clear Cache")
        print("7. Set Colors")
        print("8. Send Missing Assignment Letters")
        print("9. Send Letter to 1 student")
        print("10. Send Letters to a Class")
        print("11. Set School and Class")
        print("E(x)it")
        
        choice = input("Enter your choice: ")

        match choice:
            case 'x':
                exit()
            case '0':
                studentsInClass()
            case '1':
                listTeamMembers()
            case '2':
                studentInTeam()
            case '3':
                reviewUnsubmitted()
            case '4':
                listAnnouncements()
            case '5':
                renameGroups()
            case '6':
                clearCache()
            case '7':
                setColor(input("Enter 0-8: "))
            case '8':
                sendStatusLetters();
            case '9':
                studentId = input("Student Id: ")
                subject   = input("Subject: ")
                body      = input("Body: ")
                sendMessage([studentId], subject, body)
            case '10':
                studentList = getStudents(courseId)
                studentIds = [student['id'] for student in studentList]
                subject   = input("Subject: ")
                body      = input("Body: ")
                sendMessage(studentIds, subject, body)
            case '11':
                setParams()
            case '12':
                test()
            case "_":
                print("Invalid choice, please try again.")

main()
