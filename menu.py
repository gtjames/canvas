import  listAnnouncements
import  listGroups
import  nameGroups
import  unsubmitted

def main():
    while True:
        print("\nMain Menu")
        print("1. Review Announcements")
        print("2. List Team Members")
        print("3. Setup Groups")
        print("4. Review Unsubmitted")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            listAnnouncements.listAnnouncements()
        elif choice == '2':
            listGroups.listTeamMembers()
        elif choice == '3':
            nameGroups.nameGroups()
        elif choice == '4':
            unsubmitted.reviewUnsubmitted()
        elif choice == '5':
            exit()
        else:
            print("Invalid choice, please try again.")

main()
