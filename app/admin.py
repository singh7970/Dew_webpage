from django.contrib import admin


# Register your models here.
from .models import Register
from .models import OTP

admin.site.register(Register)
admin.site.register(OTP)



