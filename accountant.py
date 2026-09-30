"""Accountant Role"""

import os
from datetime import datetime

from constants import SERVICES_file, CUSTOMERS_file, BOOKING_file, PAYMENTS_file

field_separator = ","
tax_rate = 0.06
id_length = 4

payment_methods = ["CASH","Card","Online Transfer", "E-Wallet"]
late_fee = 10.00
not_showing_fee= 20.00

field_name1 = ["sv_id","sv_name","sv_price","sv_duration"]
field_name2 = ["cu_id","cu_name","cu_phone","cu_email","cu_password"]
field_name3 = ["bk_id","bk_customer_id","bk_service_id","bk_date","bk_time","bk_status"]
field_name4 = ["pm_id","pm_booking_id","pm_amount","pm_date","pm_status"]

def check_file (filename):
    """Create an empty file if it does not already exist."""

    if not os.path.exists(filename):
        try:
            open(filename, "w").close()
        except OSError as error:
            print(f"Sorry!Could not create file '{filename}': {error}")

def read_records (filename):
    """Read a comma-delimited .csv file and return a list of records."""

    check_file(filename)
    records = []
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if line == "":
                    continue
                fields = line.split(field_separator)
                records.append(fields)
    except OSError as error:
        print(f"Sorry! Could not read file '{filename}': {error}")
    return records

def write_records (filename, records):
    """Overwrite the whole file with the given list of records."""
    try:
        with open(filename, "w") as file:
            for record in records:
                file.write(field_separator.join(str(field) for field in record) + "\n")
        return True
    except OSError as error:
        print(f"Sorry! Could not write to file '{filename}': {error}")
        return False

def append_records (filename, record):
    """Add one new record to the end of the file without touching the rest."""
    try:
        with open(filename, "a") as file:
            file.write(field_separator.join(str(field) for field in record) + "\n")
        return True
    except OSError as error:
        print(f"Sorry! Could not write to file '{filename}': {error}")
        return False

def id_generator (records, id_index, prefix, width=4):
    """Give the next sequential ID such as PAY0001, PAY0002, PAY0003, ..."""

    max_number = 0
    for record in records:
        existing_id = record[id_index]
        numeric_part = existing_id.replace(prefix, "")
        if numeric_part.isdigit():
            max_number = max(max_number, int(numeric_part))
    next_number = max_number + 1
    return prefix + str(next_number).zfill(width)

def formatting_id(number):
    """Returns a string of the number padded with leading zeros to 4 digits."""

    return str(number).zfill(id_length)

#Input Validation

def no_empty_input(prompt):
    """the user must type something rather than leaving a blank space."""

    while True:
            value = input(prompt).strip()
            if value != "":
                return value
            print("This field cannot be empty. Please try again.")

def amount_validation(prompt, minimum=0.01):
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


def choice_validation(prompt, valid_choices):
    """The user must pick one of a fixed set of given options."""

    while True:
        value = input(prompt).strip()
        if value in valid_choices:
            return value
        print(f"Invalid choice. Please choose one of: {', '.join(valid_choices)}")


def month_validation(prompt):
    """The user must enter a real month in YYYY-MM format."""

    while True:
        raw_value = input(prompt).strip()
        try:
            datetime.strptime(raw_value, "%Y-%m")
            return raw_value
        except ValueError:
            print("Invalid month. Please use the format YYYY-MM, e.g. 2026-09")

#lookup functions

def find (records, id_index, target_id):
    """Search a list of records for the one whose ID field matches."""

    for record in records:
        if record[id_index] == target_id:
            return record
    return None

def customer_name (customer_id, customers):
    """Look up a customer's name from their ID, for display in reports which returns as customer name or unknown customer if the customer ID doesn't exist."""

    customer = find(customers, field_name1[0], customer_id)
    return customer[field_name2[2]] if customer else "Unknown Customer"

def service_name(service_id, services):
    """Look up a service's name from its ID, for display in reports."""

    service = find(services, field_name1[0], service_id)
    return service[field_name1[1]] if service else "Unknown Service"

def service_price(service_id, services):
    """Look up a service's price from its ID."""

    service = find(services, field_name1[0], service_id)
    return float(service[field_name1[3]]) if service else 0.0

def due_amount(booking, services):
    """Calculate the total amount a customer owes for one booking if a customer is either not shown or late."""

    base_amount = get_service_price(booking[field_name3[2]], services)
    status = booking[field_name3[5]]
    if status == "Not Showing":
        return round(base_amount + not_showing_fee, 2)
    if status == "Late":
        return round(base_amount + late_fee, 2)
    return round(base_amount, 2)

def total_paid_for_booking (booking_id, payments):
    """Add up every payment already made towards one booking."""

    total_paid = 0.0
    for payment in payments:
        if payment[field_name4[0]] == booking_id:
            total_paid += float(payment[field_name4[2]])
    return round(total_paid, 2)

def customer_name_for_booking(booking_id, bookings, customers):
    """Look up the name of the customer who made a given booking."""

    booking = find (bookings, field_name3[0], booking_id)
    if booking is None:
        return "Unknown Customer"
    return customer_name(booking[field_name3[2]], customers)


