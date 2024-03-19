from django.contrib import admin

from rideshare_app.models import CustomUser, Ride

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Ride)