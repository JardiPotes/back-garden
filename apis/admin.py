from django.contrib import admin

from .models import Comment, Garden, Photo

admin.site.register(Garden)
admin.site.register(Photo)
admin.site.register(Comment)
