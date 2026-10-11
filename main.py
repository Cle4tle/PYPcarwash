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

def login(ident,passkey):
    global userMode
    with open(CREDENTIALS_file) as credentials:
        authBase = [row for row in csv.DictReader(credentials)]
    if ident == "admin" and passkey == adminP:
        userMode = "Administrator"
        return userMode
    for rows in authBase:
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
                pass

          elif choice == 2:
                while True:
                    print("-----Enter your login details-----")
                    logName = input("Name: ")
                    logPass = input("Password: ")
                    logged_in_as = login(logName,logPass)
                    # Add roles related to employee here
                    if logged_in_as == "Administrator":
                        foobar()
                    elif logged_in_as == "employee":
                        foobar()
                    elif logged_in_as == "customer":
                        foobar()

          elif choice == 0:
            return False

if __name__ == "__main__":
       isrunning = True
       while isrunning:
           isrunning =  main()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
