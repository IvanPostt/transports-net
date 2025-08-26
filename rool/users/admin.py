from django.contrib import admin
from users.models import User, EmailVerification

# Register your models here.
admin.site.register(User)
admin.site.register(EmailVerification)
