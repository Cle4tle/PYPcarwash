#main program
import csv
import login
import menu
import officer_roles as officer
import accountant
import input_validation as inp_v
fieldnames=["names","idnum","pass","perms"]
services_names_list = []# [TODO] : fill this with our services
services_ids = [1,2,3,4,5]# [TODO] if these aren't the correct services ids correct them

'''NOTE : if any one of you guys have their own sub_menu u can place it in its proper place
      REPEAT [proper place]'''
'''Now everyone must read the logic of the program and add the things that they worked on to make the program fully functional.
    i got the idea of the menus from real car wash websites online.
     but please dont blindly copy past to AI cuz it will probably mess it up real bad!
     the validation functions should be done on a file and then imported here.
     NOW Get to work its not frikin rocket science!!!!!!!!!!!!!!!!!'''

'''TIP : just run the program to understand it'''
def sub_menu_customer():
      print("1.Register")
      print("2.log in")
      print("0.return")
      index = inp_v.get_menu_choice_from_user(0,2)
      if index == 1:
            print("-----Register-----")
            name = input("name: ")
            email = input("Email: ")  # [TODO] : replace input() with a proper validate function
            phone = inp_v.get_phone_number_from_user("Phone Number: ")
            res = officer.register_customer(name, email, phone)
            if not res:
                print("account already exists Try Logging In")
                return "rep"
            else:
                return True
      elif index == 2:
            print("-----Log In-----")
            #[TODO]: the Log in logic flow i still didnt understand so whoever did it handle this
            return True
      elif index == 0:
            return False
def sub_menu_customer_services():

            '''[TODO] : print all of our services in this format :
                             1. #######
                             2. @@@@@@@
                             3. $$$$$$$
                             .
                             .
                             .
                             0.return
                this will be implemented by iterating over the services List (see line 7)
                             '''
            serv_id = input( "Select a service and Book Now! or select (0) to return : ")  # [TODO] : replace input() with a proper validate function
            if serv_id == "0":
                 return False
            else:
                email = input("Email: ")# [TODO] : replace input() with a proper validate function
                date = inp_v.get_valid_date_from_user("Date YYYY-MM-DD: ")
                time = inp_v.get_valid_time_from_user("Time HH:MM: ")
                choice = input("Confirm Booking to this email ? (Y/N): ")# [TODO] : replace input() with a proper validate function
                if choice == "Y":
                    if not officer.verify_booking(email):
                        print("Booking Failed!! this account have maximum number of bookings")
                        return False
                    else:
                        print("Booking Successful!")
                        officer.book_(email, serv_id, date, time)
                        return False
                elif choice == "N":
                    return False
def sub_menu_booking_process():
    eml = input("Email: ")  # [TODO] : replace input() with a proper validate function
    while True:
        officer.view_booking_by_id(eml)
        id_ = input("Enter the Booking ID from above to perform operation: ")# [TODO] : replace input() with a proper validate function
        op = inp_v.get_spcific_text_from_user("choose operation (C) cancel, (R) reschedule, (Q) to quit: ")# [TODO] : replace input() with a proper validate function

        if op == "c":
            officer.cancel_booking(id_)
            print("canceled successfully")
        elif op == "r":
            date = inp_v.get_valid_date_from_user("Enter the date (YY/MM/DD): ")
            time = inp_v.get_valid_time_from_user("Enter the time (HH:MM): ")
            officer.reschedule_booking(id_, date, time)
        elif op == "q":
            break

