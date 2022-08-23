from django.contrib import admin
from chat.models import Member, GroupChat, Message, Forbidden

class ForbidenAdmin(admin.ModelAdmin):
    list_display = ['Forbiden_msg', 'active_flag']

class BadWordsAdmin(admin.ModelAdmin):
    list_display = ['badwords',]


admin.site.register(Member)
admin.site.register(GroupChat)
admin.site.register(Message)
admin.site.register(Forbidden,ForbidenAdmin)
# admin.site.register(BadWords,BadWordsAdmin)
