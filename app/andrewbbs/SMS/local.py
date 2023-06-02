import random
import string

class SMS:

  OTP_CODE = ""

  def otp_send_code(receiver):
    SMS.OTP_CODE = ''.join(random.choices(string.digits, k=6))
    print(f"code for {receiver} is {SMS.OTP_CODE}")
    return True 

  def otp_verify_code(receiver, code):
    if code == SMS.OTP_CODE:
      return "approved"
    else:
      return "pending"
    
  def send_sms(receiver, message):
    print(f"Sending SMS to {receiver} with message: {message}")
    return True
  
