import  listAnnouncements
import  listGroups
import  nameGroups
import  unsubmitted
import  canvas

def main():
    while True:
        print("\nMain Menu")
        print("0. Student List")
        print("1. Delete old Announcements")
        print("2. List Team Members")
        print("3. Rename Groups")
        print("4. Review Unsubmitted")
        print("5. Students w/ Teams")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '9':
            exit()
        if len(choice) > 2:
            choice, canvas.school, canvas.courseId  = choice.split(" ")
            canvas.setSchool(canvas.school)
        else:
            canvas.getParams()

        if choice == '0':
            canvas.studentRoster()
        elif choice == '1':
            listAnnouncements.listAnnouncements()
        elif choice == '2':
            listGroups.listTeamMembers()
        elif choice == '3':
            nameGroups.nameGroups()
        elif choice == '4':
            unsubmitted.reviewUnsubmitted()
        elif choice == '5':
            listGroups.studentInTeam()
        else:
            print("Invalid choice, please try again.")

main()
