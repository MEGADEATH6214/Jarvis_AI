from django.contrib import admin
from .models import Chats

# Register your models here.

class ChatsAdmin(admin.ModelAdmin):
    model = Chats

admin.site.register(Chats, ChatsAdmin)