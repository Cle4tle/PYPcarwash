#menu system
import csv
import math
from datetime import datetime
from constants import CREDENTIALS_file,CUSTOMERS_file,BOOKING_file,PAYMENTS_file,SERVICES_file,MAINTENANCE_file
import input_validation

def packScheMgr(process, action, targetID=None, changes=None):
    if process.lower() == "p":
        file = SERVICES_file
        fieldnames = ["service_id", "service_name", "price", "C4"]
        idField = "service_id"
        idPrefix = "S"
        dataType = "service"
    elif process.lower() == "s":
        file = MAINTENANCE_file
        fieldnames = ["schedule_id", "date", "start_time", "end_time", "available_slots"]
        idField = "schedule_id"
        idPrefix = "D"
        dataType = "schedule"
    else:
        print(process, "is not a valid choice!, only P/S are accepted")
        return()

    if not fileCheck(file):
        dataSave(file, fieldnames, [])
    with open(file, "r", newline="") as dataFile:
        reader = csv.DictReader(dataFile)
        existingFieldnames = reader.fieldnames
        rows = list(reader)

    if existingFieldnames is None:
        dataSave(file, fieldnames, [])
    elif not all(field in existingFieldnames for field in fieldnames):
        raise ValueError(f"{file} is missing required columns: {fieldnames}")

    if action == "s":
        return rows
    if action == "a":
        newRow = {field: "" for field in fieldnames}
        newRow.update(changes or {})
        if not packScheDataIsValid(dataType, newRow):
            return False
        existingIDs = [
            int(row[idField][len(idPrefix):])
            for row in rows
            if row[idField].startswith(idPrefix) and row[idField][len(idPrefix):].isdigit()
        ]
        newRow[idField] = f"{idPrefix}{(max(existingIDs, default=0) + 1):03d}"
        rows.append(newRow)
        dataSave(file, fieldnames, rows)
        return newRow[idField]
    if action == "u":
        for row in rows:
            if row[idField] == targetID:
                updatedRow = row.copy()
                updatedRow.update(changes or {})
                if not packScheDataIsValid(dataType, updatedRow):
                    return False
                return dataUpd(targetID, changes or {}, file, idField, fieldnames)
        print(f"No {dataType} with ID {targetID} found")
        return False
    if action == "r":
        return dataDel(targetID, file, idField, fieldnames)
    raise ValueError(f"{action} is not a supported {dataType} operation")

def packScheDataIsValid(dataType, row):
    if dataType == "service":
        try:
            if not math.isfinite(float(row["price"])) or float(row["price"]) <= 0:
                raise ValueError
            if not 1 <= int(row["C4"]) <= 1000:
                raise ValueError
        except (ValueError, TypeError):
            print("Service price must be greater than 0 and duration must be between 1 and 1000 minutes")
            return False
        if not row["service_name"].strip():
            print("Service name cannot be empty")
            return False
        return True

    try:
        datetime.strptime(row["date"], "%Y-%m-%d")
        startTime = datetime.strptime(row["start_time"], "%H:%M")
        endTime = datetime.strptime(row["end_time"], "%H:%M")
        if endTime <= startTime or not 1 <= int(row["available_slots"]) <= 1000:
            raise ValueError
    except (ValueError, TypeError):
        print("Enter a valid date, end time later than start time, and 1-1000 available slots")
        return False
    return True

def packSchePriceIsValid(value):
    try:
        return math.isfinite(float(value)) and float(value) > 0
    except (ValueError, TypeError):
        return False

def packScheTimeIsValid(startTime, endTime):
    try:
        return datetime.strptime(endTime, "%H:%M") > datetime.strptime(startTime, "%H:%M")
    except (ValueError, TypeError):
        return False

