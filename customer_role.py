from dataclasses import fields
from sys import prefix
from sys import prefix
from constants import SERVICES_file, BOOKING_file, PAYMENTS_file


TAX_RATE = 0.06
ID_LENGTH = 4  # All IDs are 4-digit numbers, e.g. 0001, 0002

# File format reference (comma-separated, one record per line):
# services.csv   -> service_id,name,price,duration_minutes
# customers.csv  -> customer_id,name,phone,email,password
# bookings.csv   -> booking_id,customer_id,service_id,date,time,status
# payments.csv   -> payment_id,booking_id,amount,date,status


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


def get_menu_choice(min_num, max_num):
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


def get_non_empty_text(prompt_message):
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


def get_valid_date(prompt_message):
    """Expects format YYYY-MM-DD, e.g. 2026-09-20."""
    while True:
        value = input(prompt_message).strip()
        parts = value.split("-")
        if (len(parts) == 3) and (all(part.isdigit() for part in parts)):
            year, month, day = parts
            if (len(year) == 4) and (1 <= int(month) <= 12) and (1 <= int(day) <= 31):
                return value
        print("Please enter a valid date in YYYY-MM-DD format (e.g. 2026-09-20).")


def get_valid_time(prompt_message):
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
# ID GENERATION HELPER
# ---------------------------------------------------------------


def generate_new_id(filename, prefix="", id_length=ID_LENGTH):
    """
    Looks back at the first field (the ID column) of every existing row
    and returns the next sequential ID, zero-padded to id_length.

    Pass a prefix to generate letter-coded IDs, e.g.
    generate_new_id(BOOKING_file, prefix="B", id_length=3) reads
    existing rows like B001, B002, B003 and returns "B004".

    With no prefix (the default) it behaves as before and returns
    a plain zero-padded number, e.g. "0001".
    """
    max_number = 0
    for line in read_every_line(filename):
        fields = line.split(",")
        if len(fields) == 0:
            continue
        current_id = fields[0].strip()
        if prefix:
            if not current_id.startswith(prefix):
                continue  # skip IDs that don't use this prefix
            number_part = current_id[len(prefix):]
        else:
            number_part = current_id

        if number_part.isdigit():
            number = int(number_part)
            if (number) > (max_number):
                max_number = number
        # non-numeric or malformed rows are skipped instead of crashing

    new_number = max_number + 1
    return prefix + str(new_number).zfill(id_length)
# ---------------------------------------------------------------
# FEATURE 1: VIEW SERVICES / SLOTS
# ---------------------------------------------------------------


def view_services():
    """Displays all available services from services.csv as a simple table."""
    print("\n--- Available Services ---")
    services = read_every_line(SERVICES_file)

    if len(services) == 0:
        print("No services are currently available.")
        return

    print(f"{'ID':<6}{'Name':<33}{'Price (RM)':<12}{'Duration (min)':<15}")
    for line in services:
        fields = line.split(",")
        if len(fields) < 4:
            continue
        service_id, name, price, duration = fields[0], fields[1], fields[2], fields[3]
        print(f"{service_id:<6}{name:<33}{price:<12}{duration:<15}")


def service_exists(service_id_to_check):
    """Returns True if the given service_id is found in services.csv."""
    for line in read_every_line(SERVICES_file):
        fields = line.split(",")
        if (len(fields) > 0) and (fields[0].strip() == service_id_to_check):
            return True
    return False

# ---------------------------------------------------------------
# FEATURE 2: MAKE A BOOKING / REQUEST AN EXTENSION
# ---------------------------------------------------------------


def create_new_booking(customer_id):
    """Collects details for a brand-new booking and appends it to bookings.csv."""
    print("\n--- New Booking ---")
    view_services()

    while True:
        service_id = get_non_empty_text(
            "Enter the service ID you want to book: ")
        if service_exists(service_id):
            break
        print("That service ID doesn't exist. Please check the list above.")

    date = get_valid_date("Enter booking date (YYYY-MM-DD): ")
    time = get_valid_time("Enter booking time (HH:MM): ")

    new_id = generate_new_id(BOOKING_file)
    # Field order: booking_id,customer_id,service_id,date,time,status
    new_line = ",".join(
        [(new_id), customer_id, service_id, date, time, "pending"])

    if append_line(BOOKING_file, new_line):
        print(
            f"Booking request submitted! Your booking ID is {new_id} (status: pending).")
    else:
        print("Something went wrong saving your booking. Please try again.")


