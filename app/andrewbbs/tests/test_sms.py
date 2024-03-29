from django.test import TestCase
from django.conf import settings

from ..SMS.provider import get_sms_provider
from ..SMS.local import SMS as LOCAL_SMS


class SMSTestCase(TestCase):
    def test_get_sms_provider(self):
        settings.SMS_PROVIDER = "local"
        sms_provider = get_sms_provider()
        self.assertEqual(sms_provider, LOCAL_SMS)

    def test_local_otp_send_code(self):
        otp_provider = LOCAL_SMS
        otp_provider.otp_send_code("1234567890")
        self.assertNotEqual(otp_provider.OTP_CODE, "")

    def test_local_otp_verify_code(self):
        otp_provider = LOCAL_SMS
        otp_provider.otp_send_code("1234567890")

        otp_status = otp_provider.otp_verify_code("1234567890", "1234567")
        self.assertEqual(otp_status, "pending")

        otp_status = otp_provider.otp_verify_code("1234567890", otp_provider.OTP_CODE)
        self.assertEqual(otp_status, "approved")

    def test_local_send_sms(self):
        otp_provider = LOCAL_SMS
        sent = otp_provider.send_sms("1234567890", "Hello World")
        self.assertEqual(sent, True)
