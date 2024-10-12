from datetime import date, datetime
from langchain.tools import StructuredTool
from langchain_core.pydantic_v1 import BaseModel
import json

class BookHotelRoomArgsSchema(BaseModel):
    fullName: str
    email: str
    phoneNumber: str
    numberOfGuests: int
    checkInDate: str
    checkOutDate: str
    roomType: str
    includeBreakfast: str
    specialRequests: str

from dateutil.parser import parse

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def reserve_room(fullName, email, phoneNumber, numberOfGuests, checkInDate, checkOutDate, roomType, includeBreakfast, specialRequests):
    if fullName=="" or fullName=="Your Name":
        return "Please provide the full name"
    if email=="":
        return "Please provide the email address"
    if phoneNumber=="":
        return "Please provide the correct phone number"
    if is_date(checkInDate) == False:
        return "Please provide the correct check in date"
    if is_date(checkOutDate) == False:
        return "Please provide the correct check out date"
    checkInDateObject = datetime.strptime(checkInDate, '%Y-%m-%d')
    checkOutDateObject = datetime.strptime(checkOutDate, '%Y-%m-%d')
    if checkInDateObject.date() < date.today():
        return "Please note that reservation can be done only for the future. \
        Please provide the correct check in date"
    if checkOutDateObject < checkInDateObject:
        return "Appears that the check out date is earlier than the check in date. \
        Please provide the correct check in and check out dates"
    if numberOfGuests > 4:
        return "Please note that there can be only upto 4 guests allowed in a room. \
        Please provide the correct number of guests"
    else:
    # python object to be appended
        y = {
                "guest_name":fullName,
                "email":email,
                "phone_number":phoneNumber,
                "number_of_guests":numberOfGuests,
                "checkin":checkInDate,
                "checkout":checkOutDate,
                "room_type":roomType, 
                "breakfast_included":includeBreakfast,
                "special_request":specialRequests
            }

        write_json(y) 
        return "Your room has been booked successfully"

reserve_hotel_tool = StructuredTool.from_function(
  name = "reserve_room",
  description = "Reserve a room for the user in the hotel",
  func = reserve_room,
  args_schema=BookHotelRoomArgsSchema
)

# function to add to JSON
def write_json(new_data, filename='reservation.json'):
    try:
        with open(filename,'r+') as file:
            print("i am after file created")
            # First we load existing data into a dict.
            file_data = []
            file_data = json.load(file)
            print(file_data)
            # Join new_data with file_data inside emp_details
            # file_data["reservation_details"].append(new_data)
            file_data.append(new_data)
            # Sets file's current position at offset.
            file.seek(0)
            # convert back to json.
            json.dump(file_data, file, indent = 4)
    except FileNotFoundError:
        print("i am here")
        datafile = open(filename, "w")
        first_data = [{"reservation_details":
                        new_data  
                    }]
        new_data = [new_data]
        json.dump(new_data, datafile)
        datafile.close()


