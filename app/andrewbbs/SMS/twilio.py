import logging
from django.conf import settings
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

logger = logging.getLogger(__name__)

client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
service = client.verify.services(settings.OTP_SERVICE_ID)


class SMS:
    def otp_send_code(receiver):
        verification = service.verifications.create(to=receiver, channel="sms")
        return verification.status

    def otp_verify_code(receiver, code):
        try:
            verification_check = service.verification_checks.create(
                to=receiver, code=code
            )
        except TwilioRestException:
            return False
        return verification_check.status

    def send_sms(receiver, message):
        try:
            response = client.messages.create(
                body=message,
                messaging_service_sid=settings.NOTIFY_SERVICE_ID,
                to=receiver,
            )
        except TwilioRestException as e:
            logger.error(f"Could Not Send SMS to {receiver}: {e}")
            return False
        return response
