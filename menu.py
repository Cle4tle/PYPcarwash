#menu system
import csv  # noqa: I001
import input_validation
import officer_roles
from constants import (
    BOOKING_file,
    CREDENTIALS_file,
    CUSTOMERS_file,
    PAYMENTS_file,
    SERVICES_file,
)

def inMgr(process):
    fileCheck(CREDENTIALS_file)
    with open(CREDENTIALS_file, "r") as employees:
        credentials = list(csv.DictReader(employees))
        #print(credentials)
    if process.lower() == "s":                                          #shows all employee data
        listData(CREDENTIALS_file)
        return()
    elif process.lower() == "a":                                        #add new employee
        newEmployeeName = input_validation.get_non_empty_text_from_user("Enter name of the new employee: ")     #assigns new employee name to variable with input prompt
        lastID = max((int(row["idnum"][2:]) for row in credentials), default=0)  #fetches largest employee ID number that exists
        newEmployeeId = f"SW{(4 - len(str(lastID + 1))) * "0"}{lastID + 1}"  #iterates on largest employee ID number by 1 and assigns to variable
        print("The ID of the new employee is: ",newEmployeeId)          #confirms new employee name to user
        newEmployeePass = input_validation.get_non_empty_text_from_user("Set a password: ")                     #assigns employee login password to variable with input prompt
        with open(CREDENTIALS_file,"a") as employees:                   #writes new line to credentials file
            write = csv.DictWriter(employees,fieldnames=["names","idnum","pass","perms"])
            if employees.tell() == 0:
                write.writeheader()
            write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass,"perms":"employee"})
            print(f"New entry for {newEmployeeName} added with ID: {newEmployeeId}")             #confirms to user new entry has been written to file
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
            print("Password updated")
            break
        elif sel.lower() == "d":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this employee? (YES/NO)")
                if confirmation == "YES":
                    dataDel(targetID)
                    print(f"Employee {targetID} deleted")
                    break
                elif confirmation == "NO":
                    print("Operation cancelled")
                    break
                else:
                    print(confirmation, "is not a valid choice!, enter YES/NO:")
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
    amended = [row for row in rows if row[idField] != targetID]
    if len(amended) == len(rows):
        return False
    dataSave(file, fieldnames, amended)
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
        with open(file, "r"):
            return True
    except FileNotFoundError:
        print(f"{file} not found. New file will be created.")
        with open(file, "w", newline="") as newFile:
            newFile.write("")
        print(f"Created new file: {file}")
        return True

def listData(file):
    fileCheck(file)
    with open(file, "r") as f:
        data = list(csv.DictReader(f))
        for rows in data:
            print(rows)
        print("eof")
        return()

def pkgMgr(process):
    fileCheck(SERVICES_file)
    with open(SERVICES_file, "r") as services:
        packages = list(csv.DictReader(services))
    if process.lower() == "s":                                          #shows all package data
        listData(SERVICES_file)
        return()
    elif process.lower() == "a":                                        #add new package
        newPkgName = input_validation.get_non_empty_text_from_user("Enter package name: ")
        lastID = max((int(row["service_id"][2:]) for row in packages), default=0)
        newPkgId = f"PK{(3 - len(str(lastID + 1))) * "0"}{lastID + 1}"
        print("The ID of the new package is: ", newPkgId)
        while True:
            try:
                newPkgDuration = int(input_validation.get_non_empty_text_from_user("Enter duration (minutes): "))
                newPkgPrice = float(input_validation.get_non_empty_text_from_user("Enter price: "))
                break
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        with open(SERVICES_file, "a", newline="") as services:
            write = csv.DictWriter(services, fieldnames=["service_id","service_name","price","duration"])
            if services.tell() == 0:
                write.writeheader()
            write.writerow({"service_name":newPkgName,"service_id":newPkgId,"price":newPkgPrice,"duration":newPkgDuration})
            print(f"New package {newPkgName} added with ID: {newPkgId} and duration: {newPkgDuration} minutes and price: {newPkgPrice}")
            return()
    elif process.lower() == "e":
        pkgMgr("s")
        selPkg = input("Enter ID of package you want to edit: ")
        exists = 0
        for ID in packages:
            if ID["service_id"] == selPkg:
                print(ID, "Found")
                exists = 1
                break
        if exists == 0:
            print("No package with ID ", selPkg, "found")
            return()
        pkgEdit(selPkg)
    else:
        print(process, "is not a valid choice!, only A/S/E are accepted")

