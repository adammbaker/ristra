from django.core.management.base import BaseCommand

from intake.models import IntakeBuses, Organizations, VolunteerTypes

from datetime import datetime

class Command(BaseCommand):
    help = '''

    '''

    # def add_arguments(self, parser):
    #     parser.add_argument('action', nargs='+', type=str)

    def handle(self, *args, **options):
        start = datetime.today()
        self.initialize_volunteer_types()
        self.initialize_organizations()
        # self.initialize_intake_buses()
        done = datetime.today()

    def initialize_volunteer_types(self):
        self.stdout.write(self.style.WARNING('Initializing model VolunteerTypes'))
        volunteer_types = (
            ('Activities'),
            ('Change of Address'),
            ('Clothes'),
            ('Departure Bags'),
            ('Food'),
            ('Intake'),
            ('Medical'),
            ('Travel'),
            ('Transport'),
            ('Volunteer Coordinator'),
            ('Other'),
        )
        for voltype in volunteer_types:
            VolunteerTypes.objects.create(volunteer_type=voltype)
            self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(vtype)s to model VolunteerTypes' % {'vtype': voltype}))

    def initialize_organizations(self):
        self.stdout.write(self.style.WARNING('Initializing model Organizations'))
        org = Organizations.objects.create(
            name='Ristra Dev',
            location = 'Albuquerque, NM',
            head_name = 'Adam Baker',
            head_email = 'adam.m.baker@gmail.com',
            head_phone_number = '317-644-6119',
        )
        self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(name)s to model Organizations' % {'name': org.name}))
