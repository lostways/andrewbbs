from django.contrib.auth.backends import ModelBackend
from ..models import Member

class MemberBackend(ModelBackend):
  """Authenticate against the Member model."""

  def authenticate(self, request, handle):
    try:
      member = Member.objects.get(handle=handle)
      return member
    except Member.DoesNotExist:
      return None
  
  def get_user(self, user_id):
    try:
      return Member.objects.get(pk=user_id)
    except Member.DoesNotExist:
      return None