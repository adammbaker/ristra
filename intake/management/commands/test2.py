from django.core.management.base import BaseCommand
from intake.choices import CAPACITY_CHOICES
from intake.models import Capacity, HouseholdNeed, Language

import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '''

    '''

    # def add_arguments(self, parser):
    #     parser.add_argument('action', nargs='+', type=str)

    def handle(self, *args, **options):
        start = datetime.now()
        self.test_logger()
        done = datetime.now()
        print('Done')

    def test_logger(self):
        self.stdout.write(self.style.WARNING('Initializing model Capacities'))
        logger.error("Test!!")