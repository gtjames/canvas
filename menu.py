# from  nameGroups import renameGroups
from  canvas import startUp, courseId, setParams, getStudents, listUnsubmitted, sendStatusLetters, sendMessage, listTeamMembers, studentInTeam

def main():

# Print all command-line arguments
    setParams()
    startUp();
    
    while True:
        print("\nMain Menu")
        print("1. Team Members        2. Students in Team")
        print("3.  List Unsubmitted   4. Missing Assignment Letters")
        print("5.  Message 1 student  6. Message Class")
        print("10. Set School and Class")
        print("E(x)it")

        # print("5. Rename Groups")
        
        choice = input("Enter your choice: ")

        match choice:
            case '1':
                listTeamMembers()
            case '2':
                studentInTeam()
            case '3':
                listUnsubmitted()
            case '4':
                sendStatusLetters();
            case '5':
                studentId = input("Student Id: ")
                subject   = input("Subject: ")
                body      = input("Body: ")
                sendMessage([studentId], subject, body)
            case '6':
                studentList = getStudents(courseId)
                studentIds = [student['id'] for student in studentList]
                subject   = input("Subject: ")
                body      = input("Body: ")
                sendMessage(studentIds, subject, body)

            # case 'r':
            #     renameGroups()
            case '10':
                setParams()
            case 'x':
                exit()
            case _:
                print("Invalid choice, please try again.")

main()
