from django.contrib import admin

from chat.models import Message, UserChatRelation, Chat


class ChatAdmin(admin.ModelAdmin):
    pass

class UserChatRelationAdmin(admin.ModelAdmin):
    pass

class MessageAdmin(admin.ModelAdmin):
    pass

admin.site.register(Chat, ChatAdmin)
admin.site.register(UserChatRelation, UserChatRelationAdmin)
admin.site.register(Message, MessageAdmin)
