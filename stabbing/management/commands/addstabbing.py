
from datetime import datetime, date
from sys import exit

from django.core.management.base import BaseCommand, CommandError
from django.contrib.sites.models import Site

from stabbing.days.models import (LastStabbing, LastShooting)


class Command(BaseCommand):
    help = "Add a stabbing/shooting event."

    def add_arguments(self, parser):
        # Positional args
        parser.add_argument(
            'url', action='store', dest='url', nargs=1, type=str,
            help="The URL of a news article describing the event")

        # Was this a stabbing?
        parser.add_argument(
            '--stabbing', action='store', dest='stabbing', nargs='?',
            default=False, type=bool, help='Specify that this was a stabbing.')

        # ... or a shooting?
        parser.add_argument(
            '--shoooting', action='store', dest='shooting', nargs='?',
            default=False, type=bool, help='Specify that this was a shooting.')

        # The Site ID, or 'what city had the event?'
        parser.add_argument(
            '--site', action='store', dest='siteid', nargs='?', default=1,
            type=int, help='Specify an explicit/alternate (integer) site ID')

        # The date as an ISO-style string; only parse if provided.
        parser.add_argument(
            '--date', action='store', dest='date', default=None,
            help='Specify an explicit event date (format: YYYY-MM-DD)')

        # Who provided this information? Default to me.
        parser.add_argument(
            '--by', action='store', dest='by', nargs='?',
            default=None,
            help='String specifying who submitted this latest event')

    def handle(self, *args, **options):
        """Simply loads and saves each member."""
        # The Site ID associates the event with a locale
        try:
            site = Site.objects.get(pk=options['siteid'])
        except Site.DoesNotExist:
            self.stdout.write("\nERROR: Site with ID {} does not exist.\n"
                              .format(options['siteid']))
            exit(1)

        if (not options['stabbing'] and not options['shooting']) or \
                options['stabbing'] and options['shooting']:
            self.stdout.write("\nERROR: Must specify one of either --stabbing "
                              "or --shooting so I know what to store..\n")
            exit(2)

        # If a date was defined, parse it, otherwise it happened today
        if options['date']:
            try:
                eventdate = datetime.strptime(options['date'], '%Y-%m-%d')\
                    .date()
            except ValueError:
                self.stdout.write("\nERROR: Couldn't parse date '{}' (must be "
                                  "formatted as YYYY-MM-DD)"
                                  .format(options['date']))
                exit(1)
        else:
            eventdate = date.today()

        # We have all the pieces; make the stabbing record
        if options['stabbing']:
            model_object = LastStabbing
        else:
            model_object = LastShooting

        event = model_object(**{
            'date_event': eventdate,
            'article_url': options['url'],
            'submitted_by': options['by'],
            'site': site,
        })
        event.save()
        self.stdout.write("\nAdded {} record {}.\n"
                          .format(event.noun, event.pk))
