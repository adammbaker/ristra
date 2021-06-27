from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import mark_safe
from hashid_field import HashidAutoField, HashidField
from intake.choices import *
from intake.generic_card import GenericCard
from simple_history.models import HistoricalRecords

import hashlib
from datetime import datetime, timedelta
from django_cryptography.fields import encrypt
from socket import gethostbyname, gethostname

# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_default_travel_duration():
    return {'Air': [0,0], 'Bus': [0,0], 'Train': [0,0], 'Car': [0,0], 'other': [0,0]}

class Capacity(models.Model):
    name = models.CharField(max_length=100, verbose_name='Capacity')

    def __str__(self):
        return '%(name)s' % {'name': self.name}

class Language(models.Model):
    language = models.CharField(max_length=100, verbose_name='Language Spoken')

    def __str__(self):
        return f'{self.language}'

# class User(AbstractUser):
#     is_team_lead = models.BooleanField(default=False)
#     is_site_coordinator = models.BooleanField(default=False)
#     name = models.CharField(verbose_name='Your name', max_length=300)
#     email = models.EmailField(verbose_name='Your email', max_length=300, null=True)
#     phone_number = models.CharField(verbose_name='Your phone number', max_length=300)
#     languages = models.ManyToManyField('Language', verbose_name='Languages Spoken')
#     capacities = models.ManyToManyField('Capacity', verbose_name='Capacities')
#     campaigns = models.ManyToManyField('Campaign', verbose_name="Active intake campaigns")
#     notes = models.TextField(help_text="Additional notes", null=True, blank=True)

#     def to_card(self):
#         gc = GenericCard()
#         gc.body.title = self.name if self.name else None
#         gc.body.subtitle = self.username if self.username else None
#         gc.body.text = self.notes if self.notes else None
#         gc.body.card_link = ('mailto:' + self.email, self.email) if self.email else None
#         gc.footer.badge_groups = (('primary', self.languages.all()), ('secondary', self.capacities.all()))
#         return str(gc)

#     def organizations(self):
#         'Return a QuerySet of Organizations the user has access to'
#         return Organization.objects.filter(
#             id__in=[x.organization.id for x in self.campaigns.all() if x.campaign.date_expired > timezone.now()]
#         )

#     def locations(self, org):
#         'Return a QuerySet of Locations the user has access to for given org'
#         return Location.objects.filter(
#             id__in=[str(x.id) for x in org.locations.all()]
#         )

#     def intakebuses(self, loc):
#         'Return a QuerySet of IntakeBuses the user has access to for given loc'
#         return IntakeBus.objects.filter(
#             id__in=[str(x.id) for x in loc.intakebuses.all()]
#         )

#     def headsofhousehold(self, ib):
#         'Return a QuerySet of HeadOfHouseholds the user has access to for given ib'
#         return HeadOfHousehold.objects.filter(
#             id__in=[str(x.id) for x in ib.headofhousehold.all()]
#         )

#     def travelplans(self, hoh):
#         'Return the TravelPlan the user has access to for given hoh'
#         return hoh.travelplan

#     def sponsor(self, hoh):
#         'Return the Sponsor the user has access to for given hoh'
#         return hoh.sponsor

#     def asylees(self, hoh):
#         'Return a QuerySet of Asylees the user has access to for given hoh'
#         return hoh.asylees.all()

#     def medicals(self, asylee):
#         'Return a QuerySet of Medicals the user has access to for given asylee'
#         return asylee.medical.all()