def inMgr(process):
    fileCheck(CREDENTIALS_file)
    with open(CREDENTIALS_file, "r") as employees:
        credentials = list(csv.DictReader(employees))
        #print(credentials)
    if process.lower() == "s":                                          #shows all employee data
        listData(CREDENTIALS_file)
        return()
    elif process.lower() == "a":                                        #add new employee
        newEmployeeName = input("Enter name of the new employee: ")     #assigns new employee name to variable with input prompt
        lastID = max(int(row["idnum"][2:]) for row in credentials)      #fetches largest employee ID number that exists
        newEmployeeId = f"SW{(4-len(str(lastID+1)))*"0"}{lastID+1}"     #iterates on largest employee ID number by 1 and assigns to variable
        print("The ID of the new employee is: ",newEmployeeId)          #confirms new employee name to user
        newEmployeePass = input("Set a password: ")                     #assigns employee login password to variable with input prompt
        with open(CREDENTIALS_file,"a") as employees:                   #writes new line to credentials file
            write = csv.DictWriter(employees,fieldnames=fieldnames)
            write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass,"perms":"employee"})
            print(f"New entry for {newEmployeeName} added")             #confirms to user new entry has been written to file
            return()
    elif process.lower() == "e":
        inMgr("S")
        selEmpy = input("Enter ID of employee you want to edit: ")
        exists = 0
        for ID in credentials:
            if ID["idnum"] == selEmpy:
                print(ID, "Found")
                exists = 1
                break
        if exists == 0:
            print("No employee with ID ", selEmpy, "found")
            return()
        empEdit(selEmpy)
    else:
        print(process, "is not a valid choice!, only A/S/E are accepted")

def empEdit(targetID):
    while True:
        sel = input_validation.get_non_empty_text_from_user(
            "Edit name (N)   Edit ID (I)   Edit password (P)   Delete employee (D)   Exit (X)")
        if sel.lower() == "n":
            newName = input_validation.get_non_empty_text_from_user("Enter new name: ")
            dataUpd(targetID, {"names": newName})
            print("Name updated to:", newName)
            break
        elif sel.lower() == "i":
            newID = input_validation.get_non_empty_text_from_user("Enter new employee ID: ")
            dataUpd(targetID, {"idnum": newID})
            targetID = newID
            print("ID updated to:", targetID)
            break
        elif sel.lower() == "p":
            newPass = input_validation.get_non_empty_text_from_user("Enter new password: ")
            dataUpd(targetID, {"pass": newPass})
            print("Password updated to:", newPass)
            break
        elif sel.lower() == "d":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this employee? (Y/N)")
                if confirmation == "Y":
                    dataDel(targetID)
                    print(f"Employee {targetID} deleted")
                    break
                elif confirmation == "N":
                    print("Operation cancelled")
                    break
                else:
                    print(confirmation, "is not a valid choice!, enter Y/N:")
                    continue
        elif sel.lower() == "x":
            break

def dataSave(file, fieldnames, rows):
    with open(file, "w", newline="") as dataFile:
        writer = csv.DictWriter(dataFile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def dataUpd(targetID, change, file=CREDENTIALS_file, idField="idnum", fieldnames=None):
    with open(file, "r", newline="") as dataFile:
        reader = csv.DictReader(dataFile)
        rows = list(reader)
        fieldnames = fieldnames or reader.fieldnames
    if fieldnames is None:
        return False
    for row in rows:
        if row[idField] == targetID:
            row.update(change)
            break
    else:
        return False
    dataSave(file, fieldnames, rows)
    return True

def dataDel(targetID, file=CREDENTIALS_file, idField="idnum", fieldnames=None):
    with open(file, "r", newline="") as dataFile:
        reader = csv.DictReader(dataFile)
        rows = list(reader)
        fieldnames = fieldnames or reader.fieldnames
    if fieldnames is None:
        return False
    ammended = [row for row in rows if row[idField] != targetID]
    if len(ammended) == len(rows):
        return False
    dataSave(file, fieldnames, ammended)
    return True

def dataview(process):
    if process.lower() == "c":
        fileCheck(CUSTOMERS_file)
        listData(CUSTOMERS_file)
        return()
    elif process.lower() == "b":
        fileCheck(BOOKING_file)
        listData(BOOKING_file)
        return()
    elif process.lower() == "p":
        fileCheck(PAYMENTS_file)
        listData(PAYMENTS_file)
        return()

def fileCheck(file):
    try:
        with open(file, "r") as f:
            return True
    except FileNotFoundError:
        print(file, "not found!!")
        return False

def listData(file):
    fileCheck(file)
    with open(file, "r") as f:
        data = list(csv.DictReader(f))
        for rows in data:
            print(rows)
        print("eof")
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