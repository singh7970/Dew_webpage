from django.contrib.auth.backends import BaseBackend
from app.models import Register

class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Register.objects.get(email=email)
            if user.check_password(password):
                return user
        except Register.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        try:
            return Register.objects.get(pk=user_id)
        except Register.DoesNotExist:
            return None
