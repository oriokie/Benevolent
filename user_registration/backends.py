from django.contrib.auth.backends import ModelBackend
from .models import User

class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, id_number=None):
        try:
            user = User.objects.get(username=username)
            if self.check_user_password(user, id_number):
                return user
        except User.DoesNotExist:
            return None

    def check_user_password(self, user, raw_password):
        return user.check_password(raw_password)
