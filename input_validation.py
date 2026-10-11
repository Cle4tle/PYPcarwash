from constants import CUSTOMERS_file, SERVICES_file


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

    while True:
        try:
            number = input(prompt_message)
            if len(number) != 10:
                print("Please enter a valid phone number.")
            else:
                return int(number)
        except ValueError:
            print("Please enter a valid phone number.")


def get_Y_or_N_from_user(prompt_message):
    """Keeps asking until the user types a letter that is wanted"""
    while True:
        value = input(prompt_message).strip().lower()
        if len(value) != 1:
            print("Please enter a single letter.")
            continue
        if value != "y" or value != "n":
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
            return email  # means valid
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

# Check if a customer ID exists in the customers.csv file


def customer_id_exists(customer_id_to_check):
    """Returns True if the given customer_id is found in customers.csv."""
    for line in read_file(CUSTOMERS_file):
        fields = line.split(",")
        if fields[0] == customer_id_to_check:
            return True
    return False
# Check if a service ID exists in the services.csv file


def service_exists(service_id_to_check):
    """Returns True if the given service_id is found in services.csv."""
    for line in read_file(SERVICES_file):
        fields = line.split(",")
        if fields[0] == service_id_to_check:
            return True
    return False


def read_file(filename):
    """Reads every line of a file into a list of strings (no newlines)."""
    lines = []
    try:
        with open(filename, "r") as file:
            next(file)  # Skip the header line
            for line in file:
                cleaned_line = line.strip()
                if cleaned_line != "":
                    lines.append(cleaned_line)
    except FileNotFoundError:
        print(f"Notice: {filename} not found. Treating it as empty.")
    except IOError:
        print(f"Error!!! Could not read {filename}.")
    return lines


def append_line(filename, line_text):
    """Adds one new line to the end of a file."""
    try:
        with open(filename, "a") as file:
            file.write(line_text + "\n")
        return True
    except IOError:
        print(f"Error!!! Could not write to {filename}.")
        return False
