from dataclasses import fields
from sys import prefix
from sys import prefix
from constants import PREBOOKING_file, SERVICES_file, BOOKING_file, PAYMENTS_file


# ---------------------------------------------------------------
# GENERIC FILE HELPERS
# The only functions that touch the disk directly.
# ---------------------------------------------------------------
def read_every_line(filename):
    """Reads every line of a file into a list of strings (no newlines)."""
    lines = []
    try:
        with open(filename, "r") as file:
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


def write_all_lines(filename, lines):
    """
    Overwrites the ENTIRE file with the given list of lines.
    Used to UPDATE an existing row (e.g. extending a
    booking) rather than just adding a new one.
    """
    try:
        with open(filename, "w") as file:
            for line in lines:
                file.write(line + "\n")
        return True
    except IOError:
        print(f"Error!!! Could not update {filename}.")
        return False

# ---------------------------------------------------------------
# INPUT VALIDATION HELPERS
# ---------------------------------------------------------------


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


def get_valid_email(prompt_message):
    """Very simple email check: must contain '@' and '.' """
    while True:
        value = input(prompt_message).strip()
        if "@" in value and "." in value:
            return value
        print("That doesn't look like a valid email (needs '@' and '.'). Please try again.")


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
        print("Please enter a valid time in HH:MM 24-hour format (e.g. 14:30).")

# ---------------------------------------------------------------
# FEATURE 1: VIEW AVAILABLE SERVICES SLOTS/ PACKAGES
# ---------------------------------------------------------------


def view_services():
    """Displays all the available services from services.csv as a simple table."""
    print("\n--- Available Services ---")
    services = read_every_line(SERVICES_file)

    if len(services) == 0:
        print("No services are currently available.")
        return

    print(f"{'ID':<6}{'Name':<33}{'Price (RM)':<12}{'Duration (min)':<15}")
    for line in services:
        fields = line.split(",")
        if len(fields) <= 4:
            continue
        service_id, name, price, duration = fields[0], fields[1], fields[2], fields[3]
        print(f"{service_id:<6}{name:<33}{price:<12}{duration:<15}")

# ---------------------------------------------------------------
# FEATURE 2: REQUEST A BOOKING OR AN EXTENSION
# ---------------------------------------------------------------
# To check if a service ID exists in the services.csv file (used when requesting a booking)


def service_exists(service_id_to_check):
    """Returns True if the given service_id is found in services.csv."""
    for line in read_every_line(SERVICES_file):
        fields = line.split(",")
        if fields[0].strip() == service_id_to_check:
            return True
    return False


def request_booking():
    """Collects details for a brand-new booking and send it to the officer for approval."""
    print("\n--- New Booking ---")
    view_services()

    while True:
        service_id = get_non_empty_text_from_user(
            "Enter the service ID you want to book: ")
        if service_exists(service_id):
            break
        print("That service ID doesn't exist. Please check the available services above.")

    date = get_valid_date_from_user("Enter your booking date (YYYY-MM-DD): ")
    time = get_valid_time_from_user("Enter your booking time (HH:MM): ")

    new_line = ','.join([service_id, date, time, "pending"])
    if append_line(PREBOOKING_file, new_line):
        print("Your booking request has been submitted for approval.")
    else:
        print("Something went wrong submitting your booking request. Please try again.")


