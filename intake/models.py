from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from intake.encryption import Encryption
from intake.generic_card import GenericCard
from shortener import shortener
from shortener.models import UrlMap

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe

class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

class Lead(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    specialty = models.OneToOneField('Capacity', on_delete=models.SET_NULL, related_name='team_lead', null=True)
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

class Capacity(models.Model):
    name = models.CharField(verbose_name="Capacity", max_length=500, unique=True)
    notes = models.TextField(verbose_name="Description of capacity", null=True, blank=True)

    class Meta:
        verbose_name = 'Capacity'
        verbose_name_plural = 'Capacities'

    def __str__(self):
        return '%(name)s' % {'name': self.name}

class TeamLead(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='team_lead')
    # organization = models.ForeignKey('Organization', on_delete=models.CASCADE, related_name='team_lead')
    # quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='team_lead')
    # score = models.FloatField()
    # date = models.DateTimeField(auto_now_add=True)

# class Languages(models.Model):
#     language = models.CharField(verbose_name="Language", max_length=500, unique=True)
#
#     class Meta:
#         verbose_name = 'Language'
#         verbose_name_plural = 'Languages'
#
#     def __str__(self):
#         return '%(language)s' % {'language': self.language}
#
# class LodgingTypes(models.Model):
#     lodging_type = models.CharField(verbose_name="State", max_length=50, unique=True)
#     notes = models.TextField(verbose_name="Description of capacity", null=True, blank=True)
#
#     class Meta:
#         verbose_name = 'Lodging'
#         verbose_name_plural = 'Lodging'
#
#     def __str__(self):
#         return '%(lodging_type)s' % {'lodging_type': self.lodging_type}
#
# class States(models.Model):
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
# class Organization(models.Model):
#     name = models.CharField(verbose_name="Name of the organization", max_length=500, unique=True)
#     city = models.CharField(verbose_name="City", max_length=500, null=True)
#     state = models.ForeignKey('States', models.DO_NOTHING, verbose_name="State", null=True)
#     url = models.CharField(verbose_name="Website", max_length=500, null=True)
#     point_of_contact = models.ForeignKey('Volunteer', models.DO_NOTHING, verbose_name="Point of contact", related_name="pointofcontact", null=True)
#     deputies = models.ManyToManyField('Volunteer', verbose_name="Deputized volunteers", related_name="deputies")
#     notes = models.TextField(verbose_name="Additional notes", null=True, blank=True)
#
#     @property
#     def location(self):
#         return '%(city)s, %(state)s' % {
#             'city': self.city,
#             'state': self.state.abbreviation.upper(),
#         }
#
#     def to_card(self):
#         gc = GenericCard()
#         gc.body.title = self.name if self.name else None
#         gc.body.subtitle = self.location if self.location else None
#         gc.body.text = self.notes if self.notes else None
#         gc.body.card_link = (self.url, self.url) if self.url else None
#         gc.footer.see_more = '/organization/%d' % self.id
#         return str(gc)
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
# class Volunteer(models.Model):
#     user = models.OneToOneField(User, help_text="", on_delete=models.CASCADE, null=True)
#     name = models.CharField(verbose_name="Volunteer's name", max_length=300)
#     email = models.EmailField(verbose_name="Volunteer's email", max_length=300, null=True)
#     phone_number = models.CharField(verbose_name="Volunteer's phone number", max_length=300)
#     languages = models.ManyToManyField('Languages', verbose_name="Languages spoken")
#     capacities = models.ManyToManyField('Capacities', verbose_name="Volunteer capacities")
#     affiliations = models.ManyToManyField('Organizations', verbose_name="Organizations to which the volunteer is affiliated")
#     campaigns = models.ManyToManyField('shortener.UrlMap', verbose_name="Active intake campaigns")
#     notes = models.TextField(help_text="Additional notes", null=True, blank=True)
#
#     def to_card(self):
#         gc = GenericCard()
#         gc.body.title = self.name if self.name else None
#         gc.body.subtitle = self.user.username if self.user.username else None
#         gc.body.text = self.notes if self.notes else None
#         gc.body.card_link = ('mailto:' + self.email, self.email) if self.email else None
#         gc.footer.badge_groups = (('primary', self.languages.all()), ('secondary', self.capacities.all()))
#         return str(gc)
#
#     class Meta:
#         verbose_name = 'Volunteer'
#         verbose_name_plural = 'Volunteers'
#
#     def __str__(self):
#         return '%(name)s [%(langs)s] [%(caps)s]' % {
#             'name': self.name if self.name else self.user.username,
#             'langs': ', '.join(map(str, self.languages.all())) if self.languages.exists() else 'unspecified',
#             'caps': ', '.join(map(str, self.capacities.all())) if self.capacities.exists() else 'unspecified',
#         }
#
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Volunteer.objects.create(user=instance)
#     instance.Volunteer.save()
#
# class Lead(models.Model):
#     volunteer = models.ForeignKey('Volunteer', related_name='leads', on_delete=models.SET_NULL, null=True)
#     capacity = models.ForeignKey('Capacity', related_name='leads', on_delete=models.SET_NULL, null=True)
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

# class Organizations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(help_text="Name of the organization", max_length=300)
#     location = models.CharField(help_text="City, State of the organization", max_length=300)
#     head_name = models.CharField(help_text="Head of organization's name", max_length=300, default='J Doe')
#     head_email = models.EmailField(help_text="Head of organization's email", max_length=300, default='hello@.com')
#     head_phone_number = models.CharField(help_text="Head of organization's phone number", max_length=300, default='505-867-5309')
#
#     def obscure_code(self):
#         enc = Encryption(self.name)
#         self.code = enc.encode(self.id)
#
#     def __str__(self):
#         return '%(org_name)s (%(org_loc)s)' % {
#             'org_name': self.name,
#             'org_loc': self.location,
#         }

# class VolunteerTypes(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     volunteer_type = models.CharField(max_length=300, unique=True)
#
#     def __str__(self):
#         return '%(vtype)s' % {'vtype': self.volunteer_type}

# class Volunteers(models.Model):
#     user = models.OneToOneField(User, help_text="", on_delete=models.CASCADE, null=True)
#     name = models.CharField(help_text="Volunteer's name", max_length=300)
#     email = models.EmailField(help_text="Volunteer's email", max_length=300, null=True)
#     phone_number = models.CharField(help_text="Volunteer's phone number", max_length=300)
#     volunteer_type = models.ManyToManyField(VolunteerTypes, help_text="Volunteer's capacities")
#     organizations = models.ManyToManyField(Organizations, help_text="Organizations to which the volunteer belongs")
#     notes = models.TextField(help_text="Additional notes", null=True, blank=True)
#
#     def __str__(self):
#         vol_type = ''
#         if self.volunteer_type.exists():
#             vol_type = '[%s]' % ', '.join(self.volunteer_type.values_list('volunteer_type',flat=True))
#         return '%(name)s %(volunteer_type)s' % {
#             'name': self.name,
#             'volunteer_type': vol_type,
#         }
#
# @receiver(post_save, sender=User)
# def update_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Volunteers.objects.create(user=instance)
#     instance.volunteers.save()

# class Locations(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField(help_text="Name of the refugee staging location", max_length=300)
#     notes = models.TextField(help_text="Additional notes", null=True, blank=True)
#
#     def __str__(self):
#         return '%(name)s' % {
#             'name': self.name,
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

# class Volunteers(models.Model):
#     # VOLUNTEER_CHOICES = [
#     #     (ACTIVITIES, 'Activities'),
#     #     (CHANGEOFADDRESS, 'Change of Address'),
#     #     (CLOTHES, 'Clothes'),
#     #     (DEPARTUREBAGS, 'Departure Bags'),
#     #     (FOOD, 'Food'),
#     #     (INTAKE, 'Intake'),
#     #     (MEDICAL, 'Medical'),
#     #     (TRAVEL, 'Travel'),
#     #     (TRANSPORT, 'Transport'),
#     #     (VOLCOORDINATOR, 'Volunteer Coordinator'),
#     #     (OTHER, 'Other'),
#     # ]
#     id = models.BigAutoField(primary_key=True)
#     name = models.CharField("volunteer's name", max_length=300)
#     email_address = models.CharField("volunteer's email", max_length=300)
#     phone_number = models.CharField("volunteer's phone number", max_length=300)
#     volunteer_type = models.ManyToManyField(VolunteerTypes)
#     notes = models.TextField(null=True, blank=True)
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
