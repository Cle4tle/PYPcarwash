def get_menu_choice_from_user(min_num, max_num):
    """Keeps asking until the user gives a valid whole number in range."""
    while True:
        raw_value = input(f"Enter your choice ({min_num}-{max_num}): ")
        try:
            choice = int(raw_value)
            if min_num <= choice <= max_num:
                return choice
            print(
                f"Please enter a number between {min_num} and {max_num}.")
        except ValueError:
            print("That's not a valid number. Please try again.")
def get_non_empty_text_from_user(prompt_message):
    """Keeps asking until the user types something that isn't blank."""
    while True:
        value = input(prompt_message).strip()
        if value != "":
            return value
        print("This field cannot be empty. Please try again.")

def get_valid_date_from_user(prompt_message):
    """Expects format YYYY-MM-DD, e.g. 2026-09-20."""
    while True:
        value = input(prompt_message).strip()
        parts = value.split("-")
        if (len(parts) == 3) and (all(part.isdigit() for part in parts)):
            year, month, day = parts
            if (len(year) == 4) and (1 <= int(month) <= 12) and (1 <= int(day) <= 31):
                return value
        print("Please enter a valid date in YYYY-MM-DD format (e.g. 2026-09-20).")
def get_valid_time_from_user(prompt_message):
    """Expects format HH:MM (24-hour), e.g. 14:30."""
    while True:
        value = input(prompt_message).strip()
        parts = value.split(":")
        if (len(parts) == 2) and (all(part.isdigit() for part in parts)):
            hour, minute = int(parts[0]), int(parts[1])
            if (0 <= hour <= 23) and (0 <= minute <= 59):
                return value
        print("Please enter a valid time in HH:MM 24-hour format (e.g. 14:30). Our operating hours are from 10:00 to 20:00.")
def get_phone_number_from_user(prompt_message):
    '''keeps asking until the user types a valid phone number.'''
    while True:
        try:
            number = input(prompt_message).strip().replace(" ", "")
            if len(number) != 11:
                print("Please enter a valid phone number.")
            else:
                return number
        except ValueError:
            print("Please enter a valid phone number.")
def get_spcific_text_from_user(prompt_message):
    """Keeps asking until the user types a letter that is wanted"""
    while True:
        value = input(prompt_message).strip().lower()
        if len(value) != 1:
            print("Please enter a single letter.")
            continue
        if value != "c" or value != "r" or value != "q":
            if value == "":
                print("This field cannot be empty. Please try again.")
            print("Please enter one of the specified Letters.")
        else:
           return value
           break
def get_valid_email_from_user(prompt_message):
    """Expects format E-Mail."""
    while True:
           value = input(prompt_message).strip().split("@")

           dig_count = 0
           char_count = 0
           for i in range(len(value[0])):
               if value[0][i].isdigit():
                   dig_count += 1
               elif value[0][i].isalpha():
                   char_count += 1
               else:
                   print("invalid!, please enter a valid email address.")
                   continue
           if 15 >= len(value[0]) >= 5 >= dig_count >= 0 and 6 <= char_count <= 15:
               email = value[0]+"@" + value[1]
               return email# means valid
           else:
               if not 5 >= dig_count >= 0:
                    print("invalid!, too many digits.")
               elif len(value[0]) > 13:
                   print("invalid!, too long.")
               elif len(value[0]) < 5:
                   print("invalid!,  too short.")
               elif char_count > 15:
                   print("invalid!, too many characters.")
               continue
           verify_gmail = s[1].split(".")

           if verify_gmail[0] == "gmail" and verify_gmail[1] == "com":
               email = value[0] + value[1]
               return email  # means valid
           else:
               print("invalid!, please enter a valid email address.")



