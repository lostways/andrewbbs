from django.conf import settings
from twilio.rest import Client

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)

def send_sms(receiver, message):
    response = client.messages.create(
        body = message,
        messaging_service_sid = settings.NOTIFY_SERVICE_ID,
        to = receiver
    )
    return response
