from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from hashid_field import HashidAutoField, HashidField
from intake.choices import *
from intake.generic_card import GenericCard
from shortener import shortener
from shortener.models import UrlMap

import hashlib
from datetime import timedelta
from socket import gethostbyname, gethostname

# Create your models here.
# class Capacity(models.Model):
#     name = models.CharField(verbose_name="Capacity", max_length=500, unique=True)
#     notes = models.TextField(verbose_name="Description of capacity", null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Capacity'
#         verbose_name_plural = 'Capacities'
#
#     def __str__(self):
#         return '%(name)s' % {'name': self.name}

class User(AbstractUser):
    is_team_lead = models.BooleanField(default=False)
    is_point_of_contact = models.BooleanField(default=False)
    name = models.CharField(verbose_name='Your name', max_length=300)
    email = models.EmailField(verbose_name='Your email', max_length=300, null=True)
    phone_number = models.CharField(verbose_name='Your phone number', max_length=300)
    # languages = models.ManyToManyField('Language', verbose_name='Languages spoken')
    languages = ArrayField(
        models.CharField(verbose_name="Languages spoken", max_length=100, choices=LANGUAGE_CHOICES, default='english'),
        null=True
    )
    # capacities = models.ManyToManyField('Capacity', verbose_name='Your capacities')
    capacities = ArrayField(
        models.CharField(verbose_name="Capacities", max_length=100, choices=CAPACITY_CHOICES, default='other'),
        null=True
    )
    # affiliations = models.ManyToManyField('Organization', verbose_name='Affiliated organizations')
    campaigns = models.ManyToManyField('Campaign', verbose_name="Active intake campaigns")
    notes = models.TextField(help_text="Additional notes", null=True, blank=True)

    def to_card(self):
        gc = GenericCard()
        gc.body.title = self.name if self.name else None
        gc.body.subtitle = self.username if self.username else None
        gc.body.text = self.notes if self.notes else None
        gc.body.card_link = ('mailto:' + self.email, self.email) if self.email else None
        gc.footer.badge_groups = (('primary', self.languages), ('secondary', self.capacities))
        return str(gc)

    def __str__(self):
        return '%(name)s (%(username)s)\nCapable of %(capacities)s\nSpeaks %(languages)s' % {
            'name': self.name,
            'username': self.username,
            'capacities': ', '.join(self.capacities) if self.capacities else '',
            'languages': ', '.join(self.languages) if self.languages else ''
        }

class Campaign(models.Model):
    id = HashidAutoField(primary_key=True)
    # campaign = models.ForeignKey('shortener.UrlMap', verbose_name="Active intake campaigns", on_delete=models.CASCADE, null=True)
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
    # specialty = models.OneToOneField('Capacity', verbose_name='Team lead area', on_delete=models.SET_NULL, related_name='capacity', null=True)
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)
    # organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)
    # quizzes = models.ManyToManyField(Quiz, through='TakenQuiz')
    # interests = models.ManyToManyField(Subject, related_name='interested_students')
    #
    # def get_unanswered_questions(self, quiz):
    #     answered_questions = self.quiz_answers \
    #         .filter(answer__question__quiz=quiz) \
    #         .values_list('answer__question__pk', flat=True)
    #     questions = quiz.questions.exclude(pk__in=answered_questions).order_by('text')
    #     return questions

    def __str__(self):
        return self.user.username

class PointOfContact(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)
    # organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)

    def to_card(self):
        return self.user.to_card()

    def __str__(self):
        return '%(name)s [POC]' % {'name': self.user.name}

