#menu system
from constants import CREDENTIALS_file

def inMgr(process):
    try:
        with open(CREDENTIALS_file, "r") as employees:
            credentials = csv.DictReader(employees)
            #print(credentials)
            if process.lower() == "s":                                          #shows all employee data
                for i in credentials:
                    print(i)
                return(print("eof"))
            elif process.lower() == "a":                                        #add new employee
                newEmployeeName = input("Enter name of the new employee: ")     #assigns new employee name to variable with input prompt
                lastID = max(int(row["idnum"][2:]) for row in credentials)      #fetches largest employee ID number that exists
                newEmployeeId = f"SW{(4-len(str(lastId+1)))*"0"}{lastId+1}"     #iterates on largest employee ID number by 1 and assigns to variable
                print("The ID of the new employee is: ",newEmployeeId)          #confirms new employee name to user
                newEmployeePass = input("Set a password: ")                     #assigns employee login password to variable with input prompt
                with open(CREDENTIALS_file,"a") as employees:                   #writes new line to credentials file
                    write = csv.DictWriter(employees,fieldnames=fieldnames)
                    write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass,"perms":employee})
                    return(print(f"New entry for {newEmployeeName} added"))      #confirms to user new entry has been written to file
            elif process.lower() == "e":
                inMgr("S")
                selEmpy = input("Enter ID of employee you want to edit: ")
                for ID in credentials:
                    if ID["idnum"] == selEmpy:
                        print(ID)
                        break
                else:
                    print("No employee with ID ", selEmpy, "found")
                    return()
    except filenotfounderror:
        print(CREDENTIALS_file, "not found!!")
        return()


def menuDial(dial):
    if dial == "sysadmin":
        print("===System administrator view===\n",
              "Select data to view   (V)\n",
              "Manage employees      (E)\n",
              "Packages and schedule (M)\n",
              "Generate report       (R)\n")
        return(input("Enter a submenu of choice: "))
    elif dial == "data":
        print("===Data view===\n",
              "Customers (C)\n",
              "Bookings  (B)\n",
              "Payments  (P)\n")
        return(input("Select data choice to view: "))
    elif dial == "employee":
        print("===Employee management===\n",
              "Add employee       (A)\n",
              "Show employee data (S)\n",
              "Edit employee data (E)\n")
        return(input("Select operation type to execute: "))
    elif dial == "packsche":
        print("===Packages and schedule management===\n",
              "Service packages (P)\n",
              "Daily schedules  (S)\n")
        return(input("Manage packages or schedules: "))
    elif dial == "report":
        print("===Report generator===\n",
              "Bookings        (B)\n",
              "Revenue         (R)\n",
              "Available slots (S)")
        return(input("Generate report: "))