#login.py
adminP="TP091031"
userMode=""

def login(ident,passkey):
    if ident == "admin" and passkey == adminP:
        userMode = "Administrator"
        return(userMode)
    else:
        for rows in employees:
            if ident == rows["names"] and passkey == index(rows)["pass"]:
                userMode = ""

