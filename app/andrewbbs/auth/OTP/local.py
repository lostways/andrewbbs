import random
import string

class OTP:

  CODE = ""

  def send_code(receiver):
    OTP.CODE = ''.join(random.choices(string.digits, k=6))
    print(f"code for {receiver} is {OTP.CODE}")
    return True 

  def verify_code(receiver, code):
    if code == OTP.CODE:
      return "approved"
    else:
      return "pending"