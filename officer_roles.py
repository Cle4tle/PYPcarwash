'''This Module will have all the functions required for the officer roles'''
import random as rnd
import random as rnd
from constants import CUSTOMERS_file, BOOKING_file, REQUESTED_BOOKING_file, REQUESTED_EXTENSION_file
import input_validation as iv

def load_entries(file_entries):
    """Reads every line of the current file state,
     and returns the content as a list"""
    with open(file_entries, "r") as f:
        entries = f.readlines()
        return entries

def save_entries(file_entries, new_entries):
    """saves every line of the new entries and writes it back into the file"""
    with open(file_entries, "w") as f:

        for entry in new_entries:

            f.write(entry)

def register_customer(name, email, phone_number):
    """adds a customer to the customers.txt file"""
    customer_info = load_entries(CUSTOMERS_file)
    acc_exists = False
    for customer in customer_info:
        if customer.split(",")[0] == email:
            acc_exists = True
            break

    if acc_exists:
        return False
    else:
        customer_info.append(email + "," + name + "," + phone_number + "\n")
        save_entries(CUSTOMERS_file, customer_info)
        return True

def book_(email):
    """adds a booking and generates an id for the booking.csv file"""
    b_id = str(rnd.randint(1,9999))
    status = "Completed"
    serv_id = ""
    date = ""
    time = ""
    requested_booking_info = load_entries(REQUESTED_BOOKING_file)  # cus_email,serv_id, date, time
    book_info = load_entries(BOOKING_file)
    verified = verify_booking(email)
    for entry in requested_booking_info:
        field = entry.split(",")
        if field[0] == email:
            serv_id += field[1]
            date += field[2]
            time += field[3].strip(" ")
            requested_booking_info.remove(entry)


    if verified:
        book_info.append(b_id + ","+ email + "," +  serv_id + "," + date + "," + time + "," + status + "\n")
        save_entries(BOOKING_file, book_info)
        save_entries(REQUESTED_BOOKING_file, requested_booking_info)
        return b_id
    else:
        return False

def verify_booking(email):
    '''counts the number of bookings and return true if the bookings did not exceed the number of bookings allowed "3"'''
    book_info = load_entries(BOOKING_file)
    bookings_count = 0
    if len(book_info) == 0:
        return True

    for entry in book_info:
        if entry.split(",")[1] == email:
            bookings_count += 1
    if bookings_count > 3:
        return False
    else :
        return True

