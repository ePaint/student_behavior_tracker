from django.contrib import admin
from users.models import CustomUser, School

# Register your models here.
admin.site.register(School)
admin.site.register(CustomUser)
