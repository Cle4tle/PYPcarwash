import random as rnd
from constants import CUSTOMERS_file, BOOKING_file

def load_entries(file_entries):
    """Reads every line of the current file state and returns the content as a list"""
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
def book_(email,serv_id, date,time):
    """adds a booking specified and generates an id for the booking and date to the booking.csv file"""
    b_id = str(rnd.randint(1,9999))
    status = "valid"
    book_info = load_entries(BOOKING_file)
    book_info.append(b_id + ","+ serv_id + "," +  email + "," + date + "," + time + "," + status + "\n") # field names style was adapted from https://wash2u.my/
    save_entries(BOOKING_file, book_info)

def verify_booking(email):
    '''counts the number of bookings'''
    book_info = load_entries(BOOKING_file)
    bookings_count = 0
    if len(book_info) == 0:
        return True

    for entry in book_info:
        if entry.split(",")[2] == email:
            bookings_count += 1
    if bookings_count > 5:
        return False
    else :
        return True
def cancel_booking(b_id):
    """cancels a booking by the id"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:

        curr_id = entry.split(",")[0]
        print(entry)
        if curr_id == b_id:
            status = "Cancelled"
            new_entry = b_id + "," + entry.split(",")[1] + "," + entry.split(",")[2] + "," +  entry.split(",")[3] + "," + entry.split(",")[4]  + "," + status + "\n"
            book_info[book_info.index(entry)] = new_entry
            break

    save_entries(BOOKING_file, book_info)

def reschedule_booking(b_id,new_date, new_time):
    """updates (change date and time) booking specified by the id, date and time"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:

        curr_id = entry.split(",")[0]

        if  curr_id == b_id :
            new_entry = b_id + "," + entry.split(",")[1] + "," + entry.split(",")[2] + "," + new_date + "," + new_time  + "," +entry.split(",")[5]
            book_info[book_info.index(entry)] = new_entry
            break
    save_entries(BOOKING_file, book_info)

def view_booking_by_id(email):
    """display the current bookings of the customer by id"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:
        if entry.split(",")[2] == email:
            print("Current bookings :-> ")
            print("ID : " + entry.split(",")[0] + " Date : " + entry.split(",")[3] + " At " + entry.split(",")[4], "Status : " + entry.split(",")[5])