def request_extension(customer_id):
    """Lets the customer pick one of their existing bookings and change its date/time."""
    print("\n--- Request an Extension ---")
    all_bookings = read_every_line(BOOKING_file)

    # Filter down to only this customer's bookings
    my_positions = []
    for position, line in enumerate(all_bookings):
        fields = line.split(",")
        if (len(fields) >= 1) and (fields[0].strip() == customer_id):
            my_positions.append(position)

    if len(my_positions) == 0:
        print("You have no existing bookings to extend.")
        return

    print("Your current bookings:")
    for display_number, position in enumerate(my_positions, start=1):
        fields = all_bookings[position].split(',')
        service_id, date, time, status = fields[1], fields[2], fields[3], fields[4]
        print(
            f"{display_number}.Service {service_id} on {date} at {time} (status: {status})")
    choice = get_menu_choice_from_user(1, len(my_positions))
    target_position = my_positions[choice - 1]
    new_date = get_valid_date_from_user("Enter the new date (YYYY-MM-DD): ")
    new_time = get_valid_time_from_user("Enter the new time (HH:MM): ")

    # Update ONLY that 1 row  in place then save the whole file back.
    fields = all_bookings[target_position].split(',')
    fields[2] = new_date
    fields[3] = new_time
    fields[4] = "extension_requested"
    all_bookings[target_position] = ','.join(fields)

    if write_all_lines(BOOKING_file, all_bookings):
        print(
            f"Booking updated to {new_date} {new_time} (status: extension_requested).")
    else:
        print("Something went wrong updating your booking. Please try again.")


def sub_menu_for_booking_menu():
    """Sub-menu: request a new booking or extension of an existing one."""
    print("\n--- Booking Menu ---")
    print("1. Request a new booking")
    print("2. Request an extension on an existing booking")
    print("3. Back to main menu")

    choice = get_menu_choice_from_user(1, 4)
    if choice == 1:
        request_booking()
    elif choice == 2:
        request_extension()
    else:
        customer_menu()  # Go back to the main customer menu


# ---------------------------------------------------------------
# FEATURE 3: VIEW BOOKING HISTORY AND INVOICES
# ---------------------------------------------------------------
def find_payment_for_booking(customer_id, services_id, date, time):
    """Returns the payment row (as a field list) matching this exact booking's customer_ id + services_id+date+time, or None if no payment has been recorded."""
    for line in read_every_line(PAYMENTS_file):
        fields = line.split(",")
        if (len(fields) < 7):
            continue
        pos_customer_id = fields[1].strip()
        pos_service_id = fields[2].strip()
        pos_date = fields[3].strip()
        pos_time = fields[4].strip()
        if (pos_customer_id == customer_id) and (pos_service_id == services_id) and (pos_date == date) and (pos_time == time):
            return fields
        return None


def view_history_and_invoices(customer_id):
    """Shows all of this customer's bookings, with payment info if available."""
    print("\n--- Your Booking History & Invoices ---")
    my_bookings = []
    for line in read_every_line(BOOKING_file):
        fields = line.split(",")
        if (len(fields) >= 1) and (fields[0].strip() == customer_id):
            my_bookings.append(fields)

    if len(my_bookings) == 0:
        print("You have no bookings yet.")
        return

    for fields in my_bookings:
        service_id, date, time, status = fields[1], fields[2], fields[3], fields[4]
        print(f"  Service ID: {service_id}")
        print(f"  Date/Time : {date} {time}")
        print(f"  Status    : {status}")

        payment = find_payment_for_booking(customer_id, service_id, date, time)
        if payment is not None:
            amount = float(payment[5])
            tax = amount * 0.06  # 6% tax
            total = amount + tax
            print(
                f"Invoice: RM{amount:.2f} + RM{tax:.2f} tax = RM{total:.2f} (status: {payment[6]})")
        else:
            print("Invoice: No payment recorded yet.")


# ---------------------------------------------------------------
# LOGGED-IN CUSTOMER MENU
# ---------------------------------------------------------------
def customer_menu():
    while True:
        print("\n===== ShineOnWheels: Customer Menu =====")
        print("1. View available services and slots")
        print("2. Request a booking or an extension")
        print("3. View service history and invoices")
        print("4. Log out")

        choice = get_menu_choice_from_user(1, 4)

        if choice == 1:
            view_services()
        elif choice == 2:
            sub_menu_for_booking_menu()
        elif choice == 3:
            view_history_and_invoices()
        elif choice == 4:
            print("Logged out.")
            break


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    # For testing purposes, I pass a dummy customer_id here
    customer_menu()
