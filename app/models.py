from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import admin
from django.contrib.sessions.models import Session

admin.site.register(Session)


class Register(models.Model):
    user =models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)  # Stores hashed password

    def set_password(self, raw_password):
        """Hashes and sets the password, then saves the object."""
        self.password = make_password(raw_password)
        self.save(update_fields=["password"])  # Save after hashing

    def check_password(self, raw_password):
        """Checks if the entered password matches the stored hashed password."""
        return check_password(raw_password, self.password)

    def __str__(self):
        return self.username



#otp model
import random
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import timedelta

class OTP(models.Model):
    email = models.EmailField()
    
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.created_at >= now() - timedelta(minutes=5)  # OTP expires in 5 minutes

    @staticmethod
    def generate_otp():
        return str(random.randint(100000, 999999))  # Generate 6-digit OTP
   

