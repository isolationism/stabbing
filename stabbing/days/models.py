
from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils import timezone

from datetime import timedelta, datetime, date
import math


class _AbstactEvent(models.Model):
    """Data stored for a particular event."""
    datetime_event = models.DateTimeField(default=datetime.now, blank=False)
    article_url = models.URLField()
    submitted_by = models.CharField(null=True, blank=True, max_length=64)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    on_site = CurrentSiteManager()

    class Meta:
        abstract = True

    @property
    def date_event(self):
        """Returns just the date of the event for backward-compatibility"""
        return date(year=self.datetime_event.year,
                    month=self.datetime_event.month,
                    day=self.datetime_event.day)

    @property
    def less_than_a_day_ago(self):
        """Returns true if the event occurred less than 24 hours ago."""
        return (timezone.now() - self.datetime_event).days < 1

    @property
    def days_since(self):
        """Returns integer representing number of days since the last event"""
        return (timezone.now() - self.datetime_event).days

    @property
    def hours_since(self):
        """Returns the integer hours since the last event"""
        return math.floor((timezone.now() -
                           self.datetime_event).seconds // 3600)

    @property
    def minutes_since(self):
        """Returns the integer minutes since the last event"""
        return math.floor((timezone.now() -
                           self.datetime_event).seconds // 60) % 60

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

