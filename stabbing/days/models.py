
import json
import math
import urllib.parse, urllib.request, urllib.error
from datetime import date, datetime, timedelta
from decimal import Decimal

from django.db import models
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from django.utils import timezone


class VerifiedEventManager(models.Manager):
    """Custom query manager for retrieving only current articles."""

    def get_queryset(self):
        """Get most recent articles that are between publish and expiry date"""
        return super().get_queryset()\
            .filter(is_pending_verification=False)\
            .order_by('-datetime_event')


class _AbstractLocation(models.Model):
    """Data stored for a particular event location."""
    number = models.IntegerField(help_text="The number/block of the address",
                                 blank=True)
    street = models.CharField(max_length=255, blank=False,
        help_text="The street name ONLY (no numbers)")
    city = models.CharField(max_length=64, blank=False, default="Ottawa")
    province = models.CharField(max_length=32, blank=False, default="Ontario")
    country = models.CharField(max_length=64, blank=False, default="Canada")

    # Spatial information
    lat = models.DecimalField(max_digits=12, decimal_places=9, editable=False)
    lng = models.DecimalField(max_digits=12, decimal_places=9, editable=False)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """Save latitude and longitude information for the location"""
        self.lat, self.lng = self.geocode(address={
            "number": self.number,
            "street": self.street,
            "city": self.city,
            "province": self.province,
            "country": self.country
        })
        super().save(*args, **kwargs)

    @staticmethod
    def geocode(address):
        """Retrieve the coordinates for an address from Google's API"""
        # URLencode the address to avoid problems with spaces etc.
        urlencoded_address = {k: urllib.parse.quote_plus(str(v))
                              for k, v in address.items()}

        # Format the different parameters into a single string for Google
        address = "{number} {street}, {city}, {province}, {country}"\
            .format(**urlencoded_address)

        # Make the request from Google
        maps_api_url = "?".join([
            "http://maps.googleapis.com/maps/api/geocode/json",
            urllib.parse.urlencode({"address": address, "sensor": False})
        ])
        try:
            response = urllib.request.urlopen(maps_api_url)
        except urllib.error.HTTPError:
            return 0, 0
        data = json.loads(response.read().decode('utf8'))

        if data['status'] == 'OK':
            lat = data['results'][0]['geometry']['location']['lat']
            lng = data['results'][0]['geometry']['location']['lng']
            return Decimal(lat), Decimal(lng)
        else:
            return 0, 0
            #raise ValueError("Couldn't determine geographic location.")


class _AbstactEvent(models.Model):
    """Data stored for a particular event."""
    datetime_event = models.DateTimeField(default=datetime.now, blank=False)
    article_url = models.URLField()
    submitted_by = models.CharField(null=True, blank=True, max_length=64)
    is_fatal = models.BooleanField()
    is_pending_verification = models.BooleanField(default=False)
    comments = models.TextField(null=True, blank=True)
    site = models.ForeignKey(Site, on_delete=models.CASCADE, default=1)
    on_site = CurrentSiteManager()

    objects = VerifiedEventManager()

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


class LastStabbing(_AbstactEvent, _AbstractLocation):
    """Stabbing events"""

    verb = "Stab"
    noun = "Stabbing"

    class Meta:
        verbose_name = "Last Stabbing"
        verbose_name_plural = "Last Stabbings"


class LastShooting(_AbstactEvent, _AbstractLocation):
    """Shooting events"""

    verb = "Shoot"
    noun = "Shooting"

    class Meta:
        verbose_name = "Last Shooting"
        verbose_name_plural = "Last Shootings"

