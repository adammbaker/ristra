from django.core.management.base import BaseCommand
from django.utils import timezone
from intake.choices import CAPACITY_CHOICES
from intake.models import HeadOfHousehold, Organization

import logging
from datetime import timedelta

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = '''
    Culls the inactive Asylees and Households
    '''

    # def add_arguments(self, parser):
    #     parser.add_argument('action', nargs='+', type=str)

    def handle(self, *args, **options):
        cull_threshold = timedelta(1)
        start = timezone.localtime()
        self.cull_inactive(cull_threshold)
        done = timezone.localtime()

    def cull_inactive(self, cull_threshold):
        self.stdout.write(self.style.SUCCESS('Beginning cull'))
        for org in Organization.objects.all():
            hohs = HeadOfHousehold.objects.filter(
                intakebus__location__organization = org,
                travel_plan__eta__lte = timezone.localtime() + cull_threshold,
            )
            if hohs.count() > 0:
                logger.info(f"Beginning cull for {org.name}")
                for hoh in hohs:
                    logger.info(f"Culling {hoh.name}")
                    hoh.delete()
                    self.stdout.write(self.style.SUCCESS(f"Culling {hoh.name}"))
        return