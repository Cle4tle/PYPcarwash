#menu system
import csv  # noqa: I001
import accountant
import input_validation
import officer_roles
from constants import (
    BOOKING_file,
    CREDENTIALS_file,
    CUSTOMERS_file,
    PAYMENTS_file,
    SERVICES_file,)
credFields = ["names","idnum","pass","perms"]

def inMgr(process):
    fileCheck(CREDENTIALS_file)
    with open(CREDENTIALS_file, "r", newline="") as employees:
        credentials = list(csv.DictReader(employees))
    if process.lower() == "s":      #shows all employee data
        listData(CREDENTIALS_file)
        return()
    elif process.lower() == "a":        #add new employee
        newEmployeeName = input_validation.get_non_empty_text_from_user("Enter name of the new employee: ")     #assigns new employee name to variable with input prompt
        lastID = max((int(row["idnum"][2:]) for row in credentials), default=0)     #fetches largest employee ID number that exists after slicing SW prefix
        newEmployeeId = f"SW{(4 - len(str(lastID + 1))) * "0"}{lastID + 1}"     #increase max id by one, add prefix and leading 0s
        print("The ID of the new employee is: ",newEmployeeId)          #confirms new employee name to user
        newEmployeePass = input_validation.get_non_empty_text_from_user("Set a password: ")     #assigns employee login password to variable with input prompt

        with open(CREDENTIALS_file,"a", newline="") as employees:     #opens file to write new line
            write = csv.DictWriter(employees,fieldnames=credFields)
            if employees.tell() == 0:       #checks if file is empty to write header
                write.writeheader()
            write.writerow({"names":newEmployeeName,"idnum":newEmployeeId,"pass":newEmployeePass,"perms":"employee"})
            print(f"New entry for {newEmployeeName} added with ID: {newEmployeeId}")             #confirms to user new entry has been written to file
            return()
    elif process.lower() == "e":        #manage employee data entries
        listData(CREDENTIALS_file)      #lists employees for easy access
        while True:
            selEmpy = input("Enter ID of employee you want to edit: ")
            exists = 0
            for ID in credentials:
                if ID["idnum"] == selEmpy:
                    print(ID, "Found")
                    exists = 1
                    break
            if exists == 0:
                print("No employee with ID ", selEmpy, "found")
                continue
        empEdit(selEmpy)
    else:
        print(process, "is not a valid choice!, only A/S/E are accepted")

def empEdit(targetID):
    while True:
        sel = input_validation.get_non_empty_text_from_user(
            "Edit name (N)   Edit ID (I)   Edit password (P)   Delete employee (D)   Exit (X)")
        if sel.lower() == "n":
            newName = input_validation.get_non_empty_text_from_user("Enter new name: ")
            dataUpd(targetID, {"names": newName},CREDENTIALS_file,"idnum")
            print("Name updated to:", newName)
            break
        elif sel.lower() == "i":
            newID = input_validation.get_non_empty_text_from_user("Enter new employee ID: ")
            dataUpd(targetID, {"idnum": newID}, CREDENTIALS_file,"idnum")
            targetID = newID
            print("ID updated to:", targetID)
            break
        elif sel.lower() == "p":
            newPass = input_validation.get_non_empty_text_from_user("Enter new password: ")
            dataUpd(targetID, {"pass": newPass}, CREDENTIALS_file, "idnum")
            print("Password updated")
            break
        elif sel.lower() == "d":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this employee? (YES/NO)")
                if confirmation == "YES":           #only fully upper-cased yes or no are accepted to ensure user is paying attention and intend to delete
                    dataDel(targetID,CREDENTIALS_file,"idnum")
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

def dataSave(file, keyNames, rows):
    with open(file, "w", newline="") as dataFile:
        writer = csv.DictWriter(dataFile, fieldnames=keyNames)
        writer.writeheader()
        writer.writerows(rows)

def dataUpd(targetID, change, file, idField):
    with open(file, "r", newline="") as dataFile:
        reader = csv.DictReader(dataFile)
        rows = list(reader)
        fieldNames = reader.fieldnames
    for row in rows:        #check if user exists
        if row[idField] == targetID:
            row.update(change)
            break
    else:
        print(f"{targetID} not found!!")
        return False
    dataSave(file, fieldNames, rows)
    return True

def dataDel(targetID, file, idField):
    with open(file, "r", newline="") as dataFile:
        reader = csv.DictReader(dataFile)
        rows = list(reader)
        fieldnames = reader.fieldnames
    amended = [row for row in rows if row[idField] != targetID]     #copies every row except for the one for deletion into amended
    if len(amended) == len(rows):
        print(f"{targetID} not found!!")
        return False
    dataSave(file, fieldnames, amended)
    return True

def dataview(process):      #prints all data inside respective files
    if process.lower() == "c":
        listData(CUSTOMERS_file)
        return()
    elif process.lower() == "b":
        listData(BOOKING_file)
        return()
    elif process.lower() == "p":
        listData(PAYMENTS_file)
        return()

def fileCheck(file):        #checks if file exist, one will be created if it doesn't
    try:
        with open(file, "r", newline=""):
            return True
    except FileNotFoundError:
        print(f"{file} not found. New file will be created.")
        with open(file, "w", newline="") as newFile:
            newFile.write("")
        print(f"Created new file: {file}")
        return True

def listData(file):
    fileCheck(file)
    with open(file, "r", newline="") as f:
        data = list(csv.DictReader(f))
        for rows in data:
            print(rows)
        print("eof")
        return()

