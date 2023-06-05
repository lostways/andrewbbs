import importlib
from django.conf import settings


def get_sms_provider():
    # Import the OTP class based on the OTP_PROVIDER setting
    sms_module = importlib.import_module(f"andrewbbs.SMS.{settings.SMS_PROVIDER}")

    # Return the OTP class
    return sms_module.SMS
