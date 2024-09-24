from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Profile,Item,Messages

admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['bio','image']
    ordering=['bio']

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['start_bid','bid','title','description','bid_time_finish','bought']
    ordering = ['start_bid']

@admin.register(Messages)
class MessagesAdmin(admin.ModelAdmin):
    list_display = ['question_message','time_sent','sender','receiver', 'item']
    ordering = ['-time_sent']
