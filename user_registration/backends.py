from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, id_number=None):
        try:
            user = User.objects.get(username=username)
            if user.check_password(id_number):
                return user
        except User.DoesNotExist:
            return None
