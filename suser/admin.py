from django.contrib.gis import admin
# Register your models here.
from suser.models import User


class UserAdmin(admin.OSMGeoAdmin):
    list_display = (
        'phone',
        'first_name',
        'last_name',
        'email',
        'rating',
    )

admin.site.register(User, UserAdmin)

