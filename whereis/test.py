import mail, geo


if __name__ == "__main__":
    emails = mail.get_emails(mail.EMAIL_ADDRESS, mail.EMAIL_PASSWORD)
    locations = map(mail.parse_email, emails)
    for loc in locations:
        res = geo.query_api(loc["name"])
        loc["lookup"] = res