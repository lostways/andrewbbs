from django.conf import settings

CODE = "12345"

class OTP:

  def send_code(receiver):
    print(f"code for {receiver} is {CODE}")
    return True 
    
  def verify_code(receiver, code):
    if code == CODE:
      return "approved"
    else:
      return False