def pkgMgr(process):
    fileCheck(SERVICES_file)
    with open(SERVICES_file, "r", newline="") as services:
        packages = list(csv.DictReader(services))
    if process.lower() == "s":                                          #shows all package data
        listData(SERVICES_file)
        return()
    elif process.lower() == "a":                                        #add new package
        newPkgName = input_validation.get_non_empty_text_from_user("Enter package name: ")
        lastID = max((int(row["service_id"][2:]) for row in packages), default=0)       #gets largest id and strips prefix
        newPkgId = f"S{(3 - len(str(lastID + 1))) * "0"}{lastID + 1}"      #increase max id by one, add prefix and leading 0s
        print("The ID of the new package is: ", newPkgId)
        while True:
            try:
                newPkgDuration = int(input_validation.get_non_empty_text_from_user("Enter duration (minutes): "))
                newPkgPrice = float(input_validation.get_non_empty_text_from_user("Enter price: "))
                break
            except ValueError:
                print("Invalid input. Please only enter numbers.")
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
            dataUpd(targetID, {"service_name": newName}, SERVICES_file, "service_id")
            print("Name updated to:", newName)
            break
        elif sel.lower() == "i":
            newID = input_validation.get_non_empty_text_from_user("Enter new package ID: ")
            dataUpd(targetID, {"service_id": newID}, SERVICES_file, "service_id")
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
            dataUpd(targetID, {"duration": newDur}, SERVICES_file, "service_id")
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
            dataUpd(targetID, {"price": newPrice}, SERVICES_file, "service_id")
            print("Price updated to:", newPrice)
            break
        elif sel.lower() == "x":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this package? (YES/NO)")
                if confirmation == "YES":
                    dataDel(targetID, SERVICES_file, "service_id")
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
    with open(BOOKING_file, "r", newline="") as bookings:
        schedules = list(csv.DictReader(bookings))
    if process.lower() == "s":                                          #shows all booking data
        listData(BOOKING_file)
        return()
    elif process.lower() == "a":                                        #add new booking
        newCustMail = input_validation.get_valid_email_from_user("Enter customer email: ")
        newPkgID = input_validation.get_non_empty_text_from_user("Enter service package ID: ")
        newDate = input_validation.get_valid_date_from_user("Enter date (YYYY-MM-DD): ")
        newTime = input_validation.get_valid_time_from_user("Enter time slot (HH:MM): ")
        newBookingId = officer_roles.book_(newCustMail, newPkgID, newDate, newTime)     #calls book_ to add booking
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
            dataUpd(targetID, {"customer_email": newCust}, BOOKING_file, "booking_id")
            print("Customer email updated to:", newCust)
            break
        elif sel.lower() == "p":
            newPkg = input_validation.get_non_empty_text_from_user("Enter new service package ID: ")
            dataUpd(targetID, {"service_id": newPkg}, BOOKING_file, "booking_id")
            print("Package updated to:", newPkg)
            break
        elif sel.lower() == "d":
            newDate = input_validation.get_valid_date_from_user("Enter new date (YYYY-MM-DD): ")
            dataUpd(targetID, {"date": newDate}, BOOKING_file, "booking_id")
            print("Date updated to:", newDate)
            break
        elif sel.lower() == "t":
            newTime = input_validation.get_valid_time_from_user("Enter new time slot (HH:MM): ")
            dataUpd(targetID, {"time": newTime}, BOOKING_file, "booking_id")
            print("Time updated to:", newTime)
            break
        elif sel.lower() == "s":
            while True:
                newStatus = str(input_validation.get_non_empty_text_from_user("Enter new status (valid/completed/cancelled): "))
                if newStatus.lower() not in ["valid", "completed", "cancelled"]:
                    print("Invalid status. Please enter 'valid', 'completed', or 'cancelled'.")
                    continue
                break
            dataUpd(targetID, {"status": newStatus}, BOOKING_file, "booking_id")
            print("Status updated to:", newStatus)
            break
        elif sel.lower() == "x":
            while True:
                confirmation = input_validation.get_non_empty_text_from_user("Are you sure you want to delete this booking? (YES/NO)")
                if confirmation == "YES":
                    dataDel(targetID, BOOKING_file, "booking_id")
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
        with open(BOOKING_file, "r", newline="") as bookings:
            data = list(csv.DictReader(bookings))
        if not data:
            print("No bookings found.")
            return()
        valid = sum(1 for row in data if row["status"].lower() == "valid")
        completed = sum(1 for row in data if row["status"].lower() == "completed")
        cancelled = sum(1 for row in data if row["status"].lower() == "cancelled")
        print("====Bookings Report====",
            f"\nTotal bookings          : {len(data)}",
            f"\nFuture bookings         : {valid}",
            f"\nCompleted bookings      : {completed}",
            f"\nCancelled bookings      : {cancelled}")
        return()
    elif process.lower() == "r":                                        #revenue report
        print("===Revenue Report===")
        accountant.income_summary()
        return()
    elif process.lower() == "s":                                        #available slots
        fileCheck(BOOKING_file)
        targetDate = input_validation.get_valid_date_from_user("Enter date to check (YYYY-MM-DD): ")
        with open(BOOKING_file, "r", newline="") as bookings:
            data = list(csv.DictReader(bookings))
        booked = {
            row["time"]
            for row in data
            if row["date"] == targetDate
            and row["status"].lower() not in ("cancelled", "completed")
        }
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