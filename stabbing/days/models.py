
from datetime import timedelta, date
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class LastStabbing(models.Model):
    """Information about the last stabbing in Ottawa"""
    date_stabbed = models.DateField(default=date.today, blank=False)
    article_url = models.URLField()
    submitted_by = models.CharField(null=True, blank=True, max_length=64)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    on_site = CurrentSiteManager()

    @property
    def days_since(self):
        """Returns integer representing number of days since last stabbing"""
        return (date.today() - self.date_stabbed).days

