import json
from datetime import datetime, timedelta

DATA_FILE = "appointments.json"

def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except:
        return []

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)


def generate_id(data):
    if not data:
        return 1
    return max(a["id"] for a in data) + 1

def is_valid_datetime(date_str, time_str):
    try:
        datetime.strptime(date_str, "%d-%m-%Y")
        datetime.strptime(time_str, "%H:%M")
        return True
    except:
        return False

def is_sunday(date_str):
    day = datetime.strptime(date_str, "%d-%m-%Y")
    return day.weekday() == 6 

def is_slot_available(data, doctor, date, time):
    for appt in data:
        if (appt["doctor"] == doctor and
            appt["date"] == date and
            appt["time"] == time):
            return False
    return True

def next_available_slot(data, doctor, date):
    start = datetime.strptime(date + " 09:00", "%d-%m-%Y %H:%M")
    end = datetime.strptime(date + " 17:00", "%d-%m-%Y %H:%M")

    while start <= end:
        t = start.strftime("%H:%M")
        if is_slot_available(data, doctor, date, t):
            return t
        start += timedelta(minutes=30)
    return None


def add_appointment(data):
    patient = input("Enter patient name: ")
    doctor = input("Enter doctor name: ")
    date = input("Enter date (DD-MM-YYYY): ")
    time = input("Enter time (HH:MM): ")

    if not is_valid_datetime(date, time):
        print("\n❌ Invalid date/time format!")
        return

    if is_sunday(date):
        print("\n🚫 Cannot book appointments on Sundays!")
        return

    if not is_slot_available(data, doctor, date, time):
        print(f"\n❌ Slot {time} is already booked!")
        suggestion = next_available_slot(data, doctor, date)
        if suggestion:
            print(f"👉 Next available slot: {suggestion}")
        else:
            print("❌ No available slots for this doctor today.")
        return

    appt = {
        "id": generate_id(data),
        "patient": patient,
        "doctor": doctor,
        "date": date,
        "time": time
    }
    data.append(appt)
    save_data(data)
    print("\n✅ Appointment booked successfully!")
    print(f"📌 Appointment ID: {appt['id']}")

def view_appointments(data):
    if not data:
        print("\n📭 No appointments in the system.")
        return

    print("\n📋 ALL APPOINTMENTS")
    for appt in data:
        print(f"[{appt['id']}] {appt['date']} {appt['time']} - {appt['patient']} (Dr. {appt['doctor']})")

def search_by_date(data):
    date = input("Enter date (DD-MM-YYYY): ")
    print(f"\n📅 Appointments on {date}:")
    found = False
    for appt in data:
        if appt["date"] == date:
            print(f"[{appt['id']}] {appt['time']} - {appt['patient']} with Dr. {appt['doctor']}")
            found = True
    if not found:
        print("No appointments found.")

def search_by_doctor(data):
    doctor = input("Enter doctor name: ")
    print(f"\n🩺 Appointments for Dr. {doctor}:")
    found = False
    for appt in data:
        if appt["doctor"].lower() == doctor.lower():
            print(f"[{appt['id']}] {appt['date']} {appt['time']} - {appt['patient']}")
            found = True
    if not found:
        print("No appointments found.")

def search_by_patient(data):
    patient = input("Enter patient name: ")
    print(f"\n🧍 Appointments for {patient}:")
    found = False
    for appt in data:
        if appt["patient"].lower() == patient.lower():
            print(f"[{appt['id']}] {appt['date']} {appt['time']} - Dr. {appt['doctor']}")
            found = True
    if not found:
        print("No appointments found.")

def daily_schedule(data):
    doctor = input("Enter doctor name: ")
    date = input("Enter date (DD-MM-YYYY): ")

    print(f"\n📘 Schedule for Dr. {doctor} on {date}")
    found = False
    for appt in data:
        if appt["doctor"].lower() == doctor.lower() and appt["date"] == date:
            print(f"{appt['time']} - {appt['patient']}  (ID {appt['id']})")
            found = True
    if not found:
        print("No appointments today for this doctor.")

def cancel_appointment(data):
    try:
        appt_id = int(input("Enter appointment ID to cancel: "))
        for appt in data:
            if appt["id"] == appt_id:
                data.remove(appt)
                save_data(data)
                print("\n🗑 Appointment cancelled successfully.")
                return
        print("❌ Appointment ID not found.")
    except:
        print("❌ Invalid input.")

def reschedule_appointment(data):
    try:
        appt_id = int(input("Enter Appointment ID to reschedule: "))
        for appt in data:
            if appt["id"] == appt_id:
                print(f"\nCurrent: {appt['date']} {appt['time']}")

                new_date = input("Enter new date (DD-MM-YYYY): ")
                new_time = input("Enter new time (HH:MM): ")

                if not is_valid_datetime(new_date, new_time):
                    print("❌ Invalid date/time format.")
                    return

                if is_sunday(new_date):
                    print("🚫 Cannot schedule on Sundays.")
                    return

                if not is_slot_available(data, appt["doctor"], new_date, new_time):
                    print(f"❌ Slot not available.")
                    return

                appt["date"] = new_date
                appt["time"] = new_time
                save_data(data)
                print("\n🔄 Appointment rescheduled successfully!")
                return

        print("❌ Appointment not found.")
    except:
        print("❌ Invalid input.")

def main():
    data = load_data()

    while True:
        print("\n========== HEALTHCARE APPOINTMENT SYSTEM ==========")
        print("1. Book Appointment")
        print("2. View All Appointments")
        print("3. Search by Date")
        print("4. Search by Doctor")
        print("5. Search by Patient")
        print("6. Doctor Daily Schedule")
        print("7. Cancel Appointment")
        print("8. Reschedule Appointment")
        print("9. Exit")

        choice = input("Enter choice: ")

        if choice == "1": add_appointment(data)
        elif choice == "2": view_appointments(data)
        elif choice == "3": search_by_date(data)
        elif choice == "4": search_by_doctor(data)
        elif choice == "5": search_by_patient(data)
        elif choice == "6": daily_schedule(data)
        elif choice == "7": cancel_appointment(data)
        elif choice == "8": reschedule_appointment(data)
        elif choice == "9":
            print("\n👋 Exiting system...")
            break
        else:
            print("❌ Invalid option. Try again!")

if __name__ == "__main__":
    main()

