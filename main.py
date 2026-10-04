#main program
import csv
import login
import menu
import officer_roles as officer
fieldnames=["names","idnum","pass","perms"]
services_names_list = []# [TODO] : fill this with our services
services_ids = [1,2,3,4, 5]# [TODO] if these aren't the correct services ids correct them

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
      index = input("choose a number: ") # [TODO] : replace input() with a proper validate function
      if index == "1":
            print("-----Register-----")
            name = input("name: ")  # [TODO] : replace input() with a proper validate function
            email = input("Email: ")  # [TODO] : replace input() with a proper validate function
            phone = input("Phone Number: ")  # [TODO] : replace input() with a proper validate function
            res = officer.register_customer(name, email, phone)
            if not res:
                print("account already exists Try Logging In")
                return "rep"
            else:
                return True
      elif index == "2":
            print("-----Log In-----")
            #[TODO]: the Log in logic flow i still didnt understand so whoever did it handle this
            return True
      elif index == "0":
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
                date = input("Date (YY/MM/DD): ")# [TODO] : replace input() with a proper validate function
                time = input("Time (HH:MM): ")# [TODO] : replace input() with a proper validate function
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
        #[TODO] : right now the above function only displays the bookings without the pyament paid or any details
         # whoever un charge of this please include those details without missing up the logic

        id_ = input("Enter the Booking ID from above to perform operation: ")# [TODO] : replace input() with a proper validate function
        op = input("choose operation (C) cancel, (R) reschedule, (Q) to quit: ").strip().upper()# [TODO] : replace input() with a proper validate function

        if op == "C":
            officer.cancel_booking(id_)
            print("canceled successfully")
        elif op == "R":
            date = input("Enter the date (YY/MM/DD): ")# [TODO] : replace input() with a proper validate function
            time = input("Enter the time (HH:MM): ")# [TODO] : replace input() with a proper validate function
            officer.reschedule_booking(id_, date, time)

        elif op == "Q":
            break
def main_menu():

    print(f"=========ShineOnWheels========="
          f"\nWelcome to Shine On Wheels!"
          f"\nLogin as a customer or employee.\n")
    print("1. Customer")
    print("2. employee")
    print("0. exit")
    choice = input("Enter your choice: ")  # [TODO] : replace input() with a proper validate function
    return choice

def main():
      while True:
          choice = main_menu()
          if choice == "1":
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
          elif choice == "2":
                    ''' [TODO] : everyone who's in charge of something related to employee handle this '''
          else:
              return False

if __name__ == "__main__":
       isrunning = True
       while isrunning:
           isrunning =  main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
