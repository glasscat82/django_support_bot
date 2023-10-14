from django.contrib import admin
from .models import *


@admin.register(Bot)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","title","token")
    list_display_links = ("id","title")  
    save_as = True 

@admin.register(Chat)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("id","name","chat_id", "token")
    list_display_links = ("id","name") 
    save_as = True 

# admin.site.register(Chat)

admin.site.site_title = "SupportBot 0.1v"
admin.site.site_header = "SupportBot 0.1v"