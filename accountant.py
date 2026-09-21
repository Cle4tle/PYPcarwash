"""
ShineOnWheels - Accountant Module
--------------------------------
Plain functions only (no classes/OOP), text/CSV files for storage,
command-line menu. No external libraries - all parsing is done
manually with .split() and string building.
"""
import os
from datetime import datetime

# ---------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------
SERVICES_FILE = "services.csv"
CUSTOMERS_FILE = "customers.csv"
BOOKINGS_FILE = "bookings.csv"
PAYMENTS_FILE = "payments.csv"

FIELD_SEPARATOR = ","
TAX_RATE = 0.06
ID_LENGTH = 4  # All IDs are 4-digit numbers, e.g. 0001, 0002

PAYMENT_METHODS = ["CASH","Card","Online Transfer", "E-Wallet"]
LATE_FEE = 10.00 # Added to the service price for late booking
NOT_SHOWING_FEE = 20.00 # Added to the service price if the user not come even though he already booked

# File format reference (comma-separated, one record per line):
# services.csv   -> service_id,name,price,duration_minutes
# customers.csv  -> customer_id,name,phone,email,password
# bookings.csv   -> booking_id,customer_id,service_id,date,time,status
# payments.csv   -> payment_id,booking_id,amount,date,status

SV_ID, SV_NAME, SV_PRICE, SV_DURATION = range(4)           #Field positions and headers for services.csv
CU_ID, CU_NAME, CU_PHONE, CU_EMAIL, CU_PASSWORD = range(5) #Field positions and headers for customers.csv
BK_ID, BK_CUSTOMER_ID, BK_SERVICE_ID, BK_DATE, BK_TIME, BK_STATUS = range(6) #Field positions and headers for booking.csv
PM_ID, PM_BOOKING_ID, PM_AMOUNT, PM_DATE, PM_STATUS = range(5) #Field positions and headers for payments.csv

#----------------------------------
#Generic File Helper
#----------------------------------
def ensure_file_exists(filename):
    """Create an empty file if it does not already exist."""

    if not os.path.exists(filename):
        try:
            open(filename, "w").close()
        except OSError as error:
            print(f"[ERROR] Could not create file '{filename}': {error}")

def read_records(filename):
    """Read a comma-delimited .csv file and return a list of records."""

    ensure_file_exists(filename)
    records = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                fields = line.split(FIELD_SEPARATOR)
                records.append(fields)
    except OSError as error:
        print(f"Error!Could not read file '{filename}': {error}")
    return records

def write_records(filename, records):
    """Overwrite the whole file with the given list of records."""
    try:
        with open(filename, "w") as file:
            for record in records:
                file.write(FIELD_SEPARATOR.join(str(field) for field in record) + "\n")
        return True
    except OSError as error:
        print(f"Error!Could not write to file '{filename}': {error}")
        return False

def append_record(filename, record):
    """Add one new record to the end of the file without touching the rest."""
    try:
        with open(filename, "a") as file:
            file.write(FIELD_SEPARATOR.join(str(field) for field in record) + "\n")
        return True
    except OSError as error:
        print(f"[ERROR] Could not write to file '{filename}': {error}")
        return False

def generate_next_id(records, id_index, prefix, width=4):
    """Give the next sequential ID such as PAY0001, PAY0002, PAY0003, ..."""

    max_number = 0
    for record in records:
        existing_id = record[id_index]
        numeric_part = existing_id.replace(prefix, "")
        if numeric_part.isdigit():
            max_number = max(max_number, int(numeric_part))
    next_number = max_number + 1
    return prefix + str(next_number).zfill(width)

def format_id(number):
    """Returns a string of the number padded with leading zeros to 4 digits."""

    return str(number).zfill(ID_LENGTH)
#-------------------------------------
#Input Validation
#-------------------------------------
def get_non_empty_input(prompt):
    """the user must type something rather than leaving a blank space."""

    while True:
            value = input(prompt).strip()
            if value != "":
                return value
            print("This field cannot be empty. Please try again.")

def get_valid_amount(prompt, minimum=0.01):
    """The user must enter a valid amount of money.The smallest amount allowed is default 0.01 which returns as a float, rounded to 2 decimal place."""

    while True:
        raw_value = input(prompt).strip()
        try:
            amount = float(raw_value)
            if amount < minimum:
                print(f"Amount must be at least {minimum:.2f}. Please try again.")
                continue
            return round(amount, 2)
        except ValueError:
            print("Invalid amount. Please enter a number, e.g. 45.00")


def get_valid_choice(prompt, valid_choices):
    """The user must pick one of a fixed set of given options."""

    while True:
        value = input(prompt).strip()
        if value in valid_choices:
            return value
        print(f"Invalid choice. Please choose one of: {', '.join(valid_choices)}")