#Record Payment

def record_payment():
    """record a new payment from the booking"""

    print("\n--- RECORD A NEW PAYMENT ---")
    bookings = read_records(BOOKING_file)
    payments = read_records(PAYMENTS_file)
    customers = read_records(CUSTOMERS_file)
    services = read_records(SERVICES_file)

    if not bookings:
        print("No booking is found. Kindly ask Booking Officer to create a booking first.")
        return

    booking_id = no_empty_input("Enter Booking ID (e.g. B0001): ").upper()
    booking = find (bookings, field_name3[0], booking_id)

    if booking is None:
        print(f"Booking '{booking_id}' was not found. Please check the Booking ID and try again.")
        return

    if booking[field_name3[5]] == "Cancelled":
        print("This booking was cancelled. No payment can be recorded against it.")
        return

    amount_due = due_amount(bookings, services)
    paid = total_paid_for_booking(booking_id, payments)
    balance = round(amount_due - paid, 2)

    customer_name1 = customer_name(booking[field_name3[1]], customers)
    service_name2 = service_name(booking[field_name3[2]], services)
    print(f"Customer      : {customer_name1} ({booking[field_name3[1]]})")
    print(f"Service       : {service_name2}")
    print(f"Booking Status: {booking[BK_STATUS]}")
    print(f"Amount Due    : RM {amount_due:.2f}")
    print(f"Already Paid  : RM {paid:.2f}")
    print(f"Balance       : RM {balance:.2f}")

    if balance <= 0:
        print("This booking has already been paid in full.")
        return

    amount = amount_validation(f"Enter payment amount (up to RM {balance:.2f}): ")
    while amount > balance:
        print(f"Amount exceeds the remaining balance of RM {balance:.2f}.")
        amount = amount_validation(f"Enter payment amount (up to RM {balance:.2f}): ")

    date_str = datetime.now().strftime("%Y-%m-%d")
    total_paid1 = round(paid + amount, 2)
    status = "Paid" if total_paid1 >= amount_due else "Partial"

    payment_id = id_generator(payments, field_name4[2], "PAY")
    new_payment = [payment_id, booking_id, f"{amount}", date_str, status]

    if append_record(PAYMENTS_file, new_payment):
        print(f"\n[OK] Payment '{payment_id}' recorded successfully. Status: {status}")
    else:
        print("Failed to save payment. Please try again.")

#Update Payment

def update_payment():
    """Option 2: Update an existing payment record."""

    print("\n--- UPDATE AN EXISTING PAYMENT ---")
    payments = read_records(PAYMENTS_file)

    if not payments:
        print("Sorry!No payments found to update.")
        return

    payment_id = no_empty_input("Enter Payment ID to update (e.g. PAY0001): ").upper()
    payment = find(payments, field_name4[0], payment_id)

    if payment is None:
        print(f"Payment '{payment_id}' was not found.")
        return

    print(f"Current record -> Amount: RM {float(payment[field_name4]):.2f}, "
          f"Date: {payment[field_name4[3]]}, Status: {payment[field_name4[4]]}")

    print("\nPlease select the choice that u would like to update")
    print("1. Amount")
    print("2. Payment Status")
    print("0. Cancel")
    choice = choice_validation("Enter choice: ", ["0", "1", "2"])

    if choice == "0":
        print("Update cancelled.")
        return
    elif choice == "1":
        new_amount = amount_validation("Enter new amount: RM ")
        payment[field_name4[2]] = f"{new_amount:.2f}"
    elif choice == "2":
        new_status = choice_validation("New status (Paid/Partial/Unpaid): ", ["Paid", "Partial", "Unpaid"])
        payment[field_name4[4]] = new_status

    if write_records(PAYMENTS_file, payments):
        print(f"Payment '{payment_id}' updated successfully.")
    else:
        print("Sorry!Failed to update payment.")

#Option 3 View all payments

def view_payments():
    """print and view every payment on file as a formatted table."""

    print("\n--- ALL PAYMENT RECORDS ---")
    payments = read_records(PAYMENTS_file)
    bookings = read_records(BOOKING_file)
    customers = read_records(CUSTOMERS_file)
    services = read_records(SERVICES_file)

    if not payments:
        print("No payment records found.")
        return

    header = (f"{'Payment ID':<12}{'Booking ID':<12}{'Customer':<18}"
              f"{'Service':<22}{'Amount':>10}  {'Date':<12}{'Status':<10}")
    print(header)
    print("-" * len(header))
    for payment in payments:
        booking = find(bookings, field_name3[0], payment[field_name4[1]])
        customer_name3 = customer_name(booking[field_name3[1]], customers) if booking else "Unknown Customer"
        service_name4 = service_name(booking[field_name1[0]], services) if booking else "Unknown Service"
        amount = float(payment[field_name4[2]])
        print(f"{payment[field_name4[0]]:<12}{payment[field_name4[1]]:<12}{customer_name3:<18}"
              f"{service_name4:<22}{amount:>10.2f}  {payment[field_name4[3]]:<12}{payment[field_name4[4]]:<10}")
    print("-" * len(header))
    print(f"Total records: {len(payments)}")

