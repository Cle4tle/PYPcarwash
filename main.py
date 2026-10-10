#main program
import accountant
import input_validation as inp_v
import menu
import officer_roles as officer
import csv
from constants import CREDENTIALS_file

adminP="TP091031"
userMode= None
fieldnames=["names","idnum","pass","perms"]
services_names_list = []# [TODO] : fill this with our services
services_ids = ["S001", "S002","S003", "S004","S005"]# [TODO] if these aren't the correct services ids correct them

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
      print("0.return")
      index = inp_v.get_menu_choice_from_user(0,1)
      if index == 1:
            print("-----Register-----")
            name = inp_v.get_non_empty_text_from_user("name: ")
            email = inp_v.get_non_empty_text_from_user("Email: ")  # [TODO] : replace input() with a proper validate function
            phone = inp_v.get_phone_number_from_user("Phone Number: ")
            res = officer.register_customer(name, email, phone)
            if not res:
                print("account already exists Try Logging In")
                return "rep"
            else:
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

def login(ident,passkey):
    userMode = None
    with open(CREDENTIALS_file) as credentials:
        authbase = [row for row in csv.DictReader(credentials)]
    if ident == "admin" and passkey == adminP:
        userMode = "Administrator"
        return userMode
    else:
        for rows in authbase:
            if ident == rows["names"] and passkey == rows["pass"]:
                userMode = rows["perms"]
                break
        return userMode

def main_menu():

    print("=========ShineOnWheels=========",
          "\nWelcome to Shine On Wheels!",
          "\nRegister as a customer or log into an existing account")
    print("1. Register")
    print("2. Login")
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
                        foobar()
                    elif emp_choice == 0:
                        break  #  back to main menu
          elif choice == 0:
            return False

if __name__ == "__main__":
       isrunning = True
       while isrunning:
           isrunning =  main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
