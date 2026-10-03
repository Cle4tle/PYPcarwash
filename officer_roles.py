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

def register_customer(name, _id):
    """adds a customer to the customers.txt file"""
    customer_info = load_entries(CUSTOMERS_file)
    customer_info.append(_id + "," + name + "\n")
    save_entries(CUSTOMERS_file,customer_info)

def book_by_id(_id, date,time):
    """adds a booking specified by the id of a customer and date to the booking.txt file
    , and adds priority to distinguish booking at the same date"""
    book_info = load_entries(BOOKING_file)
    book_info.append(_id + "," + date + "," + time + "\n")
    save_entries(BOOKING_file, book_info)

def cancel_booking(_id, date, time):
    """cancels a booking by the id and date"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:
        curr_id = entry.split(",")[0]
        curr_date = entry.split(",")[1]
        curr_time = entry.split(",")[2]
        if curr_date == date and curr_id == _id and curr_time == time:
            book_info.remove(entry)
            break
    save_entries(BOOKING_file, book_info)

def reschedule_booking(_id, prev_date, prev_time, new_date, new_time):
    """updates (change date and time) booking specified by the id, date and time"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:

        curr_id = entry.split(",")[0]

        curr_date = entry.split(",")[1]

        curr_time = entry.split(",")[2]

        if curr_date == prev_date and curr_id == _id and curr_time == prev_time + "\n":
            new_entry = _id + "," + new_date + "," + new_time
            book_info[book_info.index(entry)] = new_entry
            break
    save_entries(BOOKING_file, book_info)

def view_booking_by_id(_id):
    """display the current bookings of the customer by id"""
    book_info = load_entries(BOOKING_file)
    for entry in book_info:
        if entry.split(",")[0] == _id:
            print("Current bookings :-> ")
            print("Date : " + entry.split(",")[1] + " At " + entry.split(",")[2])
#book_by_id("0001", "4/12/2026", "4:30PM")
#cancel_booking("0001", "3/12/2026","4PM")
#view_booking_by_id("0001")
