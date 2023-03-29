from django.contrib import admin
admin.site.site_header = "weather Portal"
admin.site.site_title = "Weather Admin Portal"
admin.site.index_title = "Welcome to weather Portal"

# Register your models here.
from .models import bus,bus_stop,driver,rutes
admin.site.register(bus)
admin.site.register(bus_stop)
admin.site.register(driver)
admin.site.register(rutes)