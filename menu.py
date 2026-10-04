#menu system
from constants import CREDENTIALS_file
def inmgr(process):
    with open(CREDENTIALS_file, "r") as employees:
        credentials = csv.DictReader(employees)
        #print(credentials)
        if process.lower() == "s": #showall
            for i in credentials:
                print(i)
        elif process.lower() == "a": #append
            newEmployeeName = input("Enter name of the new employee: ")
            for ID in credentials:
                lastId = int(ID["idnum"].strip("SW"))
            newEmployeeId = f"SW{(4-len(str(lastId+1)))*"0"}{lastId+1}"
            print("The ID of the new employee is: ",newEmployeeId)
            newEmployeePass = input("Set a password: ")
            with open(CREDENTIALS_file,"a") as employees:
                write = csv.DictWriter(employees,fieldnames=fieldnames)
                write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass,"perms":employee})
                return(print(f"New entry for {newEmployeeName} added"))

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
              "Show employee data (D)\n",
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