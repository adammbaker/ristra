from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
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
from socket import gethostbyname, gethostname

# Create your models here.
class Capacity(models.Model):
    name = models.CharField(max_length=100, verbose_name='Capacity')

    def __str__(self):
        return '%(name)s' % {'name': self.name}

class Language(models.Model):
    language = models.CharField(max_length=100, verbose_name='Language Spoken')

    def __str__(self):
        return '%(lang)s' % {'lang': self.language}

class User(AbstractUser):
    is_team_lead = models.BooleanField(default=False)
    is_site_coordinator = models.BooleanField(default=False)
    name = models.CharField(verbose_name='Your name', max_length=300)
    email = models.EmailField(verbose_name='Your email', max_length=300, null=True)
    phone_number = models.CharField(verbose_name='Your phone number', max_length=300)
    languages = models.ManyToManyField('Language', verbose_name='Languages Spoken')
    capacities = models.ManyToManyField('Capacity', verbose_name='Capacities')
    campaigns = models.ManyToManyField('Campaign', verbose_name="Active intake campaigns")
    notes = models.TextField(help_text="Additional notes", null=True, blank=True)

    def to_card(self):
        gc = GenericCard()
        gc.body.title = self.name if self.name else None
        gc.body.subtitle = self.username if self.username else None
        gc.body.text = self.notes if self.notes else None
        gc.body.card_link = ('mailto:' + self.email, self.email) if self.email else None
        gc.footer.badge_groups = (('primary', self.languages.all()), ('secondary', self.capacities.all()))
        return str(gc)

    def organizations(self):
        'Return a QuerySet of Organizations the user has access to'
        return Organization.objects.filter(
            id__in=[x.organization.id for x in self.campaigns.all() if x.campaign.date_expired > timezone.now()]
        )

    def locations(self, org):
        'Return a QuerySet of Locations the user has access to for given org'
        return Location.objects.filter(
            id__in=[str(x.id) for x in org.locations.all()]
        )

    def intakebuses(self, loc):
        'Return a QuerySet of IntakeBuses the user has access to for given loc'
        return IntakeBus.objects.filter(
            id__in=[str(x.id) for x in loc.intakebuses.all()]
        )

    def families(self, ib):
        'Return a QuerySet of Families the user has access to for given ib'
        return Family.objects.filter(
            id__in=[str(x.id) for x in ib.families.all()]
        )

    def travelplans(self, fam):
        'Return the TravelPlan the user has access to for given fam'
        return fam.travelplan

    def sponsor(self, fam):
        'Return the Sponsor the user has access to for given fam'
        return fam.sponsor

    def asylees(self, fam):
        'Return a QuerySet of Asylees the user has access to for given fam'
        return fam.asylees.all()

    def medicals(self, asylee):
        'Return a QuerySet of Medicals the user has access to for given asylee'
        return asylee.medical.all()

    def __str__(self):
        return '%(name)s (%(username)s)\nCapable of %(capacities)s\nSpeaks %(languages)s' % {
            'name': self.name,
            'username': self.username,
            'capacities': ', '.join(map(str, self.capacities.all())),
            'languages': ', '.join(map(str, self.languages.all()))
        }

class Campaign(models.Model):
    id = HashidAutoField(primary_key=True)
    campaign = models.OneToOneField('shortener.UrlMap', verbose_name="Active intake campaigns", on_delete=models.SET_NULL, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True)

    @property
    def url(self):
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
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.CharField(verbose_name="Team lead area", max_length=100, choices=CAPACITY_CHOICES, default='other')
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username

class SiteCoordinator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)

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

    def breadcrumbs(self, bc=''):
        model = self.name
        if bc != '':
            return """<li class="breadcrumb-item"><a href="/organization/%(id)s/detail">%(model)s</a></li>""" % {
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
    # site_coordinator = models.OneToOneField('SiteCoordinator', on_delete=models.CASCADE, null=True)
    site_coordinator = models.ForeignKey('SiteCoordinator', on_delete=models.CASCADE, null=True)
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)