def get_valid_month(prompt):
    """The user must enter a real month in YYYY-MM format."""

    while True:
        raw_value = input(prompt).strip()
        try:
            datetime.strptime(raw_value, "%Y-%m")
            return raw_value
        except ValueError:
            print("Invalid month. Please use the format YYYY-MM, e.g. 2026-09")
#-------------------------------------
#lookup functions
#-------------------------------------
def find_record_by_id(records, id_index, target_id):
    """Search a list of records for the one whose ID field matches."""

    for record in records:
        if record[id_index] == target_id:
            return record
    return None

def get_customer_name(customer_id, customers):
    """Look up a customer's name from their ID, for display in reports which returns as customer name or unknown customer if the customer ID doesn't exist."""

    customer = find_record_by_id(customers, CU_ID, customer_id)
    return customer[CU_NAME] if customer else "Unknown Customer"

def get_service_name(service_id, services):
    """Look up a service's name from its ID, for display in reports."""

    service = find_record_by_id(services, SV_ID, service_id)
    return service[SV_NAME] if service else "Unknown Service"

def get_service_price(service_id, services):
    """Look up a service's price from its ID."""

    service = find_record_by_id(services, SV_ID, service_id)
    return float(service[SV_PRICE]) if service else 0.0

def calculate_amount_due(booking, services):
    """Calculate the total amount a customer owes for one booking if a customer is either not shown or late."""

    base_amount = get_service_price(booking[BK_SERVICE_ID], services)
    status = booking[BK_STATUS]
    if status == "No-Show":
        return round(base_amount + NOT_SHOWING_FEE, 2)
    if status == "Late":
        return round(base_amount + LATE_FEE, 2)
    return round(base_amount, 2)

def get_total_paid_for_booking(booking_id, payments):
    """Add up every payment already made towards one booking."""

    total_paid = 0.0
    for payment in payments:
        if payment[PM_BOOKING_ID] == booking_id:
            total_paid += float(payment[PM_AMOUNT])
    return round(total_paid, 2)

def get_customer_name_for_booking(booking_id, bookings, customers):
    """Look up the name of the customer who made a given booking."""

    booking = find_record_by_id(bookings, BK_ID, booking_id)
    if booking is None:
        return "Unknown Customer"
    return get_customer_name(booking[BK_CUSTOMER_ID], customers)

#--------------------------------------------
#Option:1 Record Payment
#--------------------------------------------
def record_payment():
    """Option 1: record a new payment made against a booking.
    Check the whole transaction: look up the booking by its ID, show how much is due / already paid / still
    owed, validate the entered amount, work out whether the booking becomes fully "Paid" or stays "Partial", and append the new payment
    to payments.csv. Refuses to proceed if the booking doesn't exist, was cancelled, or is already paid in full. """

    print("\n--- RECORD A NEW PAYMENT ---")
    bookings = read_records(BOOKINGS_FILE)
    payments = read_records(PAYMENTS_FILE)
    customers = read_records(CUSTOMERS_FILE)
    services = read_records(SERVICES_FILE)

    if not bookings:
        print("No booking is found. Kindly ask Booking Officer to create a booking first.")
        return

    booking_id = get_non_empty_input("Enter Booking ID (e.g. B0001): ").upper()
    booking = find_record_by_id(bookings, BK_ID, booking_id)

    if booking is None:
        print(f"Booking '{booking_id}' was not found. Please check the Booking ID and try again.")
        return

    if booking[BK_STATUS] == "Cancelled":
        print("This booking was cancelled. No payment can be recorded against it.")
        return

    amount_due = calculate_amount_due(bookings, services)
    already_paid = get_total_paid_for_booking(booking_id, payments)
    balance = round(amount_due - already_paid, 2)

    customer_name = get_customer_name(booking[BK_CUSTOMER_ID], customers)
    service_name = get_service_name(booking[BK_SERVICE_ID], services)
    print(f"Customer      : {customer_name} ({booking[BK_CUSTOMER_ID]})")
    print(f"Service       : {service_name}")
    print(f"Booking Status: {booking[BK_STATUS]}")
    print(f"Amount Due    : RM {amount_due:.2f}")
    print(f"Already Paid  : RM {already_paid:.2f}")
    print(f"Balance       : RM {balance:.2f}")

    if balance <= 0:
        print("This booking has already been paid in full.")
        return

    amount = get_valid_amount(f"Enter payment amount (up to RM {balance:.2f}): ")
    while amount > balance:
        print(f"Amount exceeds the remaining balance of RM {balance:.2f}.")
        amount = get_valid_amount(f"Enter payment amount (up to RM {balance:.2f}): ")

    date_str = datetime.now().strftime("%Y-%m-%d")
    new_total_paid = round(already_paid + amount, 2)
    status = "Paid" if new_total_paid >= amount_due else "Partial"

    payment_id = generate_next_id(payments, PM_ID, "PAY")
    new_payment = [payment_id, booking_id, f"{amount}", date_str, status]

    if append_record(PAYMENTS_FILE, new_payment):
        print(f"\n[OK] Payment '{payment_id}' recorded successfully. Status: {status}")
    else:
        print("Failed to save payment. Please try again.")
