import requests
import os
from datetime import datetime, timedelta
from pprint import pprint


# Kiwi Partners Flight Search API (Free Signup, Requires Credit Card Details) - https://partners.kiwi.com/
#
# Tequila Flight Search API Documentation - https://tequila.kiwi.com/portal/docs/tequila_api
# username: 
# password: 
# removed API
Tequilia_API_Key = os.environ.get('tequila_api')
#basic_search_end_point = "https://tequila-api.kiwi.com/v2/search"
basic_search_end_point = os.environ.get('basic_search_end_point')

today = datetime.today()
more_time = timedelta(weeks=6*4) # 6 months
more_time = today+more_time
more_time = more_time.strftime("%d/%m/%Y")
today = today.strftime("%d/%m/%Y")  # date as a string

class FlightSearch:
    #This class is responsible for talking to the Flight Search API.
    def __init__(self):

        self.headers = {
            "apikey": Tequilia_API_Key,
        }
        # sort by lowest price
        self.basic_parameters = {
            "fly_from": "HOU",
            "fly_to": "",
            "dateFrom": today,
            "dateTo": more_time,
            "flight_type": "oneway",
            "one_for_city": "1",
            "sort": "price",
            "curr": "USD",
            "max_stopovers": "0",
            "via_city": "",
        }



    def basic_flight_search(self):
        '''return data from Kiwi API based on IATA city code'''
        # create dictionary that is to be repopulated
        self.basic_dictionary = {
            "low fare": "blank",
            "destination city": "blank",
            "departure city": "blank",
            "departure airport": "blank",
            "destination airport": "blank",
            "dateFrom": self.basic_parameters["dateFrom"],
            "dateTo": self.basic_parameters["dateTo"],
        }
        self.basic_search = requests.get(url=basic_search_end_point, params=self.basic_parameters, headers = self.headers)
        print(f'The real status code: {self.basic_search.status_code}')
        # IMPORTANT: this is flight search data
        self.data = self.basic_search.json()
        print(f'Basic search json output:\n {self.data}')
        try:
            # self.test = self.data["data"][0]
            if len(self.data["data"]) == 0:
                print('No direct flights')
                # update max stopovers to 1
                self.basic_parameters["max_stopovers"] = "1"
                print(f'max stopovers: {self.basic_parameters["max_stopovers"]}')
                self.basic_search = requests.get(url=basic_search_end_point, params=self.basic_parameters,
                                                 headers=self.headers)
                # update flight data
                self.data = self.basic_search.json()
                #pretty print the data
                pprint(f'Updated basic search data, 1 stopover:\n {self.data}')
                self.test = self.data["data"][0]
        except IndexError as e:
            print(f'Empty list. No direct or 1 stop flights available {e}.')
        else:
            # iterate through json data for lowest price
            self.price = self.data["data"][0]["price"]
            print(f'low fare price: {self.price}')
            self.city_to = self.data["data"][0]["cityTo"]
            print(f'Desination city: {self.city_to}')
            self.city_from = self.data["data"][0]["cityCodeFrom"]
            print(f'Departure city: {self.city_from}')
            self.depart_airport = self.data["data"][0]["flyFrom"]
            print(f'Departure airport: {self.depart_airport}')
            self.destination_airport = self.data["data"][0]["flyTo"]
            print(f'Destination airport: {self.destination_airport}')
            #think I want to return a library of keys and values to be used in SMS alert
            self.basic_dictionary["low fare"] = self.price
            self.basic_dictionary["destination city"] = self.city_to
            self.basic_dictionary["departure city"] = self.city_from
            self.basic_dictionary["departure airport"] = self.depart_airport
            self.basic_dictionary["destination airport"] = self.destination_airport
            if self.basic_parameters["max_stopovers"] == "1":
                # update to include stop_over city
                #self.basic_dictionary["via_city"] = self.data["data"][0]["route"][0]["cityTo"]
                self.basic_parameters["via_city"] = self.data["data"][0]["route"][0]["cityTo"]
                return self.basic_dictionary
            else:
                return self.basic_dictionary
