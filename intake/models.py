from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from intake.generic_card import GenericCard
from shortener import shortener
from shortener.models import UrlMap

# Create your models here.
class Volunteer(AbstractUser):
    is_lead = models.BooleanField(default=False)
    is_point_of_contact = models.BooleanField(default=False)
    # name = models.CharField(verbose_name="Volunteer's name", max_length=300)
    # email = models.EmailField(verbose_name="Volunteer's email", max_length=300, null=True)
    # phone_number = models.CharField(verbose_name="Volunteer's phone number", max_length=300)
    # languages = models.ManyToManyField('Language', verbose_name="Languages spoken")
    # capacities = models.ManyToManyField('Capacity', verbose_name="Volunteer capacities", related_name="volunteer_capacities")
    # affiliations = models.ManyToManyField('Organization', verbose_name="Organizations to which the volunteer is affiliated")
    # campaigns = models.ManyToManyField('shortener.UrlMap', verbose_name="Active intake campaigns")
    # notes = models.TextField(help_text="Additional notes", null=True, blank=True)
    #
    # def to_card(self):
    #     gc = GenericCard()
    #     gc.body.title = self.name if self.name else None
    #     gc.body.subtitle = self.user.username if self.user.username else None
    #     gc.body.text = self.notes if self.notes else None
    #     gc.body.card_link = ('mailto:' + self.email, self.email) if self.email else None
    #     gc.footer.badge_groups = (('primary', self.language.all()), ('secondary', self.capacity.all()))
    #     return str(gc)
    #
    # class Meta:
    #     verbose_name = 'Volunteer'
    #     verbose_name_plural = 'Volunteers'
    #
    # def __str__(self):
    #     return '%(name)s [%(langs)s] [%(caps)s]' % {
    #         'name': self.name if self.name else self.user.username,
    #         'langs': ', '.join(map(str, self.language.all())) if self.language.exists() else 'unspecified',
    #         'caps': ', '.join(map(str, self.capacity.all())) if self.capacity.exists() else 'unspecified',
    #     }

class Lead(models.Model):
    volunteer = models.OneToOneField('Volunteer', on_delete=models.CASCADE, primary_key=True)
    capacity = models.OneToOneField('Capacity', verbose_name="Team", related_name="team_lead", on_delete=models.CASCADE, null=True)

    def __str__(self):
        return '%(capacity)s Lead' % {'capacity': self.capacity.capacity}

class Capacity(models.Model):
    name = models.CharField(verbose_name="Capacity", max_length=500, unique=True)
    notes = models.TextField(verbose_name="Description of capacity", null=True, blank=True)

    class Meta:
        verbose_name = 'Capacity'
        verbose_name_plural = 'Capacities'

    def __str__(self):
        return '%(name)s' % {'name': self.name}

class Language(models.Model):
    language = models.CharField(verbose_name="Language", max_length=500, unique=True)

    class Meta:
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return '%(language)s' % {'language': self.language}

class Organization(models.Model):
    name = models.CharField(verbose_name="Name of the organization", max_length=500, unique=True)
    city = models.CharField(verbose_name="City", max_length=500, null=True)
    state = models.ForeignKey('State', models.DO_NOTHING, verbose_name="State", null=True)
    url = models.CharField(verbose_name="Website", max_length=500, null=True)
    point_of_contact = models.ForeignKey('Volunteer', models.DO_NOTHING, verbose_name="Point of contact", related_name="point_of_contact", null=True)
    leads = models.ManyToManyField('Volunteer', through='Lead', related_name='leads')
    # deputies = models.ManyToManyField('User', verbose_name="Deputized volunteers", related_name="deputies")
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    @property
    def location(self):
        return '%(city)s, %(state)s' % {
            'city': self.city,
            'state': self.state.abbreviation.upper(),
        }

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

# class Lead(models.Model):
#     organization = models.ForeignKey('Organization', related_name='lead', on_delete=models.SET_NULL, null=True)
#     volunteer = models.ForeignKey('Volunteer', related_name='lead', on_delete=models.SET_NULL, null=True)
#     capacity = models.ForeignKey('Capacity', related_name='lead', on_delete=models.SET_NULL, null=True)

class State(models.Model):
    name = models.CharField(verbose_name="State", max_length=50)
    abbreviation = models.CharField(verbose_name="State abbreviation", max_length=5, unique=True)

    class Meta:
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return '%(state)s' % {'state': self.name}

class LodgingType(models.Model):
    lodging_type = models.CharField(verbose_name="Type of lodging", max_length=50, unique=True)
    notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)

    class Meta:
        verbose_name = 'Lodging'
        verbose_name_plural = 'Lodging'

    def __str__(self):
        return '%(lodging_type)s' % {'lodging_type': self.lodging_type}
