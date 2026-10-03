#menu system
from constants import CREDENTIALS_file
def inLogon(process):
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

def menuDial(key):
    if key == "foo":
        return(print("bar"))