from django.contrib import admin

from privileges.models import Grant, Privilege


admin.site.register(Grant)
admin.site.register(Privilege)
