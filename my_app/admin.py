from django.contrib import admin

# Register your models here.
from my_app.models import User, Event

admin.site.register(User)
admin.site.register(Event)