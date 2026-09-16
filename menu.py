#menu system

def inLogon(process):
    with open("data/employees.csv", "r") as employees:
        credentials = csv.DictReader(employees)
        #print(credentials)
        if process.lower() == "s":
            for i in credentials:
                print(i)
        elif process.lower() == "a":
            newEmployeeName = input("Enter name of the new employee: ")
            for ID in credentials:
                lastId = int(ID["idnum"].strip("SW"))
            newEmployeeId = f"SW{(4-len(str(lastId+1)))*"0"}{lastId+1}"
            print("The ID of the new employee is: ",newEmployeeId)
            newEmployeePass = input("Set a password: ")
            with open("data/employees.csv","a") as employees:
                write = csv.DictWriter(employees,fieldnames=fieldnames)
                write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass})

def menuDial(key):
    if key == "foo":
        return(print("bar"))