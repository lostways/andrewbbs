from django.test import TestCase
from django.conf import settings

from ..SMS.provider import get_sms_provider
from ..SMS.local import SMS as LOCAL_SMS
from ..SMS.twilio import SMS as TWILIO_SMS


class SMSTestCase(TestCase):
    def test_get_sms_provider(self):
        settings.SMS_PROVIDER = "twilio"
        sms_provider = get_sms_provider()
        self.assertEqual(sms_provider, TWILIO_SMS)

        settings.SMS_PROVIDER = "local"
        sms_provider = get_sms_provider()
        self.assertEqual(sms_provider, LOCAL_SMS)

    def test_local_otp_send_code(self):
        otp_provider = LOCAL_SMS
        otp_provider.send_code("1234567890")
        self.assertNotEqual(otp_provider.CODE, "")

    def test_local_otp_verify_code(self):
        otp_provider = LOCAL_SMS
        otp_provider.send_code("1234567890")

        otp_status = otp_provider.verify_code("1234567890", "1234567")
        self.assertEqual(otp_status, "pending")

        otp_status = otp_provider.verify_code("1234567890", otp_provider.CODE)
        self.assertEqual(otp_status, "approved")
