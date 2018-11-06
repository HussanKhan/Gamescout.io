from twilio.rest import Client

account = "ACe2e01506eb05a0e4b01dd8e4a4244fa5"
token = "a0b6e07d6f8e06c3516261262d41bc70"
client = Client(account, token)

message = client.messages.create(to="+12242412335", from_="+12242368932",
                                 body="Database Succesfully Filled!")
