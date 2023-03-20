from .models import Member

class AccessCodeMiddleware:
  def __init__(self, get_response):
    self.get_response = get_response
    # One-time configuration and initialization.

  def __call__(self, request):
    # Code to be executed for each request before
    # the view (and later middleware) are called.

    # get unlocked codes
    codes = []
    if request.user.is_authenticated:
      member = Member.objects.get(handle=request.user.handle)
      codes = member.unlocked_codes
    elif 'codes' in request.session:
      codes = request.session['codes'] 
    
    request.unlocked_codes = codes
    
    response = self.get_response(request)

    # Code to be executed for each request/response after
    # the view is called.

    return response