#--------------------------------------------------
#Option 2: Update Payment
#--------------------------------------------------
def update_payment():
    """Option 2: Update an existing payment record."""

    print("\n--- UPDATE AN EXISTING PAYMENT ---")
    payments = read_records(PAYMENTS_FILE)

    if not payments:
        print("Sorry!No payments found to update.")
        return

    payment_id = get_non_empty_input("Enter Payment ID to update (e.g. PAY0001): ").upper()
    payment = find_record_by_id(payments, PM_ID, payment_id)

    if payment is None:
        print(f"Payment '{payment_id}' was not found.")
        return

    print(f"Current record -> Amount: RM {float(payment[PM_AMOUNT]):.2f}, "
          f"Date: {payment[PM_DATE]}, Status: {payment[PM_STATUS]}")

    print("\nWhat would you like to update?")
    print("1. Amount")
    print("2. Payment Status")
    print("0. Cancel")
    choice = get_valid_choice("Enter choice: ", ["0", "1", "2"])

    if choice == "0":
        print("Update cancelled.")
        return
    elif choice == "1":
        new_amount = get_valid_amount("Enter new amount: RM ")
        payment[PM_AMOUNT] = f"{new_amount:.2f}"
    elif choice == "2":
        new_status = get_valid_choice("New status (Paid/Partial/Unpaid): ", ["Paid", "Partial", "Unpaid"])
        payment[PM_STATUS] = new_status

    if write_records(PAYMENTS_FILE, payments):
        print(f"Payment '{payment_id}' updated successfully.")
    else:
        print("Sorry!Failed to update payment.")
#-----------------------------------
#Option 3 View all payments
#-----------------------------------
def view_all_payments():
    """Option 3: print and view every payment on file as a formatted table."""

    print("\n--- ALL PAYMENT RECORDS ---")
    payments = read_records(PAYMENTS_FILE)
    bookings = read_records(BOOKINGS_FILE)
    customers = read_records(CUSTOMERS_FILE)
    services = read_records(SERVICES_FILE)

    if not payments:
        print("No payment records found.")
        return

    header = (f"{'Payment ID':<12}{'Booking ID':<12}{'Customer':<18}"
              f"{'Service':<22}{'Amount':>10}  {'Date':<12}{'Status':<10}")
    print(header)
    print("-" * len(header))
    for payment in payments:
        booking = find_record_by_id(bookings, BK_ID, payment[PM_BOOKING_ID])
        customer_name = get_customer_name(booking[BK_CUSTOMER_ID], customers) if booking else "Unknown Customer"
        service_name = get_service_name(booking[BK_SERVICE_ID], services) if booking else "Unknown Service"
        amount = float(payment[PM_AMOUNT])
        print(f"{payment[PM_ID]:<12}{payment[PM_BOOKING_ID]:<12}{customer_name:<18}"
              f"{service_name:<22}{amount:>10.2f}  {payment[PM_DATE]:<12}{payment[PM_STATUS]:<10}")
    print("-" * len(header))
    print(f"Total records: {len(payments)}")

#----------------------------------------
#Option 4: Generate an income summary
#----------------------------------------
def generate_income_summary():
    """Menu option 4: genearate a report how much money has come in, and from where."""

    print("\n--- INCOME SUMMARY ---")
    payments = read_records(PAYMENTS_FILE)
    bookings = read_records(BOOKINGS_FILE)
    services = read_records(SERVICES_FILE)

    if not payments:
        print("No payment records found.")
        return

    total_income = 0.0
    income_by_service = {}

    for payment in payments:
        amount = float(payment[PM_AMOUNT])
        total_income += amount

        booking = find_record_by_id(bookings, BK_ID, payment[PM_BOOKING_ID])
        service_name = get_service_name(booking[BK_SERVICE_ID], services) if booking else "Unknown Service"
        income_by_service[service_name] = income_by_service.get(service_name, 0.0) + amount
        lines = [
            "=" * 45,
            "        SHINEONWHEELS - INCOME SUMMARY",
            "=" * 45,
            f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total transactions: {len(payments)}",
            f"TOTAL INCOME: RM {total_income:.2f}",
            "",
            "Income by Service:",
        ]
        for service_name, amount in income_by_service.items():
            lines.append(f"  {service_name:<25}: RM {amount:.2f}")
        lines.append("=" * 45)

        report_text = "\n".join(lines)
        print("\n" + report_text)
