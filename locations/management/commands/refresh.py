from django.core.management.base import BaseCommand, CommandError

from locations.models import Location
from whereis.geo import LocationLookupError, find_location
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
                location = find_location(email)
            except LocationLookupError, e:
                self.stdout.write("{} Skipping...".format(e))
                self.skipped += 1
                continue
            Location.objects.create(**location)
            self.stdout.write("Location loaded for {}\n".format(location["user"]))
            self.loaded += 1
        self.stdout.write("{} locations added, {} skipped.".format(self.loaded, self.skipped))

    def get_emails(self):
        email, password = get_credentials()
        emails = get_emails(email, password)
        return map(parse_email, emails)
