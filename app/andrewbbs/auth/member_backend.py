from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model


class MemberBackend(ModelBackend):
    """Authenticate against the Member model."""

    def authenticate(self, request, handle):
        User = get_user_model()
        try:
            user = User.objects.get(handle=handle)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        User = get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