#----------------------------------------------
#Option 4: generate a outstanding payment list
#----------------------------------------------

def generate_outstanding_payment_list():
    """Option 5: generate a list of every booking that still has money owing."""

    print("\n--- OUTSTANDING PAYMENT LIST ---")
    bookings = read_records(BOOKINGS_FILE)
    payments = read_records(PAYMENTS_FILE)
    customers = read_records(CUSTOMERS_FILE)
    services = read_records(SERVICES_FILE)

    if not bookings:
        print("No bookings found.")
        return

    outstanding_list = []
    total_outstanding = 0.0

    for booking in bookings:
        if booking[BK_STATUS] == "Cancelled":
            continue

        amount_due = calculate_amount_due(booking, services)
        paid = get_total_paid_for_booking(booking[BK_ID], payments)
        balance = round(amount_due - paid, 2)
        if balance > 0:
            customer_name = get_customer_name(booking[BK_CUSTOMER_ID], customers)
            outstanding_list.append((booking[BK_ID], customer_name, booking[BK_DATE], amount_due, paid, balance))
            total_outstanding += balance

    if not outstanding_list:
        print("[OK] No outstanding payments. All bookings are fully paid.")
        return

    lines = [
        "=" * 65,
        "        SHINEONWHEELS - OUTSTANDING PAYMENT LIST",
        "=" * 65,
        f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"{'Booking ID':<12}{'Customer':<20}{'Date':<12}{'Due':>8}{'Paid':>8}{'Balance':>10}",
        "-" * 65,
    ]
    for booking_id, customer_name, date, due, paid, balance in outstanding_list:
        lines.append(f"{booking_id:<12}{customer_name:<20}{date:<12}{due:>8.2f}{paid:>8.2f}{balance:>10.2f}")
    lines.append("-" * 65)
    lines.append(f"TOTAL OUTSTANDING: RM {total_outstanding:.2f}  ({len(outstanding_list)} booking(s))")
    lines.append("=" * 65)

    report_text = "\n".join(lines)
    print("\n" + report_text)
#----------------------------------
#Option 6: Monthly Financial Summary
#----------------------------------

def generate_monthly_financial_summary():
    """Option 6: summarise one month's income versus outstanding."""

    print("\n--- MONTHLY FINANCIAL SUMMARY ---")
    target_month = get_valid_month("Enter month to summarise (YYYY-MM): ")

    payments = read_records(PAYMENTS_FILE)
    bookings = read_records(BOOKINGS_FILE)
    services = read_records(SERVICES_FILE)

    month_income = 0.0
    month_transactions = 0
    for payment in payments:
        if payment[PM_DATE].startswith(target_month):
            month_income += float(payment[PM_AMOUNT])
            month_transactions += 1
    month_outstanding = 0.0
    month_bookings_count = 0
    for booking in bookings:
        if booking[BK_DATE].startswith(target_month) and booking[BK_STATUS] != "Cancelled":
            month_bookings_count += 1
            amount_due = calculate_amount_due(booking, services)
            paid = get_total_paid_for_booking(booking[BK_ID], payments)
            balance = round(amount_due - paid, 2)
            if balance > 0:
                month_outstanding += balance

    lines = [
        "=" * 45,
        f"   MONTHLY FINANCIAL SUMMARY - {target_month}",
        "=" * 45,
        f"Report generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Bookings in month: {month_bookings_count}",
        f"Payments received: {month_transactions}",
        f"Income collected : RM {month_income:.2f}",
        f"Outstanding      : RM {month_outstanding:.2f}",
        f"Net position     : RM {month_income - month_outstanding:.2f}",
        "=" * 45,
    ]

    report_text = "\n".join(lines)
    print("\n" + report_text)

#---------------------------
#   Accountant Menu
#---------------------------

def accountant_menu():
    """Show the Accountant role's menu in a loop until the user exits."""

    while True:
        print("\n" + "=" * 45)
        print("           ACCOUNTANT MENU")
        print("=" * 45)
        print("1. Record a New Payment")
        print("2. Update an Existing Payment")
        print("3. View All Payments")
        print("4. Generate Income Summary")
        print("5. Generate Outstanding Payment List")
        print("6. Generate Monthly Financial Summary")
        print("0. Back to Main Menu")

        choice = get_valid_choice("Enter your choice: ", ["0", "1", "2", "3", "4", "5", "6"])

        if choice == "1":
            record_payment()
        elif choice == "2":
            update_payment()
        elif choice == "3":
            view_all_payments()
        elif choice == "4":
            generate_income_summary()
        elif choice == "5":
            generate_outstanding_payment_list()
        elif choice == "6":
            generate_monthly_financial_summary()
        elif choice == "0":
            print("Returning to main menu...")
            break


if __name__ == "__main__":
    accountant_menu()
