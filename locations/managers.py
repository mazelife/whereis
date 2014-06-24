from django.db import models

from whereis.geo import haversine


class LocationQuerySet(models.query.QuerySet):

    def location_in_date_range(self, start, stop):
        """
        Return all locations inside the given date range.
        """
        return self.filter(timestamp__gte=start, timestamp__lte=stop)

    def nearest_to(self, longitude, latitude):
        """
        Return the location nearest to the given lat/long.
        """
        # FIXME: This could be quite slow. Perhaps employ geohashing or something similar to speed lookups.
        shortest_distance = None
        closest_location = None
        for loc in self.all():
            distance = haversine(loc.longitude, loc.latitude, longitude, latitude)
            if shortest_distance is None or distance < shortest_distance:
                shortest_distance = distance
                closest_location = loc
        return closest_location


class LocationManager(models.Manager):

    def get_query_set(self, **kwargs):
        model = models.get_model("locations", "Location")
        return LocationQuerySet(model)

    def __getattr__(self, attr, *args):
        try:
            return getattr(self.__class__, attr, *args)
        except AttributeError:
            return getattr(self.get_query_set(), attr, *args)
