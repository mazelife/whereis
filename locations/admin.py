from django.contrib import admin

from locations import models


class LocationAdmin(admin.ModelAdmin):

    list_display = ("__unicode__", "user", "timestamp")
    list_filter = ("user", )

admin.site.register(models.Location, LocationAdmin)