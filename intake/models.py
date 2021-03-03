from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, User
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from django.utils.html import mark_safe
from hashid_field import HashidAutoField, HashidField
from intake.choices import *
from intake.generic_card import GenericCard
from shortener import shortener
from shortener.models import UrlMap

import hashlib
from datetime import timedelta
from django_cryptography.fields import encrypt
from socket import gethostbyname, gethostname

# Create your models here.
def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

class Capacity(models.Model):
    name = models.CharField(max_length=100, verbose_name='Capacity')

    def __str__(self):
        return '%(name)s' % {'name': self.name}

class Language(models.Model):
    language = models.CharField(max_length=100, verbose_name='Language Spoken')

    def __str__(self):
        return '%(lang)s' % {'lang': self.language}

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
    def is_capable_hotelrunner(self):
        return 'Hotel Runner' in self.capacities.values_list('name', flat=True)

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
    # campaign = models.OneToOneField('shortener.UrlMap', verbose_name="Active intake campaigns", on_delete=models.SET_NULL, null=True)
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
    organization = models.ManyToManyField('Organization', null=True)

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
    locations = models.ManyToManyField('Location', verbose_name='Locations')
    notes = models.TextField(verbose_name='Additional notes', null=True, blank=True)

    @property
    def location(self):
        return '%(city)s, %(state)s' % {
            'city': self.city,
            'state': self.state.upper(),
        }
    
    @property
    def is_active(self):
        for loc in self.locations.all():
            if loc.is_active:
                return loc.is_active
        return loc.is_active

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

class Location(models.Model):
    id = HashidAutoField(primary_key=True)
    intakebuses = models.ManyToManyField('IntakeBus', verbose_name='Intake Buses')
    lodging_type = models.CharField(verbose_name="Type of lodging provided", max_length=100, choices=LODGING_CHOICES, default='other')
    name = models.CharField(verbose_name="Name of the staging location", max_length=300)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def organization(self):
        return self.organization_set.first()
    
    @property
    def is_active(self):
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
        for hoh in self.headsofhousehold.all():
            if hoh.is_active:
                return hoh.is_active
        return hoh.is_active

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
    medicals = models.ManyToManyField('Medical', verbose_name='Medical Issues')
    sex = models.CharField(verbose_name="Sex of asylee", max_length=100, choices=SEX_CHOICES, default='other')
    date_of_birth = models.DateField(help_text="YYYY-MM-DD", verbose_name="Asylee's date of birth")
    phone_number = models.CharField(verbose_name="Asylee's phone number", max_length=300, null=True, blank=True)
    had_covid_disease = models.BooleanField(default=False, verbose_name='Has had COVID disease')
    had_covid_vaccine = models.BooleanField(default=False, verbose_name='Has received the COVID vaccine')
    covid_vaccine_doses = models.PositiveSmallIntegerField(default=0, verbose_name="COVID vaccine doses received", validators=[MinValueValidator(0),MaxValueValidator(2)])
    vaccine_received = models.CharField(max_length=100, null=True, blank=True, verbose_name="Vaccine manufacturer", choices=COVID_VACCINE_CHOICES)
    sick_covid = models.BooleanField(default=False, verbose_name="Is currently sick from COVID")
    sick_other = models.BooleanField(default=False, verbose_name="Is currently sick but not from COVID")
    # tsa_done = models.BooleanField(verbose_name="TSA paperwork is done", default=True)
    # legal_done = models.BooleanField(verbose_name="Legal paperwork is done", default=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def householdhead(self):
        return self.head_of_household.first()

    @property
    def age(self):
        return (timezone.now().date() - self.date_of_birth).days//365
    
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
    days_traveling = models.PositiveSmallIntegerField(verbose_name="Days spent traveling", default=0)
    days_detained = models.PositiveSmallIntegerField(verbose_name="Days spent in detention", default=0)
    country_of_origin = models.CharField(verbose_name="Country of origin", max_length=100, choices=COUNTRY_CHOICES, default='guatemala')

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
    zip = models.CharField(verbose_name="Sponsor's ZIP code", max_length=10, null=True, blank=True)
    relation = models.CharField(max_length=300, verbose_name="Relation to head of household", null=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def location(self):
        return '%(city)s, %(st_abbr)s' % {
            'city': self.city,
            'st_abbr': self.state.upper()
        }

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

class Medical(models.Model):
    id = HashidAutoField(primary_key=True)
    provider = models.ForeignKey(Profile, related_name="medical_provider", on_delete=models.SET(get_sentinel_user))
    entered_by = models.ForeignKey(Profile, related_name="data_entry_volunteer", on_delete=models.SET(get_sentinel_user))
    temperature = encrypt(models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="Temperature ºF"))
    # temperature = encrypt(models.FloatField(null=True, blank=True, verbose_name="Temperature ºF"))
    pulse = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Pulse"))
    blood_pressure = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Blood pressure"))
    weight = encrypt(models.DecimalField(max_digits=5, decimal_places=1, null=True, blank=True, verbose_name="Weight (lbs)", validators=[MinValueValidator(0)]))
    height = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Height"))
    oxgyen_level = encrypt(models.CharField(max_length=20, null=True, blank=True, verbose_name="Oxygen level"))
    vaccines_received = encrypt(models.CharField(max_length=300, null=True, blank=True, verbose_name="Vaccines received"))
    allergies = encrypt(models.CharField(max_length=200, null=True, blank=True, verbose_name="Allergies"))
    medications = encrypt(models.CharField(max_length=200, null=True, blank=True, verbose_name="Medications"))
    chronic_medical_problems = encrypt(models.CharField(max_length=200, null=True, blank=True, verbose_name="Chronic health issues"))
    symptoms = encrypt(models.TextField(verbose_name="Symptoms observed", null=True, blank=True))
    diagnosis = encrypt(models.TextField(verbose_name="Diagnosis", null=True, blank=True))
    treatment = encrypt(models.TextField(verbose_name="Treatment", null=True, blank=True))
    follow_up_needed = encrypt(models.TextField(verbose_name="Follow up needed", null=True, blank=True))
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def asylee(self):
        return self.asylee_set.first()

    def breadcrumbs(self, bc=''):
        parent = self.asylee
        model = 'Medical'
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/medical/%(id)s/overview">%(model)s</a></li>""" % {
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