#Option 4: Generate an income summary

def income_summary():
    """Menu option 4: genearate a report how much money has come in, and from where."""

    print("\n--- INCOME SUMMARY ---")
    payments = read_records(PAYMENTS_file)
    bookings = read_records(BOOKING_file)
    services = read_records(SERVICES_file)

    if not payments:
        print("No payment records found.")
        return

    total_income = 0.0
    income_by_service = {}

    for payment in payments:
        amount = float(payment[field_name4[2]])
        total_income += amount

        booking = find(bookings, field_name3[0], payment[field_name4[1]])
        service_name5 = service_name(booking[field_name3[2]], services) if booking else "Unknown Service"
        income_by_service[service_name5] = income_by_service.get(service_name, 0.0) + amount
        lines = [
            "=" * 15 + "        SHINEONWHEELS - INCOME SUMMARY" + "=" * 45,
            f"Report: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Total transactions: {len(payments)}",
            f"TOTAL INCOME: RM {total_income:.2f}",
            "",
            "Income by Service:",
        ]
        for service_name5, amount in income_by_service.items():
            lines.append(f"  {service_name5:<25}: RM {amount:.2f}")
        lines.append("=" * 45)

        report_text = "\n".join(lines)
        print("\n" + report_text)

#Option 4: generate a outstanding payment list


def outstanding_payment_list():
    """generate a list of every booking that still has money owing."""

    print("\n--- OUTSTANDING PAYMENT LIST ---")
    bookings = read_records(BOOKING_file)
    payments = read_records(PAYMENTS_file)
    customers = read_records(CUSTOMERS_file)
    services = read_records(SERVICES_file)

    if not bookings:
        print("No bookings found.")
        return

    outstanding_list = []
    total_outstanding = 0.0

    for booking in bookings:
        if booking[field_name3[5]] == "Cancelled":
            continue

        amount_due = due_amount(booking, services)
        paid = total_paid_for_booking(booking[field_name3[0]], payments)
        balance = round(amount_due - paid, 2)
        if balance > 0:
            customer_name6 = customer_name(booking[field_name3[1]], customers)
            outstanding_list.append((booking[field_name3[0]], customer_name6, booking[field_name3[4]], amount_due, paid, balance))
            total_outstanding += balance

    if not outstanding_list:
        print("HooYay! No outstanding payments. All bookings are fully paid.")
        return

    lines = [
        "=" * 15 + "        SHINEONWHEELS - OUTSTANDING PAYMENT LIST" + "=" * 65,
        f"Report: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
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

#Option 6: Monthly Financial Summary


def monthly_financial_summary():
    """summarise one month's income versus outstanding."""

    print("\n--- MONTHLY FINANCIAL SUMMARY ---")
    target_month = month_validation("Enter month to summarise (YYYY-MM): ")

    payments = read_records(PAYMENTS_file)
    bookings = read_records(BOOKING_file)
    services = read_records(SERVICES_file)

    month_income = 0.0
    month_transactions = 0
    for payment in payments:
        if payment[field_name4[3]].startswith(target_month):
            month_income += float(payment[field_name4[2]])
            month_transactions += 1
    month_outstanding = 0.0
    month_bookings_count = 0
    for booking in bookings:
        if booking[field_name3[3]].startswith(target_month) and booking[field_name3[5]] != "Cancelled":
            month_bookings_count += 1
            amount_due8 = due_amount(booking, services)
            paid = total_paid_for_booking(booking[field_name3[0]], payments)
            balance = round(amount_due8 - paid, 2)
            if balance > 0:
                month_outstanding += balance

    lines = [
        "=" * 15 + f"   MONTHLY FINANCIAL SUMMARY for {target_month}" + "=" * 15,
        f"Report generated : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"Bookings in month: {month_bookings_count}",
        f"Payments received: {month_transactions}",
        f"Income collected : RM {month_income:.2f}",
        f"Outstanding      : RM {month_outstanding:.2f}",
        f"Net position     : RM {month_income - month_outstanding:.2f}",
        "=" * 15,
    ]

    report_text = "\n".join(lines)
    print("\n" + report_text)


#   Accountant Menu


def accountant_menu():
    """Show the Accountant role's menu in a loop until the user exits."""

    while True:
        print("=" * 15 + "ACCOUNTANT MENU" +"=" * 15)
        print("1. Record a New Payment")
        print("2. Update an Existing Payment")
        print("3. View All Payments")
        print("4. Generate Income Summary")
        print("5. Generate Outstanding Payment List")
        print("6. Generate Monthly Financial Summary")
        print("0. Back to Main Menu")

        choice = choice_validation("Enter your choice: ", ["0", "1", "2", "3", "4", "5", "6"])

        if choice == "1":
            record_payment()
        elif choice == "2":
            update_payment()
        elif choice == "3":
            view_payments()
        elif choice == "4":
            income_summary()
        elif choice == "5":
            outstanding_payment_list()
        elif choice == "6":
            monthly_financial_summary()
        elif choice == "0":
            print("Returning to main menu...")
            break


if __name__ == "__main__":
    accountant_menu()
