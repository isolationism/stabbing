from django.contrib import admin
from . import models


@admin.register(models.LastStabbing)
class LastStabbingAdmin(admin.ModelAdmin):
    list_display = ('date_stabbed', 'article_url', 'submitted_by')
    ordering = ('-date_stabbed',)
    search_fields = ('article_url', 'submitted_by')
