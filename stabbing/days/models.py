
from datetime import date
from django.db import models


class LastStabbing(models):
    """Information about the last stabbing in Ottawa"""
    date_stabbed = models.DateField(default=date.today, blank=False)
    article_url = models.URLField()
    submitted_by = models.CharField(null=True, blank=True, max_length=64)
