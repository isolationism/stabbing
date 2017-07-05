from django.contrib import admin
from . import models


class LastEventAdmin(admin.ModelAdmin):
    list_display = ('datetime_event', 'article_url', 'submitted_by')
    ordering = ('-datetime_event',)
    search_fields = ('article_url', 'submitted_by')


@admin.register(models.LastStabbing)
class LastStabbingAdmin(LastEventAdmin):
    pass


@admin.register(models.LastShooting)
class LastShootingAdmin(LastEventAdmin):
    pass
