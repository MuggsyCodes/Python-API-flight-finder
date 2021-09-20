from twilio.rest import Client
import os
import smtplib

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure

#account_sid = 'AC3dcf09e323743e2f96702b5d81f70c7c'
account_sid = os.environ.get('account_sid')
#auth_token = 'b2dc7df154ee2b2ed6d8e37d125258e5'
auth_token= os.environ.get('auth_token')
#phone_number = '+19164149826'
phone_number = os.environ.get('phone_number')
email_pass = os.environ.get('email_pass')
# Twilio SMS API - https://www.twilio.com/docs/sms

class NotificationManager:
    #This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.sms_body = "blank message"

    def a_text_message(self, some_text):
        '''update message data'''
        self.sms_body = some_text
        print(f'SMS message: {self.sms_body}')
        # create SMS
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(
            body=self.sms_body,
            from_=phone_number,
            to='+17133309510'
        )

        print(message.status)

    def send_mail(self, quote, email_address):
        '''requires email address and body of email'''
        self.connection = smtplib.SMTP("smtp.gmail.com")
        self.my_email = 'montemayor.r.t@gmail.com'

        # use with
        with smtplib.SMTP('smtp.gmail.com') as connection:
            # makes connection secure
            self.connection.starttls()
            self.connection.login(user=self.my_email, password=email_pass)

            self.connection.sendmail(from_addr=self.my_email,
                                to_addrs=email_address,
                                msg=f"Subject: New Low Price Flight!\n{quote}")

