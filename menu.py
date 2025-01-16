import  listAnnouncements
import  listGroups
import  nameGroups
import  canvas

def main():
    while True:
        print("\n\033[0mMain Menu")
        # print("0. Student Roster")
        print("1. Team Status")
        print("2. Students in Team")
        print("3. Review Unsubmitted")
        print("4. Delete old Announcements")
        # print("5. Rename Groups")
        print("6. Clear Cache")
        print("7. Set Colors")
        print("9. Exit")
        
        choice = input("Enter your choice: ")
        if choice == '9':
            exit()
        elif len(choice) > 2:
            choice, canvas.school, canvas.courseId  = choice.split(" ")
            canvas.setSchool(canvas.school)
            if canvas.courseId not in canvas.color:
                canvas.setColor(4)
        else:
            canvas.setParams()

        # if choice == '0':
        #     canvas.studentRoster()
        if choice == '1':
            listGroups.listTeamMembers()
        elif choice == '2':
            listGroups.studentInTeam()
        elif choice == '3':
            listAnnouncements.reviewUnsubmitted()
        elif choice == '4':
            listAnnouncements.listAnnouncements()
        # elif choice == '5':
        #     nameGroups.nameGroups()
        elif choice == '6':
            canvas.clearCache()
        elif choice == '7':
            canvas.setColor(input("Enter 0-8: "))
        else:
            print("Invalid choice, please try again.")

main()
