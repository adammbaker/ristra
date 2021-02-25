from django.core.management.base import BaseCommand
from django.utils import timezone
from intake.choices import CAPACITY_CHOICES
from intake.models import Capacity, Language


class Command(BaseCommand):
    help = '''

    '''

    # def add_arguments(self, parser):
    #     parser.add_argument('action', nargs='+', type=str)

    def handle(self, *args, **options):
        start = timezone.now()
        self.initialize_capacities()
        self.initialize_languages()
        # self.initialize_lodging_types()
        # self.initialize_states()
        done = timezone.now()

    def initialize_capacities(self):
        self.stdout.write(self.style.WARNING('Initializing model Capacities'))
        volunteer_capacities = [x[1] for x in CAPACITY_CHOICES]
        for cap in volunteer_capacities:
            cap, cap_c = Capacity.objects.get_or_create(name=cap)
            if cap_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(vtype)s to model Capacities' % {'vtype': cap}))

    def initialize_languages(self):
        self.stdout.write(self.style.WARNING('Initializing model Languages'))
        languages = (
            ('English'),
            ('Spanish'),
            ('Portuguese'),
            ('French'),
            ("Maya - Achi"),
            ("Maya - Awakatek"),
            ("Maya - Ch\'orti\'"),
            ("Maya - Chuj"),
            ("Maya - Itza\'"),
            ("Maya - Ixil"),
            ("Maya - Jakaltek"),
            ("Maya - K\'iche\'"),
            ("Maya - Kaqchiquel"),
            ("Maya - Mam"),
            ("Maya - Mopan"),
            ("Maya - Poqomam"),
            ("Maya - Poqomchi\'"),
            ("Maya - Q\'anjob\'al"),
            ("Maya - Q\'eqchi\'"),
            ("Maya - Sakapultek"),
            ("Maya - Sipakapense"),
            ("Maya - Tektitek"),
            ("Maya - Tz\'utujil"),
            ("Maya - Upsantek"),
            ('Other')
        )
        for lang in languages:
            lang, lang_c = Language.objects.get_or_create(language=lang)
            if lang_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(lang)s to model Languages' % {'lang': lang}))

    # def initialize_lodging_types(self):
    #     self.stdout.write(self.style.WARNING('Initializing model LodgingTypes'))
    #     lodging_types = (
    #         ('dormitory'),
    #         ('hotel'),
    #         ('motel'),
    #         ('other'),
    #     )
    #     for lt in lodging_types:
    #         lt, lt_c = LodgingType.objects.get_or_create(lodging_type=lt)
    #         if lt_c:
    #             self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(ltype)s to model LodgingTypes' % {'ltype': lt}))

    # def initialize_states(self):
    #     states = (
    #         ('al', 'Alabama'),
    #         ('ak', 'Alaska'),
    #         ('az', 'Arizona'),
    #         ('ar', 'Arkansas'),
    #         ('ca', 'California'),
    #         ('co', 'Colorado'),
    #         ('ct', 'Connecticut'),
    #         ('de', 'Delaware'),
    #         ('dc', 'Washington D.C.'),
    #         ('fl', 'Florida'),
    #         ('ga', 'Georgia'),
    #         ('hi', 'Hawaii'),
    #         ('id', 'Idaho'),
    #         ('il', 'Illinois'),
    #         ('in', 'Indiana'),
    #         ('ia', 'Iowa'),
    #         ('ks', 'Kansas'),
    #         ('ky', 'Kentucky'),
    #         ('la', 'Louisiana'),
    #         ('me', 'Maine'),
    #         ('md', 'Maryland'),
    #         ('ma', 'Massachusetts'),
    #         ('mi', 'Michigan'),
    #         ('mn', 'Minnesota'),
    #         ('ms', 'Mississippi'),
    #         ('mo', 'Missouri'),
    #         ('mt', 'Montana'),
    #         ('ne', 'Nebraska'),
    #         ('nv', 'Nevada'),
    #         ('nh', 'New Hampshire'),
    #         ('nj', 'New Jersey'),
    #         ('nm', 'New Mexico'),
    #         ('ny', 'New York'),
    #         ('nc', 'North Carolina'),
    #         ('nd', 'North Dakota'),
    #         ('oh', 'Ohio'),
    #         ('ok', 'Oklahoma'),
    #         ('or', 'Oregon'),
    #         ('pa', 'Pennsylvania'),
    #         ('pr', 'Puerto Rico'),
    #         ('ri', 'Rhode Island'),
    #         ('sc', 'South Carolina'),
    #         ('sd', 'South Dakota'),
    #         ('tn', 'Tennessee'),
    #         ('tx', 'Texas'),
    #         ('ut', 'Utah'),
    #         ('vt', 'Vermont'),
    #         ('va', 'Virginia'),
    #         ('wa', 'Washington State'),
    #         ('wv', 'West Virginia'),
    #         ('wi', 'Wisconsin'),
    #         ('wy', 'Wyoming'),
    #         ('other', 'Other')
    #     )
    #     self.stdout.write(self.style.WARNING('Initializing model States'))
    #     for st, state in states:
    #         state, state_c = State.objects.get_or_create(
    #             name=state,
    #             abbreviation=st
    #         )
    #         if state_c:
    #             self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(name)s to model States' % {'name': state.name}))
