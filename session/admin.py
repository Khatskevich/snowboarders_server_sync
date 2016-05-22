from django.contrib import admin

from session.models import Session


class SessionAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'hash',
        'creation_time',
    )


admin.site.register(Session, SessionAdmin)
