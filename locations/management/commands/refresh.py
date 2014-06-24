from decimal import Decimal, InvalidOperation
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

from locations.models import Location
from whereis.geo import lookup_name
from whereis.mail import get_credentials, get_emails, parse_email


class Command(BaseCommand):
    args = ''
    help = 'Fetches emails and updates the database'
    loaded = 0
    skipped = 0

    def handle(self, *args, **options):
        try:
            emails = self.get_emails()
        except Exception, e:
            raise CommandError(e.message())
        for email in emails:
            try:
                user = User.objects.get(email=email["address"])
            except User.DoesNotExist:
                self.stdout.write("No user with the email {} was found. Skipping...\n".format(email["address"]))
                self.skipped += 1
                continue
            result = lookup_name(email["subject"])
            if result["totalResultsCount"] == 0:
                self.stdout.write("The location {} could not be found. Skipping...\n".format(email["subject"]))
                self.skipped += 1
                continue
            loc_data = result["geonames"][0]
            country = loc_data["countryName"]
            city = loc_data["name"] if loc_data["fclName"].startswith("city") else ""
            try:
                latitude = Decimal(loc_data["lat"])
                longitude = Decimal(loc_data["lng"])
            except InvalidOperation:
                self.stdout.write("Invalid lat/lon coords: {}, {}. Skipping...\n".format(
                    loc_data["lat"], loc_data["lng"]
                ))
                self.skipped += 1
                continue
            Location.objects.create(
                user=user,
                timestamp=email["date"],
                raw_name=email["subject"],
                country=country,
                city=city,
                latitude=latitude,
                longitude=longitude
            )
            self.stdout.write("Location loaded for {}\n".format(user))
            self.loaded += 1
        self.stdout.write("{} locations added, {} skipped.".format(self.loaded, self.skipped))


    def get_emails(self):
        email, password = get_credentials()
        emails = get_emails(email, password)
        return map(parse_email, emails)