class Location(models.Model):
    id = HashidAutoField(primary_key=True)
    intakebuses = models.ManyToManyField('IntakeBus', verbose_name='Intake Buses')
    lodging_type = models.CharField(verbose_name="Type of lodging provided", max_length=100, choices=LODGING_CHOICES, default='other')
    name = models.CharField(verbose_name="Name of the staging location", max_length=300)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def organization(self):
        return self.organization_set.first()

    def breadcrumbs(self, bc=''):
        parent = self.organization
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/location/%(id)s/detail">%(model)s</a></li>""" % {
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
    families = models.ManyToManyField('Family', verbose_name='Families')
    origin = models.CharField(max_length=300, verbose_name='City of origin of the bus')
    state = models.CharField(verbose_name="State of origin of the bus", max_length=100, choices=STATE_CHOICES, default='other')
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
    def destination(self):
        return self.location_set.first().organization_set.first().location

    def breadcrumbs(self, bc=''):
        parent = self.location
        model = self.number
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/intakebus/%(id)s/detail">%(model)s</a></li>""" % {
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

class Family(models.Model):
    id = HashidAutoField(primary_key=True)
    family_name = models.CharField(max_length=300, verbose_name='Shared family name', unique=True)
    languages = models.ManyToManyField('Language', verbose_name='Languages Spoken')
    intake_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    asylees = models.ManyToManyField('Asylee', verbose_name='Asylees')
    sponsor = models.OneToOneField('Sponsor', verbose_name='Sponsors', on_delete=models.SET_NULL, null=True)
    travel_plan = models.OneToOneField('TravelPlan', verbose_name='Travel Plans', on_delete=models.SET_NULL, null=True)
    lodging = models.CharField(verbose_name="Lodging", max_length=300, null=True)
    destination_city = models.CharField(verbose_name="Destination city", max_length=300, null=True)
    state = models.CharField(verbose_name="Destination state", max_length=100, choices=STATE_CHOICES, default='other')
    days_traveling = models.PositiveSmallIntegerField(verbose_name="Days spent traveling", default=0)
    days_detained = models.PositiveSmallIntegerField(verbose_name="Days spent in detention", default=0)
    country_of_origin = models.CharField(verbose_name="Country of origin", max_length=100, choices=COUNTRY_CHOICES, default='guatemala')
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def intakebus(self):
        return self.intakebus_set.first()

    @property
    def destination(self):
        return '%(city)s, %(st_abbr)s' % {
            'city': self.destination_city,
            'st_abbr': self.state.upper()
        }

    def breadcrumbs(self, bc=''):
        parent = self.intakebus
        model = self.family_name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/family/%(id)s/detail">%(model)s</a></li>""" % {
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
        return '%(name)s' % {
            'name': self.family_name
        }

class Asylee(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name="Asylee's name")
    medicals = models.ManyToManyField('Medical', verbose_name='Medical Issues')
    sex = models.CharField(verbose_name="Sex of asylee", max_length=100, choices=SEX_CHOICES, default='other')
    date_of_birth = models.DateField(help_text="YYYY-MM-DD", verbose_name="Asylee's date of birth")
    phone_number = models.CharField(verbose_name="Asylee's phone number", max_length=300, null=True)
    tsa_done = models.BooleanField(verbose_name="TSA paperwork done?", default=True)
    legal_done = models.BooleanField(verbose_name="Legal paperwork done?", default=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def family(self):
        return self.family_set.first()

    @property
    def age(self):
        return (timezone.now().date() - self.date_of_birth).days//365

    def breadcrumbs(self, bc=''):
        parent = self.family
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/asylee/%(id)s/detail">%(model)s</a></li>""" % {
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

class Sponsor(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name="Sponsor's name", unique=True)
    phone_number = models.CharField(verbose_name="Sponsor's phone #", max_length=300, null=True)
    address = models.CharField(verbose_name="Sponsor's address", max_length=300, null=True)
    city = models.CharField(verbose_name="Sponsor's city", max_length=300, null=True)
    state = models.CharField(verbose_name="Sponsor's state", max_length=100, choices=STATE_CHOICES, default='other')
    relation = models.CharField(max_length=300, verbose_name="Relation to family", null=True)
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
        parent = self.family
        model = self.name
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/sponsor/%(id)s/detail">%(model)s</a></li>""" % {
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
    arranged_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    confirmation = models.CharField(verbose_name="Confirmation #", max_length=100, null=True)
    destination_city = models.CharField(verbose_name="Destination city", max_length=100, null=True)
    destination_state = models.CharField(verbose_name="Destination state", max_length=100, choices=STATE_CHOICES, default='other')
    travel_date = models.DateTimeField(verbose_name="Departure time of travel", null=True)
    city_van_date = models.DateTimeField(verbose_name="Departure time on City Van", null=True)
    travel_food_prepared = models.BooleanField(verbose_name="Is travel food prepared?", default=False)
    eta = models.DateTimeField(verbose_name="Estimated time of arrival", null=True)
    travel_mode = models.CharField(verbose_name="Mode of travel", max_length=100, choices=TRAVEL_MODE_CHOICES, default='other')
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def destination(self):
        return '%(city)s, %(st_abbr)s' % {
            'city': self.destination_city,
            'st_abbr': self.destination_state.upper()
        }

    def breadcrumbs(self, bc=''):
        parent = self.family
        model = 'Travel Plan'
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/travelplan/%(id)s/detail">%(model)s</a></li>""" % {
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
        return 'Travel Plan for %(fam_name)s: %(travel_company)s Conf #%(conf)s' % {
            'fam_name': self.family.name,
            'travel_company': self.travel_mode,
            'conf': self.confirmation,
        }

class Medical(models.Model):
    id = HashidAutoField(primary_key=True)
    provider = models.ForeignKey('User', on_delete=models.CASCADE)
    issue_time = models.DateTimeField(verbose_name="Time the issue arose", auto_now_add=True)
    resolution_time = models.DateTimeField(verbose_name="Time the issue was resolved", editable=True, null=True)
    description = models.TextField(verbose_name="Description of issue", null=True, blank=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def asylee(self):
        return self.asylee_set.first()

    def breadcrumbs(self, bc=''):
        parent = self.asylee
        model = 'Medical'
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/medical/%(id)s/detail">%(model)s</a></li>""" % {
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
