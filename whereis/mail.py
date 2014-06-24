from datetime import datetime
from email import parser
from email.utils import parseaddr, parsedate_tz
import poplib

from dateutil.tz import tzoffset
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_credentials():
    """
    Get the correct email/password from the django settings file.
    """
    email = getattr(settings, "LOCATIONS_EMAIL_ADDRESS", None)
    password = getattr(settings, "LOCATIONS_EMAIL_PASSWORD", None)
    if not email:
        raise ImproperlyConfigured("The LOCATIONS_EMAIL_ADDRESS setting is missing.")
    if not password:
        raise ImproperlyConfigured("The LOCATIONS_EMAIL_PASSWORD setting is missing.")
    return email, password


def get_emails(email, password):
    """
    Takes a username/password for a POP account and returns a list of
    `parsed <https://docs.python.org/2/library/email.parser.html>`_ email messages.
    """
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(email)
    pop_conn.pass_(password)
    #Get messages from server:
    messages = [pop_conn.retr(i) for i in range(1, len(pop_conn.list()[1]) + 1)]
    # Concat message pieces:
    messages = ["\n".join(mssg[1]) for mssg in messages]
    #Parse message into an email object:
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    pop_conn.quit()
    return messages


def parse_email(email):
    """
    Extract needed data from a parsed email object.
    """
    time_tuple = parsedate_tz(email["date"])
    tzinfo = tzoffset(None, time_tuple[-1])
    date = datetime(*time_tuple[:6], tzinfo=tzinfo)
    return {
        "subject": email["subject"],
        "date": date,
        "address": parseaddr(email["From"])[1],
    }

