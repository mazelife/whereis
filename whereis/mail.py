from datetime import datetime
from email import parser
from email.utils import parseaddr, parsedate_tz
import poplib

from dateutil.tz import tzoffset


EMAIL_ADDRESS = "whereisthedimagiemployee@gmail.com"
EMAIL_PASSWORD = "horse house house horse"


class SubjectParseException(Exception):
    """ Raised when a subject line seems incorrectly formatted. """


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


def parse_data(email):
    """
    Extract needed data from a parsed email object.
    """
    time_tuple = parsedate_tz(email["date"])
    import pdb; pdb.set_trace()
    tzinfo = tzoffset(None, time_tuple[-1])
    date = datetime(*time_tuple[:6], tzinfo=tzinfo)
    return {
        "name": email["subject"],
        "date": date,
        "email": parseaddr(email["From"])[1],
    }


if __name__ == "__main__":
    emails = get_emails(EMAIL_ADDRESS, EMAIL_PASSWORD)
    locations = map(parse_data, emails)