class Organization(models.Model):
    id = HashidAutoField(primary_key=True)
    is_valid = models.BooleanField(default=False)
    name = models.CharField(verbose_name='Name of the organization', max_length=500, unique=True)
    city = models.CharField(verbose_name='City', max_length=500, null=True)
    state = models.CharField(verbose_name="State", max_length=100, choices=STATE_CHOICES, default='nm')
    # state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="State", null=True)
    url = models.CharField(verbose_name='Website', max_length=500, null=True)
    locations = models.ManyToManyField('Location', verbose_name='Locations')
    # point_of_contact = models.ForeignKey('Volunteer', models.DO_NOTHING, verbose_name="Point of contact", related_name="pointofcontact", null=True)
    # deputies = models.ManyToManyField('Volunteer', verbose_name="Deputized volunteers", related_name="deputies")
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
            return """<li class="breadcrumb-item"><a href="/organization/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append("""<li class="breadcrumb-item">%(model)s</li>""" % {
                'model': model
            })
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

    def test(self, msg=''):
        return 'Org' + msg

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
            'org_state': self.state,
        }

# class TeamLead(models.Model):
#     lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='team_lead')
    # organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='team_lead')
    # quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='team_lead')
    # score = models.FloatField()
    # date = models.DateTimeField(auto_now_add=True)

# class Language(models.Model):
#     language = models.CharField(verbose_name="Language", max_length=500, unique=True)
#
#     class Meta:
#         verbose_name = 'Language'
#         verbose_name_plural = 'Languages'
#
#     def __str__(self):
#         return '%(language)s' % {'language': self.language}
#
# class State(models.Model):
#     name = models.CharField(verbose_name="State", max_length=50)
#     abbreviation = models.CharField(verbose_name="State abbreviation", max_length=5, unique=True)
#
#     class Meta:
#         verbose_name = 'State'
#         verbose_name_plural = 'States'
#
#     def __str__(self):
#         return '%(state)s' % {'state': self.name}
#
# class CountryOfOrigin(models.Model):
#     country = models.CharField(max_length=300, primary_key=True)
#
#     def __str__(self):
#         return '%(country)s' % {'country': self.country}
#
# class Sex(models.Model):
#     sex = models.CharField(max_length=6, primary_key=True)
#
#     def __str__(self):
#         return '%(sex)s' % {'sex': self.sex}

# class LodgingType(models.Model):
#     lodging_type = models.CharField(verbose_name="Type of lodging", max_length=50, unique=True)
#     notes = models.TextField(verbose_name="Description", null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Lodging'
#         verbose_name_plural = 'Lodging'
#
#     def __str__(self):
#         return '%(lodging_type)s' % {'lodging_type': self.lodging_type}

class RequestQueue(models.Model):
    point_of_contact = models.OneToOneField('PointOfContact', on_delete=models.CASCADE, null=True)
    organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)

class Location(models.Model):
    id = HashidAutoField(primary_key=True)
    # organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)
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
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/location/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

    def test(self, msg=''):
        return self.organization.test('Loc' + msg)

    # def __str__(self):
    #     return '%(name)s (%(org)s)' % {
    #         'name': self.name,
    #         'org': Organization.objects.filter(loca),
    #     }

    def __str__(self):
        return '%(name)s' % {
            'name': self.name,
        }

class IntakeBus(models.Model):
    id = HashidAutoField(primary_key=True)
    # destination = models.OneToOneField('Location', on_delete=models.CASCADE, null=True)
    families = models.ManyToManyField('Family', verbose_name='Families')
    origin = models.CharField(max_length=300, verbose_name='City of origin of the bus')
    state = models.CharField(verbose_name="State of origin of the bus", max_length=100, choices=STATE_CHOICES, default='other')
    # state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="Originating state", null=True)
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

    def breadcrumbs(self, bc=''):
        parent = self.location
        model = self.number
        if bc != '':
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/intakebus/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

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
    # languages = models.ManyToManyField('Language', verbose_name='Languages spoken')
    languages = ArrayField(
        models.CharField(verbose_name="Languages spoken", max_length=100, choices=LANGUAGE_CHOICES, default='spanish')
    )
    intake_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    # intake_bus = models.ForeignKey('IntakeBus', on_delete=models.SET_NULL, null=True)
    asylees = models.ManyToManyField('Asylee', verbose_name='Asylees')
    sponsor = models.OneToOneField('Sponsor', verbose_name='Sponsors', on_delete=models.SET_NULL, null=True)
    travel_plan = models.OneToOneField('TravelPlan', verbose_name='Travel Plans', on_delete=models.SET_NULL, null=True)
    lodging = models.CharField(verbose_name="Lodging", max_length=300, null=True)
    destination_city = models.CharField(verbose_name="Destination city", max_length=300, null=True)
    state = models.CharField(verbose_name="Destination state", max_length=100, choices=STATE_CHOICES, default='other')
    # state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="Destination state", null=True)
    days_traveling = models.PositiveSmallIntegerField(verbose_name="Days spent traveling", default=0)
    days_detained = models.PositiveSmallIntegerField(verbose_name="Days spent in detention", default=0)
    country_of_origin = models.CharField(verbose_name="Country of origin", max_length=100, choices=COUNTRY_CHOICES, default='guatemala')
    # country_of_origin = models.ForeignKey('CountryOfOrigin', on_delete=models.SET_NULL, null=True)
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
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/family/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

    def __str__(self):
        return '%(name)s' % {
            'name': self.family_name
        }

class Asylee(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name="Asylee's name")
    # family = models.ForeignKey('Family', on_delete=models.SET_NULL, null=True)
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
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/asylee/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

class Sponsor(models.Model):
    id = HashidAutoField(primary_key=True)
    name = models.CharField(max_length=300, verbose_name="Sponsor's name", unique=True)
    phone_number = models.CharField(verbose_name="Sponsor's phone #", max_length=300, null=True)
    address = models.CharField(verbose_name="Sponsor's address", max_length=300, null=True)
    city = models.CharField(verbose_name="Sponsor's city", max_length=300, null=True)
    state = models.CharField(verbose_name="Sponsor's state", max_length=100, choices=STATE_CHOICES, default='other')
    # state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="Sponsor's state", null=True)
    # family = models.OneToOneField('Family', on_delete=models.SET_NULL, null=True)
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
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/sponsor/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

class TravelPlan(models.Model):
    id = HashidAutoField(primary_key=True)
    arranged_by = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    confirmation = models.CharField(verbose_name="Confirmation #", max_length=100, null=True)
    destination_city = models.CharField(verbose_name="Destination city", max_length=100, null=True)
    destination_state = models.CharField(verbose_name="Destination state", max_length=100, choices=STATE_CHOICES, default='other')
    # destination_state = models.state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="Destination state", null=True)
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
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/travelplan/%(id)s">%(model)s</a></li>""" % {
                'model': model
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

class Medical(models.Model):
    id = HashidAutoField(primary_key=True)
    # patient = models.OneToOneField('Asylee', on_delete=models.CASCADE)
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
            return parent.breadcrumbs("""<li class="breadcrumb-item"><a href="/medical/%(id)s">%(model)s</a></li>""" % {
                'model': model, 'id': self.id
            } + bc)
        if bc == '':
            bc = []
            bc.append('<nav aria-label="breadcrumb">')
            bc.append('<ol class="breadcrumb">')
            bc.append(parent.breadcrumbs('<li class="breadcrumb-item active" aria-current="page">%(model)s</li>' % {
                'model': model
            }))
            bc.append('</ol>')
            bc.append('</nav>')
        return ''.join(bc)

# class Token(models.Model):
#     shorthash = models.CharField(max_length=20, null=True)
#     creation_date = models.DateTimeField(auto_now_add=True, editable=False)
#     expiration_date = models.DateTimeField(null=True)
#     max_uses = models.SmallIntegerField(null=True)
#     reference_id = models.SmallIntegerField(null=True)
#     notes = models.TextField(help_text="Additional notes", null=True, blank=True)
#
#     def decrement(self):
#         if self.max_uses:
#             self.max_uses -= 1
#             self.save()
#
#     @property
#     def is_expired(self):
#         if self.max_uses:
#             return self.max_uses <= 0
#         if self.expiration_date:
#             return timezone.now() >= self.expiration_date
#         return None
#
#     @property
#     def hash(self):
#         if not self.shorthash:
#             hash = hashlib.sha256((str(self.id) + str(self.creation_date)).encode('utf-8')).hexdigest()[:6]
#             self.shorthash = hash
#             self.save()
#             return hash
#         return self.shorthash
#
#     def __str__(self):
#         return 'Token %(hash)s' % {'hash': self.hash}
#
# @receiver(post_save, sender=Token)
# def save_token(sender, instance, **kwargs):
#     if instance.max_uses is not None:
#         if instance.max_uses < 1:
#             instance.delete()
#     if instance.expiration_date is not None:
#         if timezone.now() >= instance.expiration_date:
#             instance.delete()
#
# class Location(models.Model):
#     organization = models.OneToOneField('Organizations', on_delete=models.CASCADE, null=True)
#     name = models.CharField(help_text="Name of the refugee staging location", max_length=300)
#     notes = models.TextField(help_text="Additional notes", null=True, blank=True)
#
#     def __str__(self):
#         return '%(name)s (%(org)s)' % {
#             'name': self.name,
#             'org': self.organization,
#         }

# class IntakeBuses(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     arrival_time = models.DateTimeField(
#         help_text="Bus' time of arrival at staging location",
#         blank=True,
#         null=True
#     )
#     destination = models.ForeignKey(Location, help_text="Where the bus dropped off asylees", on_delete=models.DO_NOTHING, null=True)
#     number = models.CharField(help_text="Identifying number for bus", max_length=300, null=True)
#     origin = models.CharField(help_text="Where the bus came from", max_length=100)   #TK: Necessary?
#     notes = models.TextField(null=True, blank=True)
#
#     def __str__(self):
#         return 'Bus %(number)s arrived on %(arrived)s from %(origin)s' % {
#             'number': self.number,
#             'arrived': self.arrival_time.strftime("%b %d, '%y %H:%M"),
#             'origin': self.origin,
#         }
#
# class Lodging(models.Model):
#     LODGING_CHOICES = [
#         ('hotel', 'Hotel/Motel Room'),
#         ('dorm', 'Dormitory Room'),
#         ('other', 'Other'),
#     ]
#     id = models.BigAutoField(primary_key=True)
#     lodging_type = models.CharField(
#         help_text="What type of lodging",
#         max_length=2,
#         choices=LODGING_CHOICES,
#         default='dorm',
#     )
#     description = models.CharField(help_text="Description of lodging", max_length=200)
#
# class TravelPlans(models.Model):
#     STATE_CHOICES = [
#         ('al', 'Alabama'),
#         ('ak', 'Alaska'),
#         ('az', 'Arizona'),
#         ('ar', 'Arkansas'),
#         ('ca', 'California'),
#         ('co', 'Colorado'),
#         ('ct', 'Connecticut'),
#         ('de', 'Delaware'),
#         ('dc', 'District of Columbia'),
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
#     ]
#     TRAVEL_TYPE_CHOICES = [
#         ('Air', (
#                 ('alaska', 'Alaska (AS)'),
#                 ('american', 'American (AA)'),
#                 ('delta', 'Delta (DL)'),
#                 ('frontier', 'Frontier (F9)'),
#                 ('jetblue', 'Jet Blue (B6)'),
#                 ('southwest', 'Southwest (WN)'),
#                 ('united', 'United (UA)'),
#                 ('other', 'Other'),
#             )
#         ),
#         ('Bus', (
#                 ('greyhound', 'Greyhound'),
#                 ('other', 'Other'),
#             )
#         ),
#         ('Train', (
#                 ('amtrak', 'Amtrak'),
#                 ('other', 'Other'),
#             )
#         ),
#         ('other', 'Other'),
#     ]
#     id = models.BigAutoField(primary_key=True)
#     arranged_by = models.ForeignKey(
#         Volunteer,
#         help_text="Volunteer who arranged travel plans",
#         verbose_name="Travel arranged by (volunteer)",
#         on_delete=models.DO_NOTHING
#     )
#     confirmation = models.CharField(help_text="Confirmation details", max_length=200)
#     destination_city = models.CharField(max_length=200)
#     destination_state = models.CharField(
#         max_length=2,
#         choices=STATE_CHOICES,
#         default='other',
#     )
#     travel_date = models.DateTimeField(
#         "Date of travel plans",
#         blank=True,
#         null=True
#     )
#     city_van_date = models.DateTimeField(
#         "Time of local transport",
#         blank=True,
#         null=True
#     )
#     travel_food_prepared = models.BooleanField(default=False)
#     travel_duration = models.DecimalField(
#         "Duration of travel (hours)",
#         max_digits=4,
#         decimal_places=2
#     )
#     travel_mode = models.CharField(
#         "Mode of travel",
#         max_length=2,
#         choices=TRAVEL_TYPE_CHOICES,
#         default='other',
#     )
#     notes = models.TextField(null=True, blank=True)
#
# class Sponsors(models.Model):
#     STATE_CHOICES = [
#         ('al', 'Alabama'),
#         ('ak', 'Alaska'),
#         ('az', 'Arizona'),
#         ('ar', 'Arkansas'),
#         ('ca', 'California'),
#         ('co', 'Colorado'),
#         ('ct', 'Connecticut'),
#         ('de', 'Delaware'),
#         ('dc', 'District of Columbia'),
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
#     ]
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField("sponsor's name", max_length=300)
#     phone_number = models.CharField("sponsor's phone number", max_length=300)
#     city = models.CharField("sponsor's city", max_length=300)
#     state = models.CharField(
#         "sponsor's state",
#         max_length=2,
#         choices=STATE_CHOICES,
#         default='other'
#     )
#     relation = models.CharField("Sponsor's relation to asylee", max_length=300)
#     address = models.TextField("Sponsor's street address")    #TK: Necessary?
#     notes = models.TextField(null=True, blank=True)
#
# class Families(models.Model):
#     LANGUAGE_CHOICES = [
#         ('Latin', (
#                 ('portuguese', 'Brazilian/Portuguese'),
#                 ('spanish', 'Spanish'),
#             )
#         ),
#         ('Maya', (
#                 ('achi', 'Achi'),
#                 ('awakatek', 'Awakatek'),
#                 ('chorti', "Ch\'orti\'"),
#                 ('chuj', 'Chuj'),
#                 ('itza', "Itza\'"),
#                 ('ixil', 'Ixil'),
#                 ('jakaltek', 'Jakaltek'),
#                 ('kiche', "K\'iche\'"),
#                 ('kaqchiquel', 'Kaqchiquel'),
#                 ('mam', 'Mam'),
#                 ('mopan', 'Mopan'),
#                 ('poqomam', 'Poqomam'),
#                 ('poqomchi', "Poqomchi\'"),
#                 ('qanjobal', 'Q\'anjob\'al'),
#                 ('qeqchi', 'Q\'eqchi\''),
#                 ('sakapultek', 'Sakapultek'),
#                 ('sipakapense', 'Sipakapense'),
#                 ('tektitek', 'Tektitek'),
#                 ('tzutujil', 'Tz\'utujil'),
#                 ('upsantek', 'Upsantek'),
#                 ('other', 'Other'),
#             )
#         ),
#         ('other', 'Other'),
#     ]
#     id = models.BigAutoField(primary_key=True)
#     family_name = models.CharField(
#         "name of family unit",
#         max_length=500
#     )
#     taken_in_by = models.ForeignKey(
#         Volunteer,
#         verbose_name="intake by (volunteer)",
#         on_delete=models.DO_NOTHING
#     )
#     lodging = models.ForeignKey(
#         Lodging,
#         on_delete=models.DO_NOTHING
#     )
#     destination = models.CharField(max_length=300)
#     language_spoken = models.CharField(
#         max_length=2,
#         choices=LANGUAGE_CHOICES,
#         default='spanish',
#     )
#     intake_bus = models.ForeignKey(IntakeBuses, on_delete=models.DO_NOTHING, null=True)  #TK: FK or M2M?
#     sponsor = models.ForeignKey(Sponsors, on_delete=models.DO_NOTHING)
#     travel = models.ForeignKey(
#         TravelPlans,
#         on_delete=models.DO_NOTHING
#     )
#     travel_permission_date = models.DateTimeField(
#         "okayed to travel",
#         blank=True,
#         null=True,
#     )
#     days_detained = models.IntegerField(null=True)
#     days_traveling = models.IntegerField(null=True)
#     notes = models.TextField(null=True, blank=True)
#
# class Asylees(models.Model):
#     COUNTRY_OF_ORIGIN_CHOICES = [
#         ('Most Common', (
#                 ('brazil', 'Brazil'),
#                 ('el salvador', 'El Salvador'),
#                 ('guatemala', 'Guatemala'),
#                 ('honduras', 'Honduras'),
#             )
#         ),
#         ('Less Common', (
#                 ('belize', 'Belize'),
#                 ('bolivia', 'Bolivia'),
#                 ('colombia', 'Colombia'),
#                 ('ecuador', 'Ecuador'),
#                 ('haiti', 'Haiti'),
#                 ('jamaica', 'Jamaica'),
#                 ('mexico', 'Mexico'),
#                 ('nicaragua', 'Nicaragua'),
#                 ('panama', 'Panama'),
#                 ('peru', 'Peru'),
#                 ('venezuela', 'Venezuela'),
#             )
#         ),
#         ('other', 'Other'),
#     ]
#     SEX_CHOICES = [
#         ('female', 'Female'),
#         ('male', 'Male'),
#     ]
#     id = models.BigAutoField(primary_key=True)
#     first_name = models.CharField("Asylee's first name", max_length=300)
#     last_name = models.CharField("Asylee's last name", max_length=300)
#     sex = models.CharField(
#         "Asylee's sex",
#         max_length=2,
#         choices=SEX_CHOICES,
#         default='Female'
#     )
#     date_of_birth = models.DateField("Asylee's date of birth (mdy?)")   #TK: check date format to match input format
#     country_of_origin = models.CharField(
#         "Asylee's country of origin",
#         max_length=2,
#         choices=COUNTRY_OF_ORIGIN_CHOICES,
#         default='guatemala'
#     )
#     family = models.ForeignKey(Families, on_delete=models.DO_NOTHING) #TK: FK or M2M?
#     phone_number = models.CharField("sponsor's phone number", max_length=300)
#     intake_volunteer = models.ForeignKey(Volunteer, on_delete=models.DO_NOTHING)   #TK: FK or M2M?
#     tsa_done = models.BooleanField("Is TSA done?", default=False)   #TK: Necessary?
#     legal_done = models.BooleanField("Is legal done?", default=False) #TK: Necessary?
#     notes = models.TextField(null=True, blank=True)
#
# class Medical(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     patient = models.ForeignKey(
#         Asylees,
#         verbose_name="asylee patient",
#         on_delete=models.DO_NOTHING
#     )
#     provider = models.ForeignKey(
#         Volunteer,
#         verbose_name="medical provider",
#         on_delete=models.DO_NOTHING
#     )
#     issue_time = models.DateTimeField(
#         "time of occurence",
#         blank=True,
#         auto_now_add=True
#     )
#     resolution_time = models.DateTimeField(
#         "time the issue was resolved",
#         blank=True,
#         null=True
#     )
#     description = models.TextField()
#     notes = models.TextField(null=True, blank=True)

# class NewOrganization(models.Model):
#     is_valid = models.BooleanField(default=False)
#     name = models.CharField(verbose_name='Name of the organization', max_length=500, unique=True)
#     city = models.CharField(verbose_name='City', max_length=500, null=True)
#     state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="State", null=True)
#     url = models.CharField(verbose_name='Website', max_length=500, null=True)
#     locations = models.ManyToManyField('NewLocation', verbose_name='Locations')
#     # point_of_contact = models.ForeignKey('Volunteer', models.DO_NOTHING, verbose_name="Point of contact", related_name="pointofcontact", null=True)
#     # deputies = models.ManyToManyField('Volunteer', verbose_name="Deputized volunteers", related_name="deputies")
#     notes = models.TextField(verbose_name='Additional notes', null=True, blank=True)
#
#     @property
#     def location(self):
#         return '%(city)s, %(state)s' % {
#             'city': self.city,
#             'state': self.state.upper(),
#         }
#
#     class Meta:
#         verbose_name = 'Organization'
#         verbose_name_plural = 'Organizations'
#
#     def __str__(self):
#         return '%(org_name)s (%(org_city)s, %(org_state)s)' % {
#             'org_name': self.name,
#             'org_city': self.city,
#             'org_state': self.state,
#         }
#
# class NewLocation(models.Model):
#     # organization = models.OneToOneField('Organization', on_delete=models.CASCADE, null=True)
#     # organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True)
#     name = models.CharField(verbose_name="Name of the staging location", max_length=300)
#     notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
#
#     @property
#     def organization(self):
#         return NewOrganization.objects.filter(locations__in=[self.id]).first()
#
#     def __str__(self):
#         return '%(name)s (%(org)s)' % {
#             'name': self.name,
#             'org': self.organization,
#         }
