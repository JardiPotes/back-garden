from django.contrib import admin

from .models import Comment, Conversation, Garden, Message, Photo

admin.site.register(Garden)
admin.site.register(Photo)
admin.site.register(Comment)
admin.site.register(Conversation)
admin.site.register(Message)