def request_extension(customer_id):
    """Lets the customer pick one of their existing bookings and change its date/time."""
    print("\n--- Request an Extension ---")
    all_bookings = read_every_line(BOOKING_file)

    # Filter down to only this customer's bookings
    my_bookings = []
    for line in all_bookings:
        fields = line.split(",")
        if (len(fields) >= 2) and (fields[1].strip() == customer_id):
            my_bookings.append(line)

    if len(my_bookings) == 0:
        print("You have no existing bookings to extend.")
        return

    print("Your current bookings:")
    for line in my_bookings:
        fields = line.split(",")
        print(
            f"Booking ID {fields[0]} - {fields[3]} {fields[4]} (status: {fields[5]})")

    target_id = get_non_empty_text("Enter the booking ID you want to extend: ")

    # Confirm that booking ID actually belongs to this customer
    found = False
    for line in my_bookings:
        fields = line.split(",")
        if fields[0].strip() == target_id:
            found = True
            break

    if not found:
        print("That booking ID was not found under your account.")
        return

    new_date = get_valid_date("Enter the new date (YYYY-MM-DD): ")
    new_time = get_valid_time("Enter the new time (HH:MM): ")

    # Rebuild the ENTIRE bookings file, replacing only the matching row
    updated_lines = []
    for line in all_bookings:
        fields = line.split(",")
        if (fields[0].strip() == target_id) and (fields[1].strip() == customer_id):
            fields[3] = new_date
            fields[4] = new_time
            fields[5] = "extension_requested"
            updated_lines.append(",".join(fields))
        else:
            updated_lines.append(line)

    if write_all_lines(BOOKING_file, updated_lines):
        print(
            f"Booking {target_id} updated to {new_date} {new_time} (status: extension_requested).")
    else:
        print("Something went wrong updating your booking. Please try again.")


def make_booking(customer_id):
    """Sub-menu: new booking or extension of an existing one."""
    print("\n--- Booking Menu ---")
    print("1. Request a new booking")
    print("2. Request an extension on an existing booking")
    print("3. Back to main menu")

    choice = get_menu_choice(1, 3)
    if choice == 1:
        create_new_booking(customer_id)
    elif choice == 2:
        request_extension(customer_id)
    # choice == 3 just returns to caller


# ---------------------------------------------------------------
# FEATURE 3: VIEW BOOKING HISTORY AND INVOICES
# ---------------------------------------------------------------
def find_payment_for_booking(booking_id):
    """Returns the payment line matching a booking_id, or None if not found."""
    for line in read_every_line(PAYMENTS_file):
        fields = line.split(",")
        if (len(fields) >= 2) and (fields[1].strip() == booking_id):
            return fields
    return None


def view_history_and_invoices(customer_id):
    """Shows all of this customer's bookings, with payment info if available."""
    print("\n--- Your Booking History & Invoices ---")
    my_bookings = []
    for line in read_every_line(BOOKING_file):
        fields = line.split(",")
        if (len(fields) >= 2) and (fields[1].strip() == customer_id):
            my_bookings.append(fields)

    if len(my_bookings) == 0:
        print("You have no bookings yet.")
        return

    for fields in my_bookings:
        booking_id, service_id, date, time, status = fields[
            0], fields[2], fields[3], fields[4], fields[5]
        print(f"\nBooking ID: {booking_id}")
        print(f"  Service ID: {service_id}")
        print(f"  Date/Time : {date} {time}")
        print(f"  Status    : {status}")

        payment = find_payment_for_booking(booking_id)
        if payment is not None:
            amount = float(payment[2])
            tax = amount * TAX_RATE
            total = amount + tax
            print(
                f"Invoice: RM{amount:.2f} + RM{tax:.2f} tax = RM{total:.2f} (status: {payment[4]})")
        else:
            print("Invoice: No payment recorded yet.")


# ---------------------------------------------------------------
# LOGGED-IN CUSTOMER MENU
# ---------------------------------------------------------------
def customer_menu(customer_id):
    while True:
        print("\n===== ShineOnWheels: Customer Menu =====")
        print("1. View available services and slots")
        print("2. Make a booking / request an extension")
        print("3. View my booking history and invoices")
        print("4. Log out")

        choice = get_menu_choice(1, 4)

        if choice == 1:
            view_services()
        elif choice == 2:
            make_booking(customer_id)
        elif choice == 3:
            view_history_and_invoices(customer_id)
        elif choice == 4:
            print("Logged out.")
            break


# ---------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------
if __name__ == "__main__":
    # For testing purposes, I just pass a dummy customer_id here
    customer_menu(customer_id="0001")
