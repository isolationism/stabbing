
from datetime import timedelta, date
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager


class _AbstactEvent(models.Model):
    """Data stored for a particular event."""
    date_event = models.DateField(default=date.today, blank=False)
    article_url = models.URLField()
    submitted_by = models.CharField(null=True, blank=True, max_length=64)
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

    @property
    def days_since(self):
        """Returns integer representing number of days since the last event"""
        return (date.today() - self.date_event).days

    verb = None  # Define this in your subclass
    noun = None  # Define this in your subclass


class LastStabbing(_AbstactEvent):
    """Stabbing events"""

    verb = "Stab"
    noun = "Stabbing"

    class Meta:
        verbose_name = "Last Stabbing"
        verbose_name_plural = "Last Stabbings"


class LastShooting(_AbstactEvent):
    """Shooting events"""

    verb = "Shoot"
    noun = "Shooting"

    class Meta:
        verbose_name = "Last Shooting"
        verbose_name_plural = "Last Shootings"

