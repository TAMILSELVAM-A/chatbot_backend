from datetime import datetime
import pandas as pd
import uuid

file_path = "D:/Leela-Palace/backend/data/Leela_palace.csv"

def is_valid_date(date_text):
    try:
        check_date = datetime.strptime(date_text, "%Y-%m-%d")
        if check_date.date() < datetime.today().date():
            return False
        return True
    except ValueError:
        return False


def book_hotel(location, room_type, guest_name, checkin_date, checkout_date):
    df = pd.read_csv(file_path)

    df["Location"] = df["Location"].str.strip().str.lower()
    df["Room Type"] = df["Room Type"].str.strip().str.lower()
    df["Availability"] = df["Availability"].str.strip().str.lower()

    available_room = df[
        (df["Location"] == location.lower()) &
        (df["Room Type"] == room_type.lower()) &
        (df["Availability"] == "available")
    ]

    if available_room.empty:
        return "Sorry, the requested room is not available."

    booking_id = str(uuid.uuid4())[:8]
    df.loc[available_room.index[0], ["Booking ID", "Guest Name", "Check-in Date", "Check-out Date", "Booking Status"]] = [
        booking_id, guest_name, checkin_date, checkout_date, "Confirmed"
    ]

    df.to_csv(file_path, index=False)
    return f"Booking confirmed! Your Booking ID is {booking_id}."

def check_booking_status(booking_id):
    df = pd.read_csv(file_path)
    df["Booking ID"] = df["Booking ID"].astype(str)

    booking = df[df["Booking ID"] == booking_id.strip()]
    if booking.empty:
        return "No booking found. Please check your Booking ID and try again."

    details = booking.iloc[0]
    return (f"Booking Details:\n"
            f"Hotel: {details['Hotel Name']}\n"
            f"Location: {details['Location']}\n"
            f"Room: {details['Room Type']}\n"
            f"Guest: {details['Guest Name']}\n"
            f"Check-in: {details['Check-in Date']}\n"
            f"Check-out: {details['Check-out Date']}\n"
            f"Status: {details['Booking Status']}")
