from flight_search import FlightSearch
from flight_data import FlightData
from data_manager import DataManager

''''
Program Requirements:
1. Use the Flight Search and Sheety API to populate your own copy of the Google Sheet with International Air 
Transport Association (IATA) codes for each city. Most of the cities in the sheet include multiple airports, 
you want the city code (not the airport code see here).

2. Use the Flight Search API to check for the cheapest flights from tomorrow to 6 months later for all the cities in the Google Sheet.

3. If the price is lower than the lowest price listed in the Google Sheet then send an SMS to your own number with the Twilio API.

4. The SMS should include the departure airport IATA code, destination airport IATA code, departure city, destination city, flight price and flight dates. e.g.
example SMS: only $50 to fly from Houston-HOU to Denver-DEN from 2021-06-25 to 2021-07-15 (Year-month-day)

'''
data_manager = DataManager()
#data_manager.add_user_names()
data_manager.get_emails()

# initiliaze objects from classes
flight_search = FlightSearch()
flight_data = FlightData(flight_search)
flight_data.sheety_data()






