from django.contrib import admin
from .models import User, Garden

admin.site.register(Garden)
admin.site.register(User)
