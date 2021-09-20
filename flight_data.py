from data_manager import DataManager
from notification_manager import NotificationManager

class FlightData:
    #This class is responsible for structuring the flight data.
    def __init__(self, flightsearch):
        # create FlightSearch object that was initialized in main.py
        self.flight_search_obj = flightsearch

    def sheety_data(self):
        '''iterate through the sheety data, compare prices and return a text'''
        row = DataManager()
        notifcation = NotificationManager()
        # row_data = row.get_rows()
        # return list of dictionaries from sheety
        row_data = row.parse_rows()
        for dicts in row_data:
            dest_city = dicts["iataCode"]
            price_to_beat = int(dicts["lowestPrice"])
            # udpate IATA code in flight search parameters
            self.flight_search_obj.basic_parameters["fly_to"] = dest_city
            the_city = dicts["city"]
            print(f'destination city: {the_city}')
            # return dictionary from basic flight search method
            basic_dictionary = self.flight_search_obj.basic_flight_search()
            try:
                low_price = int(basic_dictionary["low fare"])
                destination_city = basic_dictionary["destination city"]
                departure_city = basic_dictionary["departure city"]
                departure_airport = basic_dictionary["departure airport"]
                destination_airport = basic_dictionary["destination airport"]
            except TypeError as e:
                print(f'No flight data available for {the_city}: {e}')
            else:
                x = self.flight_search_obj.basic_parameters["dateFrom"]
                y = self.flight_search_obj.basic_parameters["dateTo"]
                z = self.flight_search_obj.basic_parameters["via_city"]
                self.link = f"https://www.google.com/flights?hl=en#flt={departure_city}.{destination_airport}.{x}"
                if low_price < price_to_beat:
                    #check if via_city paramter is empty
                    if not z:
                        # if via_city is empty, there are no stop over airports to report
                        message = f'Low price alert! Only ${low_price} to fly from {departure_city}-{departure_airport} to ' \
                                  f'{the_city}-{destination_airport}, from {x} to {y}\n{self.link}'
                        print(f'SMS message: {message}')
                    else:
                        s_o = self.flight_search_obj.basic_parameters["max_stopovers"]
                        message = f'Low price alert! Only ${low_price} to fly from {departure_city}-{departure_airport} to ' \
                                  f'{the_city}-{destination_airport}, from {x} to {y}\n Flight has {s_o} stopovers via {z}\n{self.link}'
                        print(f'SMS message: {message}')
                    # send an SMS to myself my bru
                    #notification.a_text_message(message)
                    # send an email to everyone in the list
                    # TODO: get email addy from sheety, compile into a list and send email body
                    list_of_emails = row.get_emails()
                    for email in list_of_emails:
                        notifcation.send_mail(message, email)

                else:
                    print(f'{low_price} greater than {price_to_beat}')