"""
    inyoka.portal.management.commands.stats
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    This module provides a command to the Django ``manage.py`` file that outputs some statistics about the portal.
    In some time in the future, these should be converted to a proper view.

    :copyright: (c) 2011-2024 by the Inyoka Team, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
from django.core.management.base import BaseCommand
from django.db.models import Count
from django.db.models.functions import TruncYear

from inyoka.forum.models import Topic
from inyoka.portal.user import User


class Command(BaseCommand):
    help = "Outputs some statistics about the portal"

    def last_logins_grouped_by_year(self):
        query = (User.objects.annotate(year=TruncYear('last_login')).values('year')
                 .annotate(c=Count('id')).values('year', 'c').order_by('year'))

        for e in query:
            print(e['year'], e['c'])

    def threads_per_year(self):
        t_years = (Topic.objects.annotate(year=TruncYear('last_post__pub_date'))
                   .values('year').annotate(c=Count('id')).values('year', 'c')
                   .order_by('year'))

        for t in t_years:
            print(t['year'], t['c'])

    def handle(self, **options):
        self.last_logins_grouped_by_year()
        # TODO self.threads_per_year()

"""
TODO

--Benutzeranmeldungen / Monat
SELECT date_trunc('month', date_joined) AS month, count(id) AS users FROM portal_user GROUP BY month ORDER BY month;

--Ikhaya-Artikel / Monat
SELECT date_trunc('month', pub_date) AS month, count(id) AS articles FROM ikhaya_article GROUP BY month ORDER BY month;

--Wikiänderungen / Monat
SELECT date_trunc('month', change_date) AS month, count(id) AS wiki_edits FROM wiki_revision GROUP BY month ORDER BY month;

--Neue Wikiseiten / Monat
SELECT date_trunc('month', change_date) AS month, count(page_id) AS new_pages FROM (SELECT page_id, min(change_date) as change_date FROM wiki_revision GROUP BY page_id) AS page_created GROUP BY month ORDER BY month;


--Benutzeranmeldungen / Jahr
SELECT date_trunc('year', date_joined) AS year, count(id) AS users FROM portal_user GROUP BY year ORDER BY year;

--Ikhaya-Artikel / Jahr
SELECT date_trunc('year', pub_date) AS year, count(id) AS articles FROM ikhaya_article GROUP BY year ORDER BY year;

--Wikiänderungen / Jahr
SELECT date_trunc('year', change_date) AS year, count(id) AS wiki_edits FROM wiki_revision GROUP BY year ORDER BY year;

--Neue Wikiseiten / Jahr
SELECT date_trunc('year', change_date) AS year, count(page_id) AS new_pages FROM (SELECT page_id, min(change_date) as change_date FROM wiki_revision GROUP BY page_id) AS page_created GROUP BY year ORDER BY year;

-- Posts / Jahr
SELECT date_trunc('year', pub_date) AS year, count(id) AS posts FROM forum_post GROUP BY year ORDER BY year;
"""
