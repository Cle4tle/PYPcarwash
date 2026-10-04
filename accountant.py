# ShineOnWheels Booking System - Accountant
# 1. Record and update payments
# 2. Income summary and outstanding payment list
# 3. Monthly financial summary

from constants import PAYMENTS_file, BOOKING_file, SERVICES_file
TAX_RATE = 0.06

# payments.csv : payment_id,booking_id,amount_due,amount_paid,method,date,status
# bookings.csv : booking_id,customer_id,service_id,date,time,status
# services.csv : service_id,service_name,price


# read a file into a list
def read_file(file_name):
    data = []
    try:
        file = open(file_name, "r")
        for line in file:
            line = line.strip()
            if line != "":
                data.append(line.split(","))
        file.close()
    except:
        print("Cannot open", file_name)
    return data

# save the payments list into payments.txt
def save_payments(payments):
    file = open(PAYMENTS_file, "w")
    for p in payments:
        file.write(p[0] + "," + p[1] + "," + p[2] + "," + p[3] + "," +
                   p[4] + "," + p[5] + "," + p[6] + "\n")
    file.close()


# ask for money until the user types a correct number
def ask_amount():
    while True:
        try:
            amount = float(input("Enter amount paid: RM "))
            if amount >= 0:
                return amount
            else:
                print("Amount cannot be negative.")
        except:
            print("Please enter a number only.")

# 1. record payment
def record_payment():
    bookings = read_file(BOOKING_file)
    services = read_file(SERVICES_file)
    payments = read_file(PAYMENTS_file)

    booking_id = input("Enter booking ID: ")

    # check the booking
    found = False
    for b in bookings:
        if b[0] == booking_id:
            found = True
            service_id = b[2]
            booking_status = b[5]

    if found == False:
        print("Booking not found.")
        return
    if booking_status == "Cancelled":
        print("This booking is cancelled.")
        return

    # check if already paid
    for p in payments:
        if p[1] == booking_id:
            print("This booking already has a payment.")
            return

        # find the price of the service
        price = 0
        for s in services:
            if s[0] == service_id:
                price = float(s[2])

        tax = price * TAX_RATE
        due = round(price + tax, 2)
        print("Price: RM", price)
        print("Tax  : RM", round(tax, 2))
        print("Total: RM", due)

        paid = ask_amount()
        if paid > due:
            paid = due

        method = input("Payment method (Cash/Card/E-Wallet): ")
        date = input("Payment date (YYYY-MM-DD): ")

        if paid == due:
            status = "Paid"
        elif paid > 0:
            status = "Partial"
        else:
            status = "Unpaid"

        payment_id = "P" + str(len(payments) + 1)
        payments.append([payment_id, booking_id, str(due), str(paid), method, date, status])
        save_payments(payments)
        print("Payment", payment_id, "saved. Status:", status)

# 2. update payment
def update_payment():
    payments = read_file(PAYMENTS_file)
    payment_id = input("Enter payment ID: ")

    for p in payments:
        if p[0] == payment_id:
            due = float(p[2])
            paid = float(p[3])
            print("Total due  : RM", due)
            print("Already paid: RM", paid)
            print("Balance     : RM", round(due - paid, 2))

            extra = ask_amount()
            paid = paid + extra
            if paid > due:
                paid = due

            if paid == due:
                status = "Paid"
            elif paid > 0:
                status = "Partial"
            else:
                status = "Unpaid"

            p[3] = str(round(paid, 2))
            p[4] = input("Payment method (Cash/Card/E-Wallet): ")
            p[5] = input("Payment date (YYYY-MM-DD): ")
            p[6] = status
            save_payments(payments)
            print("Payment updated. Status:", status)
            return

    print("Payment not found.")

# 3. view all payments
def view_payments():
    payments = read_file(PAYMENTS_file)
    print("\nID, Booking, Due, Paid, Method, Date, Status")
    for p in payments:
        print(p[0], p[1], p[2], p[3], p[4], p[5], p[6])


# 4. income summary
def income_summary():
    payments = read_file(PAYMENTS_file)
    total_due = 0
    total_paid = 0

    for p in payments:
        total_due = total_due + float(p[2])
        total_paid = total_paid + float(p[3])

    print("\n--- Income Summary ---")
    print("Number of payments:", len(payments))
    print("Total billed  : RM", round(total_due, 2))
    print("Total received: RM", round(total_paid, 2))
    print("Still owed    : RM", round(total_due - total_paid, 2))

# 5. outstanding payments
def outstanding_list():
    payments = read_file(PAYMENTS_file)
    print("\n--- Outstanding Payments ---")
    count = 0

    for p in payments:
        if p[6] != "Paid":
            balance = float(p[2]) - float(p[3])
            print(p[0], "Booking", p[1], "owes RM", round(balance, 2))
            count = count + 1

    if count == 0:
        print("No outstanding payments.")


# 6. monthly summary
def monthly_summary():
    payments = read_file(PAYMENTS_file)
    month = input("Enter month (YYYY-MM): ")
    total = 0
    count = 0

    print("\n--- Payments in", month, "---")
    for p in payments:
        if month in p[5]:
            print(p[0], p[1], p[5], "RM", p[3])
            total = total + float(p[3])
            count = count + 1

    print("Number of payments:", count)
    print("Total received    : RM", round(total, 2))

# accountant menu
def accountant_menu():
    while True:
        print("\n===== ACCOUNTANT MENU =====")
        print("1. Record payment")
        print("2. Update payment")
        print("3. View all payments")
        print("4. Income summary")
        print("5. Outstanding payments")
        print("6. Monthly summary")
        print("7. Logout")
        choice = input("Choose (1-7): ")

        if choice == "1":
            record_payment()
        elif choice == "2":
            update_payment()
        elif choice == "3":
            view_payments()
        elif choice == "4":
            income_summary()
        elif choice == "5":
            outstanding_list()
        elif choice == "6":
            monthly_summary()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


accountant_menu()