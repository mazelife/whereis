from django.db import models


class Location(models.Model):
    """
    A model of a user's reported location.
    """
    user = models.ForeignKey('auth.User')
    timestamp = models.DateTimeField("When the location was reported.")
    raw_name = models.CharField("Raw location name", max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)

    class Meta:
        get_latest_by = "timestamp"
        order_with_respect_to = "user"
        ordering = ["-timestamp"]

    def __unicode__(self):
        return self.raw_name