Where Is our field staff?
============================

At Dimagi we typically have a lot of employees spread throughout the globe. One of our engineers built a website to keep tabs on everyone's location, which you can check out at http://whereis.dimagi.com/

However, one of the problems is that often our staff are deployed to areas with little to no connectivity, which makes updating their locations from a rich web interface a challenge. One thought we had to make things easier for them is to provide email integration into the service. This would allow the field staff to send an email to whereis@dimagi.com with their location in the subject, and have this information automatically update their location. Your job is to start the process of building this functionality.

The goal is to take in the information from the email - time, sender, and freetext subject line, and convert it to a normalized record that can be used to update the whereis.dimagi.com database.
Your source data for lookups will be geonames. http://www.geonames.org/

You can use whatever data format you'd like to get the data, although we recommend either using the search api ( http://www.geonames.org/export/geonames-search.html ) or the text-download format http://download.geonames.org/export/dump/ . For text-download, the cities15000.zip file has a good set of locations to start with. Note that there is an hourly API limit of 2000 calls per hour, so be slightly judicious with API requests.

Likewise, you can assume any format you want for the incoming email data. For example, one source data format might be an array formatted like::

    [
        ["nick@dimagi.com", 2011-05-19 14:05,  "Dodoma"],
        ["alex@dimagi.com", 2011-05-22 16:22,  "Lusaka"]
    ]

The output of your program should be a normalized output of the person, time, and location (latitude and longitude) of the guessed location. The most likely format for this output would be a database table or set of tables, but other formats such as json, xml, or csv are perfectly fine.

Suggestions for bonus points and task extensions (in no particular order):
    * Integrate with a live email address.
    * Facilitate SMS integration by designing an API to accept the contents as an incoming HTTP request with a phone number and message body.
    * Partial matches of place names or regex search
    * Configurable options for choosing a place in the case of multiple matches. E.g.
    * Choice of place by greatest population
    * Choice of place by closest distance from person's most recently seen location
    * Add the ability to query someone's location at a given date/time.
    * Draw the outputted data on a map (we know we already have this, but you can take your own crack at it).
    * Reverse engineer/design the http://whereis.dimagi.com schema including history, people, places, etc.
    * Calculated Badges/Awards ("most distance covered", "biggest homebody", etc. extra bonus points for creative badges)
    * Design and implement API to re-POST the data to http://whereis.dimagi.com for us to integrate with.
    * Location Validation (you can't go from Delhi to Seattle in 15 minutes)
    * Write a source-data generator to test your system.
    * Roll your own! Feel free to wow us with your creativity.