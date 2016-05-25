from django.contrib import admin

from chat.models import Message, UserChatRelation, Chat, DialogRelation


class ChatAdmin(admin.ModelAdmin):
    pass

class UserChatRelationAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

class DialogRelationAdmin(admin.ModelAdmin):
    list_display = ('chat', 'user_1', 'user_2',)

admin.site.register(DialogRelation, DialogRelationAdmin)

admin.site.register(Chat, ChatAdmin)
admin.site.register(UserChatRelation, UserChatRelationAdmin)
admin.site.register(Message, MessageAdmin)
