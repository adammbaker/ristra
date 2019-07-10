# Generated by Django 2.2.3 on 2019-07-10 04:32

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_team_lead', models.BooleanField(default=False)),
                ('is_point_of_contact', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=300, verbose_name='Your name')),
                ('email', models.EmailField(max_length=300, null=True, verbose_name='Your email')),
                ('phone_number', models.CharField(max_length=300, verbose_name='Your phone number')),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Latin', (('english', 'English'), ('spanish', 'Spanish'), ('portuguese', 'Portuguese'), ('french', 'French'))), ('Maya', (('achi', 'Achi'), ('awakatek', 'Awakatek'), ('chorti', "Ch'orti'"), ('chuj', 'Chuj'), ('itza', "Itza'"), ('ixil', 'Ixil'), ('jakaltek', 'Jakaltek'), ('kiche', "K'iche'"), ('kaqchiquel', 'Kaqchiquel'), ('mam', 'Mam'), ('mopan', 'Mopan'), ('poqomam', 'Poqomam'), ('poqomchi', "Poqomchi'"), ('qanjobal', "Q'anjob'al"), ('qeqchi', "Q'eqchi'"), ('sakapultek', 'Sakapultek'), ('sipakapense', 'Sipakapense'), ('tektitek', 'Tektitek'), ('tzutujil', "Tz'utujil"), ('upsantek', 'Upsantek'))), ('other', 'Other')], default='spanish', max_length=100, verbose_name='Languages spoken'), size=None)),
                ('capacities', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('activities', 'Activities'), ('changeofaddress', 'Change of Address'), ('clothes', 'Clothes'), ('departurebags', 'Departure Bags'), ('food', 'Food'), ('intake', 'Intake'), ('medical', 'Medical'), ('travel', 'Travel'), ('transport', 'Transport'), ('volunteercoordinator', 'Volunteer Coordinator'), ('other', 'Other')], default='other', max_length=100, verbose_name='Capacities'), size=None)),
                ('notes', models.TextField(blank=True, help_text='Additional notes', null=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Asylee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name="Asylee's name")),
                ('sex', models.CharField(choices=[('female', 'Female'), ('male', 'Male'), ('other', 'Other')], default='other', max_length=100, verbose_name='Sex of asylee')),
                ('date_of_birth', models.DateField(help_text='YYYY-MM-DD', verbose_name="Asylee's date of birth")),
                ('phone_number', models.CharField(max_length=300, null=True, verbose_name="Asylee's phone number")),
                ('tsa_done', models.BooleanField(default=True, verbose_name='TSA paperwork done?')),
                ('legal_done', models.BooleanField(default=True, verbose_name='Legal paperwork done?')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
            ],
        ),
        migrations.CreateModel(
            name='Family',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('family_name', models.CharField(max_length=300, unique=True, verbose_name='Shared family name')),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Latin', (('english', 'English'), ('spanish', 'Spanish'), ('portuguese', 'Portuguese'), ('french', 'French'))), ('Maya', (('achi', 'Achi'), ('awakatek', 'Awakatek'), ('chorti', "Ch'orti'"), ('chuj', 'Chuj'), ('itza', "Itza'"), ('ixil', 'Ixil'), ('jakaltek', 'Jakaltek'), ('kiche', "K'iche'"), ('kaqchiquel', 'Kaqchiquel'), ('mam', 'Mam'), ('mopan', 'Mopan'), ('poqomam', 'Poqomam'), ('poqomchi', "Poqomchi'"), ('qanjobal', "Q'anjob'al"), ('qeqchi', "Q'eqchi'"), ('sakapultek', 'Sakapultek'), ('sipakapense', 'Sipakapense'), ('tektitek', 'Tektitek'), ('tzutujil', "Tz'utujil"), ('upsantek', 'Upsantek'))), ('other', 'Other')], default='spanish', max_length=100, verbose_name='Languages spoken'), size=None)),
                ('lodging', models.CharField(max_length=300, null=True, verbose_name='Lodging')),
                ('destination_city', models.CharField(max_length=300, null=True, verbose_name='Destination city')),
                ('state', models.CharField(choices=[('al', 'Alabama'), ('ak', 'Alaska'), ('az', 'Arizona'), ('ar', 'Arkansas'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'Washington D.C.'), ('fl', 'Florida'), ('ga', 'Georgia'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'), ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'), ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('va', 'Virginia'), ('wa', 'Washington State'), ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming'), ('other', 'Other')], default='other', max_length=100, verbose_name='Destination state')),
                ('days_traveling', models.PositiveSmallIntegerField(default=0, verbose_name='Days spent traveling')),
                ('days_detained', models.PositiveSmallIntegerField(default=0, verbose_name='Days spent in detention')),
                ('country_of_origin', models.CharField(choices=[('Central America and Caribbean', (('guatemala', 'Guatemala'), ('honduras', 'Honduras'), ('elsalvador', 'El Salvador'), ('mexico', 'Mexico'), ('argentina', 'Argentina'), ('bolivia', 'Bolivia'), ('brazil', 'Brazil'), ('chile', 'Chile'), ('colombia', 'Colombia'), ('costarica', 'Costa Rica'), ('cuba', 'Cuba'), ('dominicanrepublic', 'Dominican Republic'), ('ecuador', 'Ecuador'), ('frenchguiana', 'French Guiana'), ('guadeloupe', 'Guadeloupe'), ('haiti', 'Haiti'), ('martinique', 'Martinique'), ('mexico', 'Mexico'), ('nicaragua', 'Nicaragua'), ('panama', 'Panama'), ('paraguay', 'Paraguay'), ('peru', 'Peru'), ('saintmartin', 'Saint Martin'), ('uruguay', 'Uruguay'), ('venezuela', 'Venezuela'))), ('Africa', (('algeria', 'Algeria'), ('angola', 'Angola'), ('benin', 'Benin'), ('botswana', 'Botswana'), ('burkinafaso', 'Burkina Faso'), ('burundi', 'Burundi'), ('cameroon', 'Cameroon'), ('canaryislands', 'Canary Islands'), ('capeverde', 'Cape Verde'), ('centralafricanrepublic', 'Central African Republic'), ('ceuta', 'Ceuta'), ('chad', 'Chad'), ('comoros', 'Comoros'), ('cotedivoire', "Côte d'Ivoire"), ('democraticrepublicofthecongo', 'Democratic Republic of the Congo'), ('djibouti', 'Djibouti'), ('egypt', 'Egypt'), ('equatorialguinea', 'Equatorial Guinea'), ('eritrea', 'Eritrea'), ('ethiopia', 'Ethiopia'), ('gabon', 'Gabon'), ('gambia', 'Gambia'), ('ghana', 'Ghana'), ('guinea', 'Guinea'), ('guinea-bissau', 'Guinea-Bissau'), ('kenya', 'Kenya'), ('lesotho', 'Lesotho'), ('liberia', 'Liberia'), ('libya', 'Libya'), ('madagascar', 'Madagascar'), ('madeira', 'Madeira'), ('malawi', 'Malawi'), ('mali', 'Mali'), ('mauritania', 'Mauritania'), ('mauritius', 'Mauritius'), ('mayotte', 'Mayotte'), ('melilla', 'Melilla'), ('morocco', 'Morocco'), ('mozambique', 'Mozambique'), ('namibia', 'Namibia'), ('niger', 'Niger'), ('nigeria', 'Nigeria'), ('republicofthecongo', 'Republic of the Congo'), ('reunion', 'Réunion'), ('rwanda', 'Rwanda'), ('sainthelena', 'Saint Helena'), ('saotomeandpríncipe', 'São Tomé and Príncipe'), ('senegal', 'Senegal'), ('seychelles', 'Seychelles'), ('sierraleone', 'Sierra Leone'), ('somalia', 'Somalia'), ('southafrica', 'South Africa'), ('sudan', 'Sudan'), ('swaziland', 'Swaziland'), ('tanzania', 'Tanzania'), ('togo', 'Togo'), ('tunisia', 'Tunisia'), ('uganda', 'Uganda'), ('westernsahara', 'Western Sahara'), ('zambia', 'Zambia'), ('zimbabwe', 'Zimbabwe'))), ('other', 'Other')], default='guatemala', max_length=100, verbose_name='Country of origin')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('asylees', models.ManyToManyField(to='intake.Asylee', verbose_name='Asylees')),
                ('intake_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='IntakeBus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('origin', models.CharField(max_length=300, verbose_name='City of origin of the bus')),
                ('state', models.CharField(choices=[('al', 'Alabama'), ('ak', 'Alaska'), ('az', 'Arizona'), ('ar', 'Arkansas'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'Washington D.C.'), ('fl', 'Florida'), ('ga', 'Georgia'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'), ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'), ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('va', 'Virginia'), ('wa', 'Washington State'), ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming'), ('other', 'Other')], default='other', max_length=100, verbose_name='State of origin of the bus')),
                ('arrival_time', models.DateTimeField(default=datetime.datetime(2019, 7, 10, 4, 32, 42, 786017, tzinfo=utc), verbose_name='Arrival time of bus')),
                ('number', models.CharField(blank=True, max_length=300, null=True, verbose_name='Descriptive bus name')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('families', models.ManyToManyField(to='intake.Family', verbose_name='Families')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lodging_type', models.CharField(choices=[('dormitory', 'Dormitory'), ('hotel', 'Hotel'), ('motel', 'Motel'), ('other', 'Other')], default='other', max_length=100, verbose_name='Type of lodging provided')),
                ('name', models.CharField(max_length=300, verbose_name='Name of the staging location')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('intakebuses', models.ManyToManyField(to='intake.IntakeBus', verbose_name='Intake Buses')),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_valid', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=500, unique=True, verbose_name='Name of the organization')),
                ('city', models.CharField(max_length=500, null=True, verbose_name='City')),
                ('state', models.CharField(choices=[('al', 'Alabama'), ('ak', 'Alaska'), ('az', 'Arizona'), ('ar', 'Arkansas'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'Washington D.C.'), ('fl', 'Florida'), ('ga', 'Georgia'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'), ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'), ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('va', 'Virginia'), ('wa', 'Washington State'), ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming'), ('other', 'Other')], default='nm', max_length=100, verbose_name='State')),
                ('url', models.CharField(max_length=500, null=True, verbose_name='Website')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('locations', models.ManyToManyField(to='intake.Location', verbose_name='Locations')),
            ],
            options={
                'verbose_name': 'Organization',
                'verbose_name_plural': 'Organizations',
            },
        ),
        migrations.CreateModel(
            name='Sponsor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, unique=True, verbose_name="Sponsor's name")),
                ('phone_number', models.CharField(max_length=300, null=True, verbose_name="Sponsor's phone #")),
                ('address', models.CharField(max_length=300, null=True, verbose_name="Sponsor's address")),
                ('city', models.CharField(max_length=300, null=True, verbose_name="Sponsor's city")),
                ('state', models.CharField(choices=[('al', 'Alabama'), ('ak', 'Alaska'), ('az', 'Arizona'), ('ar', 'Arkansas'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'Washington D.C.'), ('fl', 'Florida'), ('ga', 'Georgia'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'), ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'), ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('va', 'Virginia'), ('wa', 'Washington State'), ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming'), ('other', 'Other')], default='other', max_length=100, verbose_name="Sponsor's state")),
                ('relation', models.CharField(max_length=300, null=True, verbose_name='Relation to family')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
            ],
        ),
        migrations.CreateModel(
            name='PointOfContact',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='intake.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='TravelPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('confirmation', models.CharField(max_length=100, null=True, verbose_name='Confirmation #')),
                ('destination_city', models.CharField(max_length=100, null=True, verbose_name='Destination city')),
                ('destination_state', models.CharField(choices=[('al', 'Alabama'), ('ak', 'Alaska'), ('az', 'Arizona'), ('ar', 'Arkansas'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'Washington D.C.'), ('fl', 'Florida'), ('ga', 'Georgia'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'), ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'), ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('va', 'Virginia'), ('wa', 'Washington State'), ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming'), ('other', 'Other')], default='other', max_length=100, verbose_name='Destination state')),
                ('travel_date', models.DateTimeField(null=True, verbose_name='Departure time of travel')),
                ('city_van_date', models.DateTimeField(null=True, verbose_name='Departure time on City Van')),
                ('travel_food_prepared', models.BooleanField(default=False, verbose_name='Is travel food prepared?')),
                ('eta', models.DateTimeField(null=True, verbose_name='Estimated time of arrival')),
                ('travel_mode', models.CharField(choices=[('Air', (('alaska', 'Alaska (AS)'), ('american', 'American (AA)'), ('delta', 'Delta (DL)'), ('frontier', 'Frontier (F9)'), ('jetblue', 'Jet Blue (B6)'), ('southwest', 'Southwest (WN)'), ('united', 'United (UA)'))), ('Bus', (('greyhound', 'Greyhound'),)), ('Train', (('amtrak', 'Amtrak'),)), ('other', 'Other')], default='other', max_length=100, verbose_name='Mode of travel')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('arranged_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Medical',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_time', models.DateTimeField(auto_now_add=True, verbose_name='Time the issue arose')),
                ('resolution_time', models.DateTimeField(null=True, verbose_name='Time the issue was resolved')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description of issue')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Additional notes')),
                ('provider', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='family',
            name='sponsor',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='intake.Sponsor', verbose_name='Sponsors'),
        ),
        migrations.AddField(
            model_name='family',
            name='travel_plan',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='intake.TravelPlan', verbose_name='Travel Plans'),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='intake.Organization')),
            ],
        ),
        migrations.AddField(
            model_name='asylee',
            name='medicals',
            field=models.ManyToManyField(to='intake.Medical', verbose_name='Medical Issues'),
        ),
        migrations.AddField(
            model_name='user',
            name='campaigns',
            field=models.ManyToManyField(to='intake.Campaign', verbose_name='Active intake campaigns'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.CreateModel(
            name='RequestQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='intake.Organization')),
                ('point_of_contact', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='intake.PointOfContact')),
            ],
        ),
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('specialty', models.CharField(choices=[('activities', 'Activities'), ('changeofaddress', 'Change of Address'), ('clothes', 'Clothes'), ('departurebags', 'Departure Bags'), ('food', 'Food'), ('intake', 'Intake'), ('medical', 'Medical'), ('travel', 'Travel'), ('transport', 'Transport'), ('volunteercoordinator', 'Volunteer Coordinator'), ('other', 'Other')], default='other', max_length=100, verbose_name='Team lead area')),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='intake.Organization')),
            ],
        ),
    ]
