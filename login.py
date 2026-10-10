#login.py
import csv

from constants import CREDENTIALS_file

adminP="TP091031"
userMode=""

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

def logprompt():
    print("===Enter your login details===")
    logname = input("Name: ")
    logpass = input("Password: ")
    return(login(logname,logpass))
