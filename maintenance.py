from constants import MAINTENANCE_file
import input_validation as iv

# read rows from maintenance.csv
def load_records():
    records = []
    try:
        f = open(MAINTENANCE_file, "r")
        f.readline()  # skip header row
        for line in f:
            line = line.strip()
            if line != "":
                records.append(line.split(","))
        f.close()
    except FileNotFoundError:
        print("maintenance.csv not found, starting fresh.")
    return records

# save list back to maintenance.csv
def save_records(records):
    f = open(MAINTENANCE_file, "w")
    f.write("maint_id,equipment,type,date,status\n")
    for row in records:
        f.write(row[0] + "," + row[1] + "," + row[2] + "," + row[3] + "," + row[4] + "\n")
    f.close()

def log_maintenance():
    records = load_records()
    new_id = "M" + str(len(records) + 1)
    equip = iv.get_non_empty_text_from_user("Enter equipment: ")
    job_type = iv.get_non_empty_text_from_user("Enter service type (Repair/Check): ")
    log_date = iv.get_valid_date_from_user("Enter date (YYYY-MM-DD): ")
    
    records.append([new_id, equip, job_type, log_date, "Pending"])
    save_records(records)
    print("Added new record with ID:", new_id)

def update_maintenance():
    records = load_records()
    check_id = input("Enter maintenance ID to update: ").strip()
    for row in records:
        if row[0].upper() == check_id.upper():
            print("Current status:", row[4])
            row[4] = iv.get_non_empty_text_from_user("Enter new status: ")
            save_records(records)
            print("Status updated.")
            return
    print("ID was not found.")

def view_maintenance():
    records = load_records()
    if len(records) == 0:
        print("No maintenance records to display.")
        return
    print("\nID    Equipment            Type        Date        Status")
    print("-" * 55)
    for row in records:
        print(f"{row[0]:<6}{row[1]:<21}{row[2]:<12}{row[3]:<12}{row[4]}")

def maintenance_summary():
    records = load_records()
    pending = 0
    completed = 0
    for row in records:
        if row[4].lower() == "pending":
            pending += 1
        elif row[4].lower() == "completed":
            completed += 1
    print(f"\nTotal: {len(records)} | Pending: {pending} | Completed: {completed}")

def maintenance_menu():
    while True:
        print("\n--- Maintenance Menu ---")
        print("1. Log record\n2. Update status\n3. View all\n4. Summary\n5. Exit")
        opt = iv.get_menu_choice_from_user(1, 5)
        if opt == 1:
            log_maintenance()
        elif opt == 2:
            update_maintenance()
        elif opt == 3:
            view_maintenance()
        elif opt == 4:
            maintenance_summary()
        elif opt == 5:
            print("Exiting...")
            break

if __name__ == "__main__":
    maintenance_menu()