def sub_menu_packsche():
    while True:
        process = menu.menuDial("packsche").strip().lower()
        if process == "x":
            return
        elif process == "p":
            dataType = "service"
            idField = "service_id"
        elif process == "s":
            dataType = "schedule"
            idField = "schedule_id"
        else:
            print(process, "is not a valid choice!, only P/S/X are accepted")
            continue

        while True:
            action = inp_v.get_non_empty_text_from_user(
                f"Add {dataType} (A)   Update {dataType} (U)   Remove {dataType} (R)   Exit (X): ").lower()
            if action == "x":
                break
            if action not in ("a", "u", "r"):
                print(action, "is not a valid choice!, only A/U/R/X are accepted")
                continue

            rows = menu.packScheMgr(process, "s")
            if action == "a":
                if process == "p":
                    changes = {"service_name": inp_v.get_non_empty_text_from_user("Enter service name: ")}
                    while True:
                        price = inp_v.get_non_empty_text_from_user("Enter service price: ")
                        if menu.packSchePriceIsValid(price):
                            changes["price"] = price
                            break
                        print("Please enter a number greater than 0")
                    changes["C4"] = str(inp_v.get_menu_choice_from_user(1, 1000))
                else:
                    changes = {"date": inp_v.get_valid_date_from_user("Enter schedule date (YYYY-MM-DD): ")}
                    changes["start_time"] = inp_v.get_valid_time_from_user("Enter start time (HH:MM): ")
                    while True:
                        changes["end_time"] = inp_v.get_valid_time_from_user("Enter end time (HH:MM): ")
                        if menu.packScheTimeIsValid(changes["start_time"], changes["end_time"]):
                            break
                        print("End time must be later than start time")
                    changes["available_slots"] = str(inp_v.get_menu_choice_from_user(1, 1000))
                newID = menu.packScheMgr(process, "a", changes=changes)
                if newID:
                    print(f"New {dataType} added with ID {newID}")
                continue

            if not rows:
                print(f"No {dataType}s found")
                continue
            for row in rows:
                print(row)
            targetID = inp_v.get_non_empty_text_from_user(
                f"Enter {dataType} ID to {action}: ")
            for row in rows:
                if row[idField] == targetID:
                    targetRow = row
                    break
            else:
                print(f"No {dataType} with ID {targetID} found")
                continue

            if action == "u":
                changes = {}
                if process == "p":
                    edit = inp_v.get_non_empty_text_from_user(
                        "Edit name (N)   Edit price (P)   Edit duration (D): ").lower()
                    if edit == "n":
                        changes["service_name"] = inp_v.get_non_empty_text_from_user("Enter new service name: ")
                    elif edit == "p":
                        while True:
                            price = inp_v.get_non_empty_text_from_user("Enter new service price: ")
                            if menu.packSchePriceIsValid(price):
                                changes["price"] = price
                                break
                            print("Please enter a number greater than 0")
                    elif edit == "d":
                        changes["C4"] = str(inp_v.get_menu_choice_from_user(1, 1000))
                    else:
                        print(edit, "is not a valid choice!, only N/P/D are accepted")
                        continue
                else:
                    edit = inp_v.get_non_empty_text_from_user(
                        "Edit date (D)   Edit start time (S)   Edit end time (E)   Edit available slots (A): ").lower()
                    if edit == "d":
                        changes["date"] = inp_v.get_valid_date_from_user("Enter new date (YYYY-MM-DD): ")
                    elif edit == "s" or edit == "e":
                        newTime = inp_v.get_valid_time_from_user("Enter new time (HH:MM): ")
                        startTime = newTime if edit == "s" else targetRow["start_time"]
                        endTime = targetRow["end_time"] if edit == "s" else newTime
                        if not menu.packScheTimeIsValid(startTime, endTime):
                            print("Start time must be earlier than end time" if edit == "s"
                                  else "End time must be later than start time")
                            continue
                        changes["start_time" if edit == "s" else "end_time"] = newTime
                    elif edit == "a":
                        changes["available_slots"] = str(inp_v.get_menu_choice_from_user(1, 1000))
                    else:
                        print(edit, "is not a valid choice!, only D/S/E/A are accepted")
                        continue
                if menu.packScheMgr(process, "u", targetID, changes):
                    print(f"{dataType.title()} {targetID} updated")
            else:
                confirmation = inp_v.get_non_empty_text_from_user(
                    f"Are you sure you want to remove {dataType} {targetID}? (Y/N): ")
                if confirmation.lower() == "y":
                    if menu.packScheMgr(process, "r", targetID):
                        print(f"{dataType.title()} {targetID} removed")
                else:
                    print("Operation cancelled")

def main_menu():

    print(f"=========ShineOnWheels========="
          f"\nWelcome to Shine On Wheels!"
          f"\nLogin as a customer or employee.\n")
    print("1. Customer")
    print("2. employee")
    print("0. exit")
    choice = inp_v.get_menu_choice_from_user(0,2)
    return choice

def main():
      while True:
          choice = main_menu()
          if choice == 1:
                while True:
                  running = sub_menu_customer()
                  if running == "rep":
                      continue
                  if not running:
                      break
                  while True:
                        print("1. Check out our Services")
                        print("2. View Bookings")
                        print("0. return")
                        choice = input("Enter your choice: ") # [TODO] : replace input() with a proper validate function
                        if choice == "1":
                             choice_s = sub_menu_customer_services()
                             if not choice_s:
                                 continue
                        elif choice == "2":
                             sub_menu_booking_process()
                        elif choice == "0":
                             break

          elif choice == 2:
                while True:
                    print("-----Employee-----")
                    print("1. Accountant")
                    print("2. Packages and schedules")
                    # Add roles related to employee here
                    print("0. return")
                    emp_choice = inp_v.get_menu_choice_from_user(0,2)
                    if emp_choice == 1:
                        accountant.accountant_menu()
                    elif emp_choice == 2:
                        sub_menu_packsche()
                    elif emp_choice == 0:
                        break  #  back to main menu
          elif choice == 0:
            return False

if __name__ == "__main__":
       isrunning = True
       while isrunning:
           isrunning =  main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