def pkgEdit(targetID):
    while True:
        sel = input_validation.get_non_empty_text_from_user(
            "Edit name (N)   Edit ID (I)   Edit duration (D)   Edit price (P)   Delete package (X)   Exit (Q)")
        if sel.lower() == "n":
            newName = input_validation.get_non_empty_text_from_user("Enter new name: ")
            dataUpd(targetID, {"service_name": newName}, file=SERVICES_file)
            print("Name updated to:", newName)
            break
        elif sel.lower() == "i":
            newID = input_validation.get_non_empty_text_from_user("Enter new package ID: ")
            dataUpd(targetID, {"service_id": newID}, file=SERVICES_file)
            targetID = newID
            print("ID updated to:", targetID)
            break
        elif sel.lower() == "d":
            while True:
                try:
                    newDur = int(input_validation.get_non_empty_text_from_user("Enter new duration (minutes): "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
            dataUpd(targetID, {"duration": newDur}, file=SERVICES_file)
            print("Duration updated to:", newDur)
            break
        elif sel.lower() == "p":
            while True:
                try:
                    newPrice = float(input_validation.get_non_empty_text_from_user("Enter new price: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid number.")
                    continue
            dataUpd(targetID, {"price": newPrice}, file=SERVICES_file)
            print("Price updated to:", newPrice)
            break
        elif sel.lower() == "x":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this package? (YES/NO)")
                if confirmation == "YES":
                    dataDel(targetID, file=SERVICES_file)
                    print(f"Package {targetID} deleted")
                    break
                elif confirmation == "NO":
                    print("Operation cancelled")
                    break
                else:
                    print(confirmation, "is not a valid choice!, enter YES/NO:")
                    continue
        elif sel.lower() == "q":
            break

def schedMgr(process):
    fileCheck(BOOKING_file)
    with open(BOOKING_file, "r") as bookings:
        schedules = list(csv.DictReader(bookings))
    if process.lower() == "s":                                          #shows all booking data
        listData(BOOKING_file)
        return()
    elif process.lower() == "a":                                        #add new booking
        newCustMail = input_validation.get_non_empty_text_from_user("Enter customer email: ")
        newPkgID = input_validation.get_non_empty_text_from_user("Enter service package ID: ")
        newDate = input_validation.get_valid_date_from_user("Enter date (YYYY-MM-DD): ")
        newTime = input_validation.get_valid_time_from_user("Enter time slot (HH:MM): ")
        newBookingId = officer_roles.book_(newCustMail, newPkgID, newDate, newTime)
        print(f"New booking for {newCustMail} added with ID: {newBookingId} on {newDate} at {newTime}")
    elif process.lower() == "e":
        listData(BOOKING_file)
        selBook = input("Enter ID of booking you want to edit: ")
        exists = 0
        for ID in schedules:
            if ID["booking_id"] == selBook:
                print(ID, "Found")
                exists = 1
                break
        if exists == 0:
            print("No booking with ID ", selBook, "found")
            return()
        schedEdit(selBook)
    else:
        print(process, "is not a valid choice!, only A/S/E are accepted")

def schedEdit(targetID):
    while True:
        sel = input_validation.get_non_empty_text_from_user(
            "Edit customer (C)   Edit package (P)   Edit date (D)   Edit time (T)   Edit status (S)   Delete booking (X)   Exit (Q)")
        if sel.lower() == "c":
            newCust = input_validation.get_non_empty_text_from_user("Enter new customer email: ")
            dataUpd(targetID, {"email": newCust}, file=BOOKING_file)
            print("Customer email updated to:", newCust)
            break
        elif sel.lower() == "p":
            newPkg = input_validation.get_non_empty_text_from_user("Enter new service package ID: ")
            dataUpd(targetID, {"service_id": newPkg}, file=BOOKING_file)
            print("Package updated to:", newPkg)
            break
        elif sel.lower() == "d":
            newDate = input_validation.get_valid_date_from_user("Enter new date (YYYY-MM-DD): ")
            dataUpd(targetID, {"date": newDate}, file=BOOKING_file)
            print("Date updated to:", newDate)
            break
        elif sel.lower() == "t":
            newTime = input_validation.get_valid_time_from_user("Enter new time slot (HH:MM): ")
            dataUpd(targetID, {"time": newTime}, file=BOOKING_file)
            print("Time updated to:", newTime)
            break
        elif sel.lower() == "s":
            while True:
                newStatus = str(input_validation.get_non_empty_text_from_user("Enter new status (valid/completed/cancelled): "))
                if newStatus.lower() not in ["valid", "completed", "cancelled"]:
                    print("Invalid status. Please enter 'valid', 'completed', or 'cancelled'.")
                    continue
                break
            dataUpd(targetID, {"status": newStatus}, file=BOOKING_file)
            print("Status updated to:", newStatus)
            break
        elif sel.lower() == "x":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this booking? (YES/NO)")
                if confirmation == "YES":
                    dataDel(targetID, file=BOOKING_file)
                    print(f"Booking {targetID} deleted")
                    break
                elif confirmation == "NO":
                    print("Operation cancelled")
                    break
                else:
                    print(confirmation, "is not a valid choice!, enter YES/NO:")
                    continue
        elif sel.lower() == "q":
            break   

def reportGen(process):
    if process.lower() == "b":                                          #bookings report
        fileCheck(BOOKING_file)
        with open(BOOKING_file, "r") as bookings:
            data = list(csv.DictReader(bookings))
        if not data:
            print("No bookings found.")
            return()
        valid = sum(1 for row in data if row["status"].lower() == "valid")
        completed = sum(1 for row in data if row["status"].lower() == "completed")
        cancelled = sum(1 for row in data if row["status"].lower() == "cancelled")
        print("===Bookings Report===")
        print(f"Total bookings : {len(data)}")
        print(f"Valid          : {valid}")
        print(f"Completed      : {completed}")
        print(f"Cancelled      : {cancelled}")
        return()
    elif process.lower() == "r":                                        #revenue report
        fileCheck(BOOKING_file)
        fileCheck(SERVICES_file)
        with open(BOOKING_file, "r") as bookings:
            data = list(csv.DictReader(bookings))
        with open(SERVICES_file, "r") as services:
            svc = {row["service_id"]: float(row["price"]) for row in csv.DictReader(services)}
        if not data:
            print("No bookings found.")
            return()
        completed = [row for row in data if row["status"].lower() == "completed"]
        total = sum(svc.get(row["service_id"], 0) for row in completed)
        byService = {}
        for row in completed:
            sid = row["service_id"]
            byService[sid] = byService.get(sid, 0) + svc.get(sid, 0)
        print("===Revenue Report===")
        print(f"Completed bookings : {len(completed)}")
        print(f"Total revenue      : {total:.2f}")
        print("\nBy service:")
        for sid in sorted(byService):
            print(f"  {sid} : {byService[sid]:.2f}")
        return()
    elif process.lower() == "s":                                        #available slots
        fileCheck(BOOKING_file)
        targetDate = input_validation.get_valid_date_from_user("Enter date to check (YYYY-MM-DD): ")
        with open(BOOKING_file, "r") as bookings:
            data = list(csv.DictReader(bookings))
        booked = {row["time"] for row in data if row["date"] == targetDate and row["status"].lower() != "cancelled"}
        allSlots = [f"{h:02d}:00" for h in range(9, 17)]
        available = [slot for slot in allSlots if slot not in booked]
        print(f"===Available slots for {targetDate}===")
        if available:
            for slot in available:
                print(f"  {slot}")
        else:
            print("  Fully booked.")
        return()
    else:
        print(process, "is not a valid choice!, only B/R/S are accepted")   

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