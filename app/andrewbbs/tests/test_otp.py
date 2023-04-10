from django.test import TestCase
from django.conf import settings

from ..auth.verify import get_otp_provider
from ..auth.OTP.local import OTP as LOCAL_OTP
from ..auth.OTP.twilio import OTP as TWILIO_OTP

class VerifyTestCase(TestCase):
    
  def test_get_otp_provider(self):
    settings.OTP_PROVIDER = "twilio"
    otp_provider = get_otp_provider()
    self.assertEqual(otp_provider, TWILIO_OTP)

    settings.OTP_PROVIDER = "local"
    otp_provider = get_otp_provider()
    self.assertEqual(otp_provider, LOCAL_OTP)
  
  def test_local_send_code(self):
    otp_provider = LOCAL_OTP
    otp_provider.send_code("1234567890")
    self.assertNotEqual(otp_provider.CODE, "")
  
  def test_local_verify_code(self):
    otp_provider = LOCAL_OTP
    otp_provider.send_code("1234567890")

    otp_status = otp_provider.verify_code("1234567890", "1234567")
    self.assertEqual(otp_status, "pending")

    otp_status = otp_provider.verify_code("1234567890", otp_provider.CODE)
    self.assertEqual(otp_status, "approved")
