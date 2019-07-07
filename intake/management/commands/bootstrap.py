from django.core.management.base import BaseCommand

from intake.models import Capacity, CountryOfOrigin, Language, LodgingType, Sex, State

from datetime import datetime

class Command(BaseCommand):
    help = '''

    '''

    # def add_arguments(self, parser):
    #     parser.add_argument('action', nargs='+', type=str)

    def handle(self, *args, **options):
        start = datetime.today()
        self.initialize_capacities()
        self.initialize_lodging_types()
        self.initialize_languages()
        self.initialize_states()
        self.initialize_countries_of_origin()
        self.initialize_sex()
        done = datetime.today()

    def initialize_capacities(self):
        self.stdout.write(self.style.WARNING('Initializing model Capacities'))
        volunteer_capacities = (
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
        for cap in volunteer_capacities:
            cap, cap_c = Capacity.objects.get_or_create(name=cap)
            if cap_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(vtype)s to model Capacities' % {'vtype': cap}))

    def initialize_lodging_types(self):
        self.stdout.write(self.style.WARNING('Initializing model LodgingTypes'))
        lodging_types = (
            ('dormitory'),
            ('hotel'),
            ('motel'),
            ('other'),
        )
        for lt in lodging_types:
            lt, lt_c = LodgingType.objects.get_or_create(lodging_type=lt)
            if lt_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(ltype)s to model LodgingTypes' % {'ltype': lt}))

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

    def initialize_states(self):
        states = (
            ('al', 'Alabama'),
            ('ak', 'Alaska'),
            ('az', 'Arizona'),
            ('ar', 'Arkansas'),
            ('ca', 'California'),
            ('co', 'Colorado'),
            ('ct', 'Connecticut'),
            ('de', 'Delaware'),
            ('dc', 'Washington D.C.'),
            ('fl', 'Florida'),
            ('ga', 'Georgia'),
            ('hi', 'Hawaii'),
            ('id', 'Idaho'),
            ('il', 'Illinois'),
            ('in', 'Indiana'),
            ('ia', 'Iowa'),
            ('ks', 'Kansas'),
            ('ky', 'Kentucky'),
            ('la', 'Louisiana'),
            ('me', 'Maine'),
            ('md', 'Maryland'),
            ('ma', 'Massachusetts'),
            ('mi', 'Michigan'),
            ('mn', 'Minnesota'),
            ('ms', 'Mississippi'),
            ('mo', 'Missouri'),
            ('mt', 'Montana'),
            ('ne', 'Nebraska'),
            ('nv', 'Nevada'),
            ('nh', 'New Hampshire'),
            ('nj', 'New Jersey'),
            ('nm', 'New Mexico'),
            ('ny', 'New York'),
            ('nc', 'North Carolina'),
            ('nd', 'North Dakota'),
            ('oh', 'Ohio'),
            ('ok', 'Oklahoma'),
            ('or', 'Oregon'),
            ('pa', 'Pennsylvania'),
            ('pr', 'Puerto Rico'),
            ('ri', 'Rhode Island'),
            ('sc', 'South Carolina'),
            ('sd', 'South Dakota'),
            ('tn', 'Tennessee'),
            ('tx', 'Texas'),
            ('ut', 'Utah'),
            ('vt', 'Vermont'),
            ('va', 'Virginia'),
            ('wa', 'Washington State'),
            ('wv', 'West Virginia'),
            ('wi', 'Wisconsin'),
            ('wy', 'Wyoming'),
            ('other', 'Other')
        )
        self.stdout.write(self.style.WARNING('Initializing model States'))
        for st, state in states:
            state, state_c = State.objects.get_or_create(
                name=state,
                abbreviation=st
            )
            if state_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(name)s to model States' % {'name': state.name}))

    def initialize_countries_of_origin(self):
        countries = (
            ("Guatemala"),
            ("Honduras"),
            ("El Salvador"),
            ("Mexico"),
            ("Argentina"),
            ("Bolivia"),
            ("Brazil"),
            ("Chile"),
            ("Colombia"),
            ("Costa Rica"),
            ("Cuba"),
            ("Dominican Republic"),
            ("Ecuador"),
            ("French Guiana"),
            ("Guadeloupe"),
            ("Haiti"),
            ("Martinique"),
            ("Mexico"),
            ("Nicaragua"),
            ("Panama"),
            ("Paraguay"),
            ("Peru"),
            ("Saint Martin"),
            ("Uruguay"),
            ("Venezuela"),
            ("Algeria"),
            ("Angola"),
            ("Benin"),
            ("Botswana"),
            ("Burkina Faso"),
            ("Burundi"),
            ("Cameroon"),
            ("Canary Islands"),
            ("Cape Verde"),
            ("Central African Republic"),
            ("Ceuta"),
            ("Chad"),
            ("Comoros"),
            ("Côte d'Ivoire"),
            ("Democratic Republic of the Congo"),
            ("Djibouti"),
            ("Egypt"),
            ("Equatorial Guinea"),
            ("Eritrea"),
            ("Ethiopia"),
            ("Gabon"),
            ("Gambia"),
            ("Ghana"),
            ("Guinea"),
            ("Guinea-Bissau"),
            ("Kenya"),
            ("Lesotho"),
            ("Liberia"),
            ("Libya"),
            ("Madagascar"),
            ("Madeira"),
            ("Malawi"),
            ("Mali"),
            ("Mauritania"),
            ("Mauritius"),
            ("Mayotte"),
            ("Melilla"),
            ("Morocco"),
            ("Mozambique"),
            ("Namibia"),
            ("Niger"),
            ("Nigeria"),
            ("Republic of the Congo"),
            ("Réunion"),
            ("Rwanda"),
            ("Saint Helena"),
            ("São Tomé and Príncipe"),
            ("Senegal"),
            ("Seychelles"),
            ("Sierra Leone"),
            ("Somalia"),
            ("South Africa"),
            ("Sudan"),
            ("Swaziland"),
            ("Tanzania"),
            ("Togo"),
            ("Tunisia"),
            ("Uganda"),
            ("Western Sahara"),
            ("Zambia"),
            ("Zimbabwe"),
            ('Other')
        )
        self.stdout.write(self.style.WARNING('Initializing model CountryOfOrigin'))
        for country in countries:
            coo, coo_c = CountryOfOrigin.objects.get_or_create(
                country=country,
            )
            if coo_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(country)s to model CountryOfOrigin' % {'country': coo.country}))

    def initialize_sex(self):
        sex_choices = (
            ("Female"),
            ("Male"),
            ('Other')
        )
        self.stdout.write(self.style.WARNING('Initializing model Sex'))
        for sex in sex_choices:
            so, so_c = Sex.objects.get_or_create(
                sex=sex,
            )
            if so_c:
                self.stdout.write(self.style.SUCCESS('\tSuccessfully added %(sex)s to model Sex' % {'sex': so.sex}))
