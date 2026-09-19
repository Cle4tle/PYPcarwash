#login.py
from constants import CREDENTIALS


adminP="TP091031"
userMode=""

def login(ident,passkey):
    with open(CREDENTIALS_file) as credentials:
        authbase = [row for row in csv.DictReader(credentials)]
    if ident == "admin" and passkey == adminP:
        userMode = "Administrator"
        return(userMode)
    else:
        for rows in authbase:
            if ident == rows["names"] and passkey == index(rows)["pass"]:
                if rows["perms"] == "employee":
                    userMode = "employee"
                elif rows["perms"] == "customer":
                    userMode = "customer"

