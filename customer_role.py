from constants import CUSTOMERS_file, REQUESTED_BOOKING_file, SERVICES_file, BOOKING_file, PAYMENTS_file, REQUESTED_EXTENSION_file
from input_validation import get_menu_choice_from_user, get_non_empty_text_from_user, get_valid_date_from_user, get_valid_time_from_user, read_file, append_line, service_exists, customer_id_exists

# FEATURE 1: VIEW AVAILABLE SERVICES SLOTS/ PACKAGES


def view_services():
    """Displays all the available services from services.csv as a simple table."""
    print("\n--- Available Services ---")
    services = read_file(SERVICES_file)
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

# FEATURE 2: REQUEST A BOOKING OR AN EXTENSION
# To check if a service ID exists in the services.csv file (used when requesting a booking)


def request_booking():
    """Collects details for a brand-new booking and send it to the officer for approval."""
    print("\n--- New Booking ---")
    view_services()

    while True:
        # 1.) Get the customer ID from the user
        customer_id = get_non_empty_text_from_user("Enter your customer ID: ")
        # Check if the customer ID exists in the customers.csv file
        if not customer_id_exists(customer_id):
            print("Customer ID not found. Please check your ID and try again.")
            return
        service_id = get_non_empty_text_from_user(
            "Enter the service ID you want to book: ")
        if service_exists(service_id):
            break
        print("That service ID doesn't exist. Please check the available services above.")
    date = get_valid_date_from_user("Enter your booking date (YYYY-MM-DD): ")
    time = get_valid_time_from_user("Enter your booking time (HH:MM): ",
                                    "Please enter a valid time in 24-hour format (HH:MM) and ensure it is within the operating hours of 10:00 to 20:00.")
    new_line = ','.join([customer_id, service_id, date, time])
    if append_line(REQUESTED_BOOKING_file, new_line):
        print("Your booking request has been submitted for approval.")
    else:
        print("Something went wrong submitting your booking request. Please try again.")


def request_extension():
    """Shows all the customer booking in the form of table and let the customer pick one of their existing booking and change its date/time for extension."""
    print("\n--- Request an extension for a specific booking ---")
    # 1.) Get the customer ID from the user
    customer_id = get_non_empty_text_from_user("Enter your customer ID: ")
    # Check if the customer ID exists in the customers.csv file
    if not customer_id_exists(customer_id):
        print("Customer ID not found. Please check your ID and try again.")
        return
    # 2.) Show all of this customer's bookings
    all_bookings = []
    for line in read_file(BOOKING_file):
        data = line.split(",")
        if (len(data) >= 6) and (data[1] == customer_id):
            all_bookings.append(data)
    if len(all_bookings) == 0:
        print("You have no existing bookings to extend.")
        return
    # Display the bookings in a table format for the customer
    print("Your current bookings:")
    print(f"{'Booking ID':<12}{'Service ID':<12}{'Date':<12}{'Time':<8}")
    for fields in all_bookings:
        booking_id, service_id, date, time = fields[0], fields[2], fields[3], fields[4], fields[5]
        print(f"{booking_id:<12}{service_id:<12}{date:<12}{time:<8}")
    # 3.)Let the customer pick which booking by typing its Booking ID
    booking_id_to_extend = get_non_empty_text_from_user(
        "Enter the Booking ID of the booking you want to extend: ")
    # Check if the entered Booking ID exists in the customer's bookings
    selected_booking = None
    for fields in all_bookings:
        if fields[0] == booking_id_to_extend:
            selected_booking = fields
            break
    if selected_booking is None:
        print("Invalid Booking ID. Please check and try again.")
        return
    # 4.) Ask for the new time for the extension
    new_time = get_valid_time_from_user("Enter the new time for the extension (HH:MM): ",
                                        "Please enter a valid time in 24-hour format (HH:MM) and ensure it is within the operating hours of 10:00 to 20:00.")
    # 5.) Save the extension request to requested_extension.csv
    new_line = ','.join([customer_id, booking_id_to_extend, new_time])
    if append_line(REQUESTED_EXTENSION_file, new_line):
        print("Your extension request has been submitted for approval.")
    else:
        print("Something went wrong submitting your extension request. Please try again.")


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

# FEATURE 3: VIEW BOOKING HISTORY AND INVOICES


def find_payment_for_booking(booking_id, date, ):
    """Returns the payment row (as a field list) matching this exact booking's customer_ id + services_id+date+time, or None if no payment has been recorded."""
    for line in read_file(PAYMENTS_file):
        fields = line.split(",")
        if (len(fields) < 7):
            continue
        pos_booking_id = fields[1].strip()
        pos_date = fields[5].strip()
        if (pos_booking_id == booking_id) and (pos_date == date):
            return fields
        return None


def view_history_and_invoices():
    """Shows all of this customer's bookings with payment info if available."""
    print("\n--- SERVICES History & Invoices ---")
    # Get the customer ID from the user
    customer_id = get_non_empty_text_from_user("Enter your customer ID: ")
    # Check if the customer ID exists in the customers.csv file
    if not customer_id_exists(customer_id):
        print("Customer ID not found. Please check your ID and try again.")
        return
    all_bookings = []
    for line in read_file(BOOKING_file):
        fields = line.split(",")
        if (len(fields) >= 1) and (fields[1] == customer_id):
            all_bookings.append(fields)
    if len(all_bookings) == 0:
        print("You have no bookings yet.")
        return
    # Display the bookings for the customer
    print(f"{'Booking ID':<12}{'Service ID':<12}{'Date':<12}{'Time':<8}{'Status':<10}")
    for fields in all_bookings:
        booking_id, service_id, date, time, status = fields[
            0], fields[2], fields[3], fields[4], fields[5]
        print(f"{booking_id:<12}{service_id:<12}{date:<12}{time:<8}{status:<10}")
        # Invoice (tax is already included for amount_that_to_be_paid)
        payment = find_payment_for_booking(booking_id, date)
        if payment is not None:
            amount_that_to_be_paid = float(payment[2])
            print(
                f"Invoice: RM{amount_that_to_be_paid:.2f} (status: {payment[6]})")
        else:
            print("Invoice: No payment recorded yet.")

# LOGGED-IN CUSTOMER MENU


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


# ENTRY POINT
if __name__ == "__main__":
    customer_menu()
