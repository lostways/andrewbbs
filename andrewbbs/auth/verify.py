from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

client = Client(settings.OTP_ACCOUNT_SID, settings.OTP_AUTH_TOKEN)
verify = client.verify.services(settings.OTP_SERVICE_ID)

class OTP:
  def send_code(receiver):
    verification = verify.create(to=receiver, channel='sms')
    return verification.status

  def verify_code(receiver, code):
    try:
      verification_check = verify.verification_checks.create(to=receiver, code=code)
    except TwilioRestException as e:
      return False
    return verification_check.status == 'approved' 