#     def __str__(self):
#         return '%(name)s (%(username)s)\nCapable of %(capacities)s\nSpeaks %(languages)s' % {
#             'name': self.name,
#             'username': self.username,
#             'capacities': ', '.join(map(str, self.capacities.all())),
#             'languages': ', '.join(map(str, self.languages.all()))
#         }
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # is_team_lead = models.BooleanField(default=False)
    # is_site_coordinator = models.BooleanField(default=False)
    role = models.CharField(max_length=50, null=True)
    email_confirmed = models.BooleanField(default=False)
    # name = models.CharField(verbose_name='Your name', max_length=300)
    phone_number = models.CharField(verbose_name='Your phone number', max_length=300)
    languages = models.ManyToManyField('Language', verbose_name='Languages Spoken')
    capacities = models.ManyToManyField('Capacity', verbose_name='Capacities')
    # focus = models.ForeignKey('Capacity', on_delete=models.SET_NULL, null=True, verbose_name='Current Focus', related_name='current_focus')
    affiliation = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, verbose_name='Affiliated Organization')
    can_create_organization = models.BooleanField(default=False, verbose_name='Able to create organizations')
    organizations_created = models.ManyToManyField('Organization', verbose_name='Organizations created', related_name='organizations_created')
    # campaigns = models.ManyToManyField('Campaign', verbose_name="Active intake campaigns")
    history = HistoricalRecords()

    notes = models.TextField(help_text="Additional notes", null=True, blank=True)

    def to_card(self):
        gc = GenericCard()
        gc.body.title = self.user.get_full_name() if self.user.get_full_name() else None
        gc.body.subtitle = self.user.username if self.user.username else None
        gc.body.text = self.notes if self.notes else None
        gc.body.card_link = ('mailto:' + self.user.email, self.user.email) if self.user.email else None
        gc.footer.badge_groups = (('primary', self.languages.all()), ('secondary', self.capacities.all()))
        return str(gc)
    
    @property
    def name(self):
        return self.user.get_full_name()
    
    @property
    def is_capable_clothes(self):
        return 'Clothes' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_departurebags(self):
        return 'Departure Bags' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_food(self):
        return 'Food' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_concierge(self):
        return 'Concierge' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_intake(self):
        return 'Intake' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_medical(self):
        return 'Medical' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_travel(self):
        return 'Travel' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_transportation(self):
        return 'Transportation' in self.capacities.values_list('name', flat=True)

    @property
    def is_capable_volunteercoordinator(self):
        return 'Volunteer Coordinator' in self.capacities.values_list('name', flat=True)
    
    def __str__(self):
        return f'{self.name}'

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Campaign(models.Model):
    id = HashidAutoField(primary_key=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)

    @property
    def url(self):
        return f'{settings.BASE_URL}/s/{self.campaign.short_url}'
        return 'http://%(base_url)s%(url_modifier)ss/%(short_url)s' % {
            'base_url': gethostbyname(gethostname()),
            'url_modifier': ':8000/',
            'short_url': self.campaign.short_url
        }

    @property
    def affiliate_url(self):
        return 'http://%(base_url)s%(url_modifier)s%(aff_url)s' % {
            'base_url': gethostbyname(gethostname()),
            'url_modifier': ':8000',
            'aff_url': self.campaign.full_url + '?campaign=' + str(self.id)
        }

class Lead(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.SET(get_sentinel_user), primary_key=True)
    specialty = models.CharField(verbose_name="Team lead area", max_length=100, choices=CAPACITY_CHOICES, default='other')
    organization = models.OneToOneField('Organization', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username

class SiteCoordinator(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.SET(get_sentinel_user), primary_key=True)
    # organization = models.OneToOneField('Organization', on_delete=models.SET(get_sentinel_user), null=True)
    organization = models.ManyToManyField('Organization')

    def to_card(self):
        return self.user.to_card()

    def __str__(self):
        return '%(name)s [SC]' % {'name': self.user.name}

class Organization(models.Model):
    id = HashidAutoField(primary_key=True)
    is_valid = models.BooleanField(default=False)
    name = models.CharField(verbose_name='Name of the organization', max_length=500, unique=True)
    city = models.CharField(verbose_name='City', max_length=500, null=True)
    state = models.CharField(verbose_name="State", max_length=100, choices=STATE_CHOICES, default='nm')
    url = models.CharField(verbose_name='Website', max_length=500, null=True)
    associated_airport = models.CharField(max_length=150, choices=AIRPORT_CHOICES, default='abq')
    locations = models.ManyToManyField('Location', verbose_name='Locations')
    notes = models.TextField(verbose_name='Additional notes', null=True, blank=True)
    historical_families_count = models.IntegerField(default=0)
    historical_asylees_count = models.IntegerField(default=0)
    historical_sex_count = models.JSONField(default=dict)
    historical_age_count = models.JSONField(default=dict)
    historical_country_of_origin = models.JSONField(default=dict)
    historical_days_traveling = models.IntegerField(default=0)
    historical_days_in_detention = models.IntegerField(default=0)
    historical_detention_type = models.JSONField(default=dict)
    historical_sick_covid = models.IntegerField(default=0)
    historical_sick_other = models.IntegerField(default=0)
    historical_destinations = models.JSONField(default=dict)
    historical_languages_spoken = models.JSONField(default=dict)
    historical_travel_duration = models.JSONField(default=get_default_travel_duration) # time in hours
    historical_needs = models.JSONField(default=dict)
    history = HistoricalRecords()

    @property
    def location(self):
        return '%(city)s, %(state)s' % {
            'city': self.city,
            'state': self.state.upper(),
        }
    
    @property
    def is_active(self):
        if self.locations.exists():
            for loc in self.locations.all():
                if loc.is_active:
                    return loc.is_active
            return loc.is_active
    
    @property
    def historical_country_of_origin_sorted(self):
        return sorted(self.historical_country_of_origin, key= self.historical_country_of_origin.get, reverse=True)
    
    @property
    def historical_age_count_sorted(self):
        ages_0_3 = ('0mo','1mo','2mo','3mo','4mo','5mo','6mo','7mo','8mo','9mo','10mo','11mo','12mo','1yo','2yo','3yo',)
        ages_4_8 = ('4yo','5yo','6yo','7yo','8yo',)
        ages_9_12 = ('9yo','10yo','11yo','12yo',)
        ages_13_17 = ('13yo','14yo','15yo','16yo','17yo',)
        ages_18_24 = ('18yo','19yo','20yo','21yo','22yo','23yo','24yo',)
        ages_25_29 = ('25yo','26yo','27yo','28yo','29yo',)
        ages_30_34 = ('30yo','31yo','32yo','33yo','34yo',)
        ages_35_39 = ('35yo','36yo','37yo','38yo','39yo',)
        ages_40_44 = ('40yo','41yo','42yo','43yo','44yo',)
        ages_45_49 = ('45yo','46yo','47yo','48yo','49yo',)
        ages_50_59 = ('50yo','51yo','52yo','53yo','54yo','55yo','56yo','57yo','58yo','59yo',)
        ages_60_69 = ('60yo','61yo','62yo','63yo','64yo','65yo','66yo','67yo','68yo','69yo',)
        ages_70_79 = ('70yo','71yo','72yo','73yo','74yo','75yo','76yo','77yo','78yo','79yo',)
        ages_80_89 = ('80yo','81yo','82yo','83yo','84yo','85yo','86yo','87yo','88yo','89yo',)
        ages_90_99 = ('90yo','91yo','92yo','93yo','94yo','95yo','96yo','97yo','98yo','99yo',)
        ages_100_plus = ('100yo','101yo','102yo','103yo','104yo','105yo','106yo','107yo','108yo','109yo',)
        count_0_3 = sum([v for k,v in self.historical_age_count.items() if k in ages_0_3])
        count_4_8 = sum([v for k,v in self.historical_age_count.items() if k in ages_4_8])
        count_9_12 = sum([v for k,v in self.historical_age_count.items() if k in ages_9_12])
        count_13_17 = sum([v for k,v in self.historical_age_count.items() if k in ages_13_17])
        count_18_24 = sum([v for k,v in self.historical_age_count.items() if k in ages_18_24])
        count_25_29 = sum([v for k,v in self.historical_age_count.items() if k in ages_25_29])
        count_30_34 = sum([v for k,v in self.historical_age_count.items() if k in ages_30_34])
        count_35_39 = sum([v for k,v in self.historical_age_count.items() if k in ages_35_39])
        count_40_44 = sum([v for k,v in self.historical_age_count.items() if k in ages_40_44])
        count_45_49 = sum([v for k,v in self.historical_age_count.items() if k in ages_45_49])
        count_50_59 = sum([v for k,v in self.historical_age_count.items() if k in ages_50_59])
        count_60_69 = sum([v for k,v in self.historical_age_count.items() if k in ages_60_69])
        count_70_79 = sum([v for k,v in self.historical_age_count.items() if k in ages_70_79])
        count_80_89 = sum([v for k,v in self.historical_age_count.items() if k in ages_80_89])
        count_90_99 = sum([v for k,v in self.historical_age_count.items() if k in ages_90_99])
        count_100_plus = sum([v for k,v in self.historical_age_count.items() if k in ages_100_plus])
        return (('Ages 0 - 3', count_0_3),('Ages 4 - 8', count_4_8),('Ages 9 - 12', count_9_12),('Ages 13 - 17', count_13_17),('Ages 18 - 24', count_18_24),('Ages 25 - 29', count_25_29),('Ages 30 - 34', count_30_34),('Ages 35 - 39', count_35_39),('Ages 40 - 44', count_40_44),('Ages 45 - 49', count_45_49),('Ages 50 - 59', count_50_59),('Ages 60 - 69', count_60_69),('Ages 70 - 79', count_70_79),('Ages 80 - 89', count_80_89),('Ages 90 - 99', count_90_99),('Ages 100 +', count_100_plus))
    
    @property
    def historical_travel_duration_sorted(self):
        my_list = []
        for mode, nums in self.historical_travel_duration.items():
            mode_string = ''
            count, total_days = nums
            mode_string += f"{count} {'person' if count == 1 else 'people'} who {'has' if count == 1 else 'have'} traveled {total_days:.1f} total days"
            if count > 1:
                mode_string += f" ({total_days / 24.0 / count:.1f} hours on average)"
            my_list.append((mode, mode_string))
        return my_list

    def breadcrumbs(self, bc=''):
        model = self.name
        if bc != '':
            return """<li class="breadcrumb-item"><a href="/organization/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append("""<li class="breadcrumb-item">%(model)s</li>""" % {
                'model': model
            })
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))

    def to_card(self):
        gc = GenericCard()
        gc.body.title = self.name if self.name else None
        gc.body.subtitle = self.location if self.location else None
        gc.body.text = self.notes if self.notes else None
        gc.body.card_link = (self.url, self.url) if self.url else None
        gc.footer.see_more = '/organization/%d' % self.id
        return str(gc)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return '%(org_name)s (%(org_city)s, %(org_state)s)' % {
            'org_name': self.name,
            'org_city': self.city,
            'org_state': self.state.upper(),
        }

class RequestQueue(models.Model):
    # site_coordinator = models.OneToOneField('SiteCoordinator', on_delete=models.SET(get_sentinel_user), null=True)
    site_coordinator = models.ForeignKey('Profile', on_delete=models.SET(get_sentinel_user), null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)
    history = HistoricalRecords()

class Location(models.Model):
    id = HashidAutoField(primary_key=True)
    intakebuses = models.ManyToManyField('IntakeBus', verbose_name='Intake Buses')
    lodging_type = models.CharField(verbose_name="Type of lodging provided", max_length=100, choices=LODGING_CHOICES, default='other')
    name = models.CharField(verbose_name="Name of the staging location", max_length=300)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def organization(self):
        return self.organization_set.first()
    
    @property
    def is_active(self):
        if self.intakebuses.exists():
            for ib in self.intakebuses.all():
                if ib.is_active:
                    return ib.is_active
            return ib.is_active

    def breadcrumbs(self, bc=''):
        parent = self.organization
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/location/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))

    def test(self, msg=''):
        return self.organization.test('Loc' + msg)

    def __str__(self):
        return '%(name)s' % {
            'name': self.name,
        }

class IntakeBus(models.Model):
    id = HashidAutoField(primary_key=True)
    headsofhousehold = models.ManyToManyField('HeadOfHousehold', verbose_name='Heads of Households')
    origin = models.CharField(max_length=300, default='El Paso', verbose_name='City of origin of the bus')
    state = models.CharField(default='tx', verbose_name="State of origin of the bus", max_length=100, choices=STATE_CHOICES)
    arrival_time = models.DateTimeField(verbose_name="Arrival time of bus", default=timezone.now)
    number = models.CharField(verbose_name="Descriptive bus name", max_length=300, null=True, blank=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def location(self):
        return self.location_set.first()

    @property
    def origin_location(self):
        return '%(city)s, %(st_abbr)s' % {
            'city': self.origin,
            'st_abbr': self.state.upper()
        }
    
    @property
    def is_active(self):
        if self.headsofhousehold.exists():
            for hoh in self.headsofhousehold.all():
                if hoh.is_active:
                    return hoh.is_active
            return hoh.is_active
        # Bus may have just recently arrived; give them 6 hours to intake
        return timezone.now() - self.arrival_time < timedelta(0.25)

    @property
    def destination(self):
        return self.location_set.first().organization_set.first().location

    def breadcrumbs(self, bc=''):
        parent = self.location
        model = self.number
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/intakebus/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))

    def test(self, msg=''):
        return self.location.test('Ibus' + msg)

    def __str__(self):
        return 'Bus %(number)s arrived on %(arrived)s from %(origin)s, %(state)s' % {
            'number': self.number,
            'arrived': self.arrival_time.strftime("%b %d, '%y %H:%M"),
            'origin': self.origin,
            'state': self.state
        }

class Asylee(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name="Asylee's name")
    a_number = models.CharField(max_length=20, default='A-', verbose_name='Alien number')
    # medicals = models.ManyToManyField('Medical', verbose_name='Medical Issues')
    sex = models.CharField(verbose_name="Sex of asylee", max_length=100, choices=SEX_CHOICES, default='other')
    date_of_birth = models.DateField(help_text="YYYY-MM-DD", verbose_name="Asylee's date of birth")
    phone_number = models.CharField(verbose_name="Asylee's phone number", max_length=300, null=True, blank=True)
    had_covid_disease = models.BooleanField(default=False, verbose_name='Has had COVID disease in the past')
    had_covid_vaccine = models.BooleanField(default=False, verbose_name='Has received the COVID vaccine')
    covid_vaccine_doses = models.PositiveSmallIntegerField(default=0, verbose_name="COVID vaccine doses received", validators=[MinValueValidator(0),MaxValueValidator(2)])
    vaccine_received = models.CharField(max_length=100, null=True, blank=True, verbose_name="Vaccine manufacturer", choices=COVID_VACCINE_CHOICES)
    sick_covid = models.BooleanField(default=False, verbose_name="Is currently sick from COVID")
    sick_other = models.BooleanField(default=False, verbose_name="Is currently sick but not from COVID")
    needs_medical_attention = models.BooleanField(default=False, verbose_name="Needs medical attention")
    # tsa_done = models.BooleanField(verbose_name="TSA paperwork is done", default=True)
    # legal_done = models.BooleanField(verbose_name="Legal paperwork is done", default=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def householdhead(self):
        return self.head_of_household.first()

    @property
    def age(self):
        age_in_days = (timezone.now().date() - self.date_of_birth).days
        if age_in_days // 365 > 0:
            return f'{age_in_days //365}yo'
        return f'{age_in_days // 30}mo'
    
    @property
    def is_active(self):
        return self.householdhead.is_active
    
    @property
    def had_covid_disease_str(self):
        string = []
        if self.sex == 'male':
            string.append('He')
        elif self.sex == 'female':
            string.append('She')
        else:
            string.append('They')
        if self.had_covid_disease:
            if self.sex in ('male', 'female'):
                string.append('<b>HAS</b>')
            elif self.sex in ('other'):
                string.append('<b>HAVE</b>')
        else:
            if self.sex in ('male', 'female'):
                string.append('has <b>NOT</b>')
            elif self.sex in ('other'):
                string.append('have <b>NOT</b>')
        return ' '.join(string) + ' had COVID-19 disease.'
    
    @property
    def had_covid_vaccine_str(self):
        string = []
        if self.sex == 'male':
            string.append('He')
        elif self.sex == 'female':
            string.append('She')
        else:
            string.append('They')
        if self.had_covid_disease:
            if self.sex in ('male', 'female'):
                string.append('<b>HAS</b>')
            elif self.sex in ('other'):
                string.append('<b>HAVE</b>')
            string.append(f'received {self.covid_vaccine_doses} doses of the {self.vaccine_received} vaccine.')
        else:
            if self.sex in ('male', 'female'):
                string.append('has <b>NOT</b>')
            elif self.sex in ('other'):
                string.append('have <b>NOT</b>')
            string.append('received any COVID-19 vaccine.')
        return ' '.join(string)
    
    @property
    def pronoun(self):
        if self.sex == 'male':
            return 'he'
        if self.sex == 'female':
            return 'she'
        return 'they'

    def breadcrumbs(self, bc=''):
        parent = self.householdhead
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/asylee/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))
    
    def __str__(self):
        return f'{self.name}'
    
    class Meta:
        ordering = ['date_of_birth']

class HeadOfHousehold(Asylee):
    languages = models.ManyToManyField('Language', verbose_name='Languages Spoken')
    intake_by = models.ForeignKey('Profile', on_delete=models.SET(get_sentinel_user), null=True)
    asylees = models.ManyToManyField('Asylee', verbose_name='Asylees', related_name='head_of_household', default=None)
    sponsor = models.OneToOneField('Sponsor', verbose_name='Sponsors', on_delete=models.SET_NULL, null=True)
    travel_plan = models.OneToOneField('TravelPlan', verbose_name='Travel Plans', on_delete=models.SET_NULL, null=True)
    lodging = models.CharField(verbose_name="Room assignment", max_length=300, null=True, blank=True)
    destination_city = models.CharField(verbose_name="Destination city", max_length=300, null=True, blank=True)
    state = models.CharField(verbose_name="Destination state", max_length=100, choices=STATE_CHOICES, default='other')
    detention_type = models.CharField(max_length=100, choices=DETENTION_TYPE_CHOICES, default='other')
    days_traveling = models.PositiveSmallIntegerField(verbose_name="Days spent traveling", default=0)
    days_detained = models.PositiveSmallIntegerField(verbose_name="Days spent in detention", default=0)
    country_of_origin = models.CharField(verbose_name="Country of origin", max_length=100, choices=COUNTRY_CHOICES, default='guatemala')
    needs = models.ManyToManyField('HouseholdNeed', verbose_name="Household Needs", default=None)
    departure_bag_made = models.BooleanField(default=False, verbose_name='Departure bags made')
    food_made = models.BooleanField(default=False, verbose_name='Travel food made')
    history = HistoricalRecords()

    @property
    def intakebus(self):
        return self.intakebus_set.first()

    @property
    def destination(self):
        return '%(city)s, %(st_abbr)s' % {
            'city': self.destination_city,
            'st_abbr': self.state.upper()
        }
    
    @property
    def is_active(self):
        if self.travel_plan:
            if self.travel_plan.eta:
                return self.travel_plan.eta - timezone.now() > timedelta(-1)
        return True
    
    @property
    def is_sick_covid(self):
        if self.asylees.exists():
            for asylee in self.asylees.all():
                if asylee.sick_covid:
                    return asylee.sick_covid
        return False
    
    @property
    def time_at_location(self, as_string=True):
        # time_of_departure = timezone.localtime(timezone.now())
        time_of_departure = datetime.now()
        if self.travel_plan:
            time_of_departure = min(time_of_departure, self.travel_plan.departure_time)
        td = time_of_departure - self.intakebus.arrival_time
        if as_string:
            string = ''
            if td.days:
                string += f'{abs(td.days)}d '
            remaining_seconds = td.seconds % 86400
            hours = remaining_seconds // 3600 
            # remaining seconds
            remaining_seconds -= hours * 3600
            # minutes
            minutes = remaining_seconds // 60
            # remaining seconds
            seconds = remaining_seconds - (minutes * 60)
            # total time
            string += f'{hours:02d}h'
            return string
        return False
    
    @property
    def ages_and_sex(self):
        ages_and_sex = sorted(self.asylees.all(), key=lambda asy: asy.age, reverse=True)
        sexes = {'male': '♂︎', 'female': '♀︎', 'other': '⚧'}
        return ' '.join([f"{x.age}{sexes[x.sex]}"  for x in ages_and_sex])

    def breadcrumbs(self, bc=''):
        parent = self.intakebus
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/headofhousehold/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))

    def __str__(self):
        return f'{self.name}, Head of Household'

class Sponsor(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name="Sponsor's name", unique=True)
    phone_number = models.CharField(verbose_name="Sponsor's phone #", max_length=300, null=True)
    address = models.CharField(verbose_name="Sponsor's address", max_length=300, null=True)
    city = models.CharField(verbose_name="Sponsor's city", max_length=300, null=True)
    state = models.CharField(verbose_name="Sponsor's state", max_length=100, choices=STATE_CHOICES, default='other')
    zip_code = models.CharField(verbose_name="Sponsor's ZIP code", max_length=10, null=True, blank=True)
    relation = models.CharField(max_length=300, verbose_name="Relation to head of household", null=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
    history = HistoricalRecords()

    @property
    def location(self):
        return f'{self.city}, {self.state.upper()} {self.zip_code}'

    def __str__(self):
        return '%(name)s - %(phone)s, lives in %(loc)s' % {
            'name': self.name,
            'phone': self.phone_number,
            'loc': self.location,
        }

    def breadcrumbs(self, bc=''):
        parent = self.headofhousehold
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/sponsor/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))

class TravelPlan(models.Model):
    id = HashidAutoField(primary_key=True)
    arranged_by = models.ForeignKey('Profile', on_delete=models.SET(get_sentinel_user), null=True)
    confirmation = models.CharField(verbose_name="Confirmation #", max_length=100, null=True)
    destination_city = models.CharField(verbose_name="Destination city", max_length=100, null=True)
    destination_state = models.CharField(verbose_name="Destination state", max_length=100, choices=STATE_CHOICES, default='other')
    travel_date = models.DateTimeField(verbose_name="Departure time of travel", null=True)
    city_van_date = models.DateTimeField(verbose_name="Departure time on City Van", null=True)
    travel_food_prepared = models.BooleanField(verbose_name="Is travel food prepared?", default=False)
    eta = models.DateTimeField(verbose_name="Estimated arrival", null=True)
    travel_mode = models.CharField(verbose_name="Mode of travel", max_length=100, choices=TRAVEL_MODE_CHOICES, default='other')
    layovers = models.CharField(max_length=300, verbose_name='Layover(s)', null=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
    # Airline only
    flight_number = models.CharField(max_length=200, verbose_name='Flight #(s)', null=True)
    history = HistoricalRecords()

    @property
    def destination(self):
        return '%(city)s, %(st_abbr)s' % {
            'city': self.destination_city,
            'st_abbr': self.destination_state.upper()
        }

    @property
    def travel_time(self):
        if self.eta and self.travel_date:
            return self.eta - self.travel_date
        else:
            return 'No ETA entered'
    
    @property
    def departure_time(self):
        return min(self.travel_date, self.city_van_date)

    def breadcrumbs(self, bc=''):
        parent = self.headofhousehold
        model = 'Travel Plan'
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/travelplan/%(id)s/overview">%(model)s</a></li>""" % {
                'model': model
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return mark_safe(''.join(bc))

    def __str__(self):
        return 'Travel Plan for %(hoh_name)s: %(travel_company)s Conf #%(conf)s' % {
            'hoh_name': self.headofhousehold.name,
            'travel_company': self.travel_mode.title(),
            'conf': self.confirmation,
        }

# class Medical(models.Model):
#     id = HashidAutoField(primary_key=True)
#     provider = models.ForeignKey(Profile, related_name="medical_provider", on_delete=models.SET(get_sentinel_user))
#     entered_by = models.ForeignKey(Profile, related_name="data_entry_volunteer", on_delete=models.SET(get_sentinel_user))
#     temperature = encrypt(models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Temperature ºF"))
#     # temperature = encrypt(models.FloatField(null=True, blank=True, verbose_name="Temperature ºF"))
#     pulse = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Pulse"))
#     blood_pressure = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Blood pressure"))
#     weight = encrypt(models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Weight (lbs)", validators=[MinValueValidator(0)]))
#     height = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Height"))
#     oxgyen_level = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Oxygen level"))
#     vaccines_received = encrypt(models.CharField(max_length=300, null=True, blank=True, verbose_name="Vaccines received"))
#     allergies = encrypt(models.CharField(max_length=200, null=True, blank=True, verbose_name="Allergies"))
#     medications = encrypt(models.CharField(max_length=200, null=True, blank=True, verbose_name="Medications"))
#     chronic_medical_problems = encrypt(models.CharField(max_length=200, null=True, blank=True, verbose_name="Chronic health issues"))
#     symptoms = encrypt(models.TextField(verbose_name="Symptoms observed", null=True, blank=True))
#     diagnosis = encrypt(models.TextField(verbose_name="Diagnosis", null=True, blank=True))
#     treatment = encrypt(models.TextField(verbose_name="Treatment", null=True, blank=True))
#     follow_up_needed = encrypt(models.TextField(verbose_name="Follow up needed", null=True, blank=True))
#     notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

#     @property
#     def asylee(self):
#         return self.asylee_set.first()

#     def breadcrumbs(self, bc=''):
#         parent = self.asylee
#         model = 'Medical'
#         if bc != '':
#             return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/medical/%(id)s/overview">%(model)s</a></li>""" % {
#                 'model': model, 'id': self.id
#             } + bc)
#         if bc == '':
#             bc = []
#             bc.append('<nav aria-label="breadcrumb">')
#             bc.append('<ol class="breadcrumb">')
#             bc.append("""<li class="breadcrumb-item"><a href="/">Home</a></li>""")
#             bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
#                 'model': model
#             }))
#             bc.append('</ol>')
#             bc.append('</nav>')
#         return mark_safe(''.join(bc))

class Message(models.Model):
    MESSAGE_TYPES = [
        ('primary', 'Primary'),
        ('secondary', 'Secondary'),
        ('success', 'Success'),
        ('danger', 'Danger'),
        ('warning', 'Warning'),
        ('info', 'Info'),
        ('light', 'Light'),
        ('dark', 'Dark'),
    ]
    text = models.CharField(max_length=1000)
    dismissible = models.BooleanField(default=True)
    message_type = models.CharField(verbose_name="Message", max_length=100, choices=MESSAGE_TYPES)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'

    def __str__(self):
        return '%s' % (self.text[:100])


class Donate(models.Model):
    name = models.CharField(max_length=200, null=False, blank=False, verbose_name="Name")
    location = models.CharField(max_length=200, null=True, blank=True, verbose_name="Location")
    url = models.URLField(max_length=1000, null=True, blank=True, verbose_name="URL")
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.name}'


class HouseholdNeed(models.Model):
    need = models.CharField(max_length=100, verbose_name="Household Need")

    def __str__(self):
        return f'{self.need}'


# Triggers for historical data
# @receiver(post_save, sender=HeadOfHousehold)
# def hear_signal_headofhousehold(sender, instance, **kwargs):
#     if kwargs.get('created'):
#         print(instance.name, instance.ages_and_sex)
#         print(instance, type(instance))
#         return # if a new model object is created then return. You need to distinguish between a new object created and the one that just got updated.

#     #Do whatever you want. 
#     #Your trigger function content.
#     #Parameter "instance" will have access to all the attributes of the model being saved. To quote from docs : It's "The actual instance being saved."        
#     print('HOH SAVED', kwargs.keys())
#     print(instance.name, instance.ages_and_sex)
#     print('H:', instance.history.count(), instance.history.all())
#     # History increments on creation and then later save
#     # Objects with 2 history count are new
#     if instance.history.count() < 3:
#         print('Org', instance.intakebus.location.organization)
#         org = instance.intakebus.location.organization
#         org.historical_families_count += 1
#         print('Incrementing family count', )
#         if instance.country_of_origin in org.historical_country_of_origin.keys():
#             org.historical_country_of_origin[instance.country_of_origin] += 1
#         else:
#             org.historical_country_of_origin[instance.country_of_origin] = 1
#         org.historical_days_traveling += instance.days_traveling
#         org.historical_days_in_detention += instance.days_detained
#         if instance.detention_type in org.historical_detention_type.keys():
#             org.historical_detention_type[instance.detention_type] += 1
#         else:
#             org.historical_detention_type[instance.detention_type] = 1
#         if instance.destination in org.historical_destinations.keys():
#             org.historical_destinations[instance.destination] += 1
#         else:
#             org.historical_destinations[instance.destination] = 1
#         languages = '&'.join(list(instance.languages.values_list('language',flat=True)))
#         if languages in org.historical_languages_spoken.keys():
#             org.historical_languages_spoken[languages] += 1
#         else:
#             org.historical_languages_spoken[languages] = 1
#         # Asylee specific stuff but still associated with HoH
#         org.historical_asylees_count += instance.asylees.count()
#         if instance.sex in org.historical_sex_count.keys():
#             org.historical_sex_count[instance.sex] += 1
#         else:
#             org.historical_sex_count[instance.sex] = 1
#         if instance.age in org.historical_age_count.keys():
#             org.historical_age_count[instance.age] += 1
#         else:
#             org.historical_age_count[instance.age] = 1
#         for asy in instance.asylees.all():
#             if asy.sick_covid:
#                 org.historical_sick_covid += 1
#             if asy.sick_other:
#                 org.historical_sick_other += 1
#         org.save()
#         print('Org saved?')
#     for key in kwargs.keys():
#         print('Key:', key, 'Value:', kwargs[key])
#     return


# @receiver(pre_delete, sender=HeadOfHousehold)
# def pre_delete_headofhousehold(sender, instance, **kwargs):
#     print('HOH DELETED')
#     # historical_travel_duration = models.JSONField(default={'train':[0,0], 'plane':[0,0], 'bus':[0,0], 'private_car':[0,0]})
#     # historical_needs = models.JSONField(default=)
#     print(instance.name, instance.ages_and_sex)
#     return

