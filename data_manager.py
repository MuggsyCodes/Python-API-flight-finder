import requests
# Google Sheet Data Management - https://sheety.co/
import os

# this is the URL endpoint required to post data to spreadsheet
#city_end_point = 'https://api.sheety.co/897a97aa37b24984bb01f80417d3f791/flightDeals/prices'
city_end_point= os.environ.get('city_end_point')

#sheety_username = "Enzo"
#sheety_password = "Enzo_Oct18"
#sheety_authorization = "Basic RW56bzpFbnpvX09jdDE4"
sheety_authorization = os.environ.get('sheety_authorization')
user_post_end_point = os.environ.get('user_post_end_point')

class DataManager:
    #This class is responsible for talking to the Google Sheet.
    def __init__(self):

        self.headers = {
            "Authorization": sheety_authorization,
            "Content-Type": "application/json",
        }

    def get_rows(self):
        self.flight_deals = requests.get(url=city_end_point, headers=self.headers)
        print(self.flight_deals.status_code)
        self.flight_deals = self.flight_deals.json()
        return self.flight_deals


    def get_emails(self):
        self.email_address = requests.get(url=user_post_end_point, headers=self.headers)
        print(self.email_address.status_code)
        self.email_address = self.email_address.json()
        print(f'JSON of email addresses: {self.email_address}')
        self.list_of_emails = [entry["email"] for entry in self.email_address["users"]]
        print(f'list of emails: {self.list_of_emails}')
        return self.list_of_emails


    def parse_rows(self):
        '''returns to data from the g sheet'''
        self.row_data = self.get_rows()["prices"]
        return self.row_data

    # ask user to enter their name
    def user_input(self):
        self.first = input("Enter first name\n")
        self.last = input("Enter last name\n")
        self.email_1 = input("Please enter your email\n")
        self.email_2 = input("Please enter your email again\n")
        if self.email_1 == self.email_2:
            print("You're now in the Flight Club - welcome!")
            return self.first, self.last, self.email_1
        else:
            print("Try that email again")
            # rerun user input request
            self.user_input()


    # day 40 addition
    def add_user_names(self):
        '''add user names based on user inputting data'''
        # create json of user data
        # why does this only like lower case letters?
        f, l, e = self.user_input()
        self.real_data = {
            "user": {
                "first": f,
                "last": l,
                "email": e,
            }
        }
        # post user input data to sheety
        self.user_data = requests.post(url=user_post_end_point, json=self.real_data, headers=self.headers)
        print(self.user_data.raise_for_status())
        print(self.user_data.status_code)
        print(self.user_data.text)


