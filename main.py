#main program
import csv
import login
fieldnames=["names","idnum","pass"]
def inLogon(process):
    with open("data/employees.csv", "r") as employees:
        credentials = csv.DictReader(employees)
        #print(credentials)
        if process == "showall":
            for i in credentials:
                print(i)
        elif process == "append":
            newEmployeeName = input("Enter name of the new employee: ")
            for ID in credentials:
                lastId = int(ID["idnum"].strip("SW"))
            newEmployeeId = f"SW{(4-len(str(lastId+1)))*"0"}{lastId+1}"
            print("The ID of the new employee is: ",newEmployeeId)
            newEmployeePass = input("Set a password: ")
            with open("data/employees.csv","a") as employees:
                write = csv.DictWriter(employees,fieldnames=fieldnames)
                write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass})



print(f"=========ShineOnWheels========="
      f"Welcome to Shine On Wheels!"
      f"Login as a customer or employee.\n")





# See PyCharm help at https://www.jetbrains.com/help/pycharm/
