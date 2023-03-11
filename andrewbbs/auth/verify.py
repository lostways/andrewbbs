from django.conf import settings
from twilio.rest import Client

class OTP:
  def send_code(receiver):
    account_sid = settings.OTP_ACCOUNT_SID
    auth_token = settings.OTP_AUTH_TOKEN
    service_id = settings.OTP_SERVICE_ID

    client = Client(account_sid, auth_token)
    verification = client.verify \
        .services(service_id) \
        .verifications \
        .create(to=receiver, channel='sms')
    
    return verification.status

  def verify_code(receiver, code):
    account_sid = settings.OTP_ACCOUNT_SID
    auth_token = settings.OTP_AUTH_TOKEN
    service_id = settings.OTP_SERVICE_ID

    client = Client(account_sid, auth_token)
    verification_check = client.verify \
        .services(service_id) \
        .verification_checks \
        .create(to=receiver, code=code)
    
    return verification_check.status 
