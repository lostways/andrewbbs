import importlib
from django.conf import settings

def get_otp_provider():
  # Import the OTP class based on the OTP_PROVIDER setting
  otp_module = importlib.import_module(f"andrewbbs.auth.OTP.{settings.OTP_PROVIDER}")

  # Assign the OTP class to the OTP variable
  OTP = otp_module.OTP

  # Return the OTP class
  return OTP