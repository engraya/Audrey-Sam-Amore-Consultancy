from django.contrib import admin
from .models import Favorite, Appointment, Client
# Register your models here.

admin.site.register(Appointment)
admin.site.register(Client)