def cancel_booking(b_id):
    """cancels a booking by the id"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:

        curr_id = entry.split(",")[0]
        if curr_id == b_id:
            status = "Cancelled"
            new_entry = b_id + "," + entry.split(",")[1] + "," + entry.split(",")[2] + "," +  entry.split(",")[3] + "," + entry.split(",")[4]  + "," + status + "\n"
            book_info[book_info.index(entry)] = new_entry
            print("cancelled Succesfully")
            break

    save_entries(BOOKING_file, book_info)

def reschedule_booking(eml,b_id):
    """updates (change date and time) booking specified by the email and booking id"""
    requested_ex_info = load_entries(REQUESTED_EXTENSION_file )
    new_time = ""
    for entry in requested_ex_info:
        fields = entry.split(",")
        if fields[0] == eml and b_id== fields[1]:
            new_time += fields[2]
            requested_ex_info.remove(entry)
    book_info = load_entries(BOOKING_file)
    for entry in book_info:
        fields = entry.split(",")
        if b_id == fields[0] and eml == fields[1]:
            new_entry = b_id + ","+ eml + "," +  fields[2] + "," + fields[3] + "," + new_time + "," + fields[5]
            book_info[book_info.index(entry)] = new_entry
            break
    print("updated Succesfully")
    save_entries(BOOKING_file, book_info)
    save_entries(REQUESTED_EXTENSION_file, requested_ex_info)

def view_bookings():
    """display the current bookings"""
    book_info = load_entries(BOOKING_file)
    while True:
        print("1.View all Bookings")
        print("2.Filter Bookings")
        choice = iv.get_menu_choice_from_user(1, 2)

        if choice == 1:
            print("All Current Bookings :-> ")
            for entry in book_info:
                    print("ID : " + entry.split(",")[1] + "Booking ID: " + entry.split(",")[0] + " Date : " + entry.split(",")[3] + " At " + entry.split(",")[4], "Status : " + entry.split(",")[5])
        elif choice == 2:
            email = iv.get_valid_email_from_user("Enter Email to Show corrosponding Bookings: ")
            print(f"All {email} Bookings :-> ")
            for entry in book_info:
                if entry.split(",")[1] == email:
                    print("ID : " + email + "Booking ID: " + entry.split(",")[0] +  " Date : " + entry.split(",")[3] + " At " + entry.split(",")[4], "Status : " + entry.split(",")[5])
        dis = iv.get_Y_or_N_from_user("Cancel Booking (Y/N) ?")
        if dis == "y":
            cancel_id = iv.get_non_empty_text_from_user(" Enter the Booking ID: ")
            cancel_booking(cancel_id)
        elif dis == "n":
            continue
        elif len(dis) !=1:
            print("Please enter a valid choice")
        else:
            print("Please enter a valid choice")

def view_requested_bookings():
    '''display the requested bookings for the REQUESTED_BOOKING_file'''
    requested_booking_info= load_entries(REQUESTED_BOOKING_file)
    if len(requested_booking_info) == 0:
        print("No requests available")
        return False
    print("Email  " + "Service ID   " + "Date    " + "Time")
    for entry in requested_booking_info:
        field = entry.split(",")
        print(field[0] + "  " + field[1] + "  " + field[2] + "  " + field[3])

def view_requested_extensions():
    requested_ex_info= load_entries(REQUESTED_EXTENSION_file)
    if len(requested_ex_info) == 0:
        print("No requests available")
        return False
    print("Email  " + "Booking ID   " + "requested time")
    for entry in requested_ex_info:
        field = entry.split(",")
        print(field[0] + "  " + field[1] + "  " + field[2])



def sub_menu_customer():
    while True:
        print("1.Register")
        print("0.return")
        index = iv.get_menu_choice_from_user(0, 1)
        if index == 1:
            print("-----Register-----")
            name = iv.get_non_empty_text_from_user("name: ")
            email = iv.get_valid_email_from_user(
                "Email: ")
            phone = iv.get_phone_number_from_user("Phone Number: ")
            res = register_customer(name, email, phone)
            if not res:
                print("account already exists")
                continue
            else:
                break
        elif index == 0:
            break

def sub_menu_bookings_process():
    '''Sub Menu for all the Booking Processes'''
    while True:
        print("1. View Requested Bookings")
        print("2. View Requested Extensions")
        print("3. View Bookings")
        print("0. Exit")
        choice = iv.get_menu_choice_from_user(0, 3)
        if choice == 1:
            res = view_requested_bookings()
            if not res:
                continue
            eml = iv.get_valid_email_from_user("Enter the Email to approve request:  ")
            res = book_(eml)
            if not res:
                print("Booking failed!, this customer has too many bookings!")
        elif choice == 2:
            res = view_requested_extensions()
            if not res:
                continue
            eml = iv.get_valid_email_from_user("Enter the Email to approve request:  ")
            booking_id = iv.get_non_empty_text_from_user("Booking ID: ")
            reschedule_booking(eml, booking_id)
        elif choice == 3:
            view_bookings()
        else:
            break

def officer_menu():
    while True:
        print("-------officer------")
        print("1.Register customers")
        print("2.Process Bookings")
        print("0.log out")
        choice = iv.get_menu_choice_from_user(0,2)
        if choice == 1:
            res = sub_menu_customer()
        elif choice == 2:
            sub_menu_bookings_process()
        elif choice == 0:
            break