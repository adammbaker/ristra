# Generated by Django 3.1.7 on 2021-02-27 23:15

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='intakebus',
            name='origin',
            field=models.CharField(default='El Paso', max_length=300, verbose_name='City of origin of the bus'),
        ),
        migrations.AlterField(
            model_name='intakebus',
            name='state',
            field=models.CharField(choices=[('al', 'Alabama'), ('ak', 'Alaska'), ('az', 'Arizona'), ('ar', 'Arkansas'), ('ca', 'California'), ('co', 'Colorado'), ('ct', 'Connecticut'), ('de', 'Delaware'), ('dc', 'Washington D.C.'), ('fl', 'Florida'), ('ga', 'Georgia'), ('hi', 'Hawaii'), ('id', 'Idaho'), ('il', 'Illinois'), ('in', 'Indiana'), ('ia', 'Iowa'), ('ks', 'Kansas'), ('ky', 'Kentucky'), ('la', 'Louisiana'), ('me', 'Maine'), ('md', 'Maryland'), ('ma', 'Massachusetts'), ('mi', 'Michigan'), ('mn', 'Minnesota'), ('ms', 'Mississippi'), ('mo', 'Missouri'), ('mt', 'Montana'), ('ne', 'Nebraska'), ('nv', 'Nevada'), ('nh', 'New Hampshire'), ('nj', 'New Jersey'), ('nm', 'New Mexico'), ('ny', 'New York'), ('nc', 'North Carolina'), ('nd', 'North Dakota'), ('oh', 'Ohio'), ('ok', 'Oklahoma'), ('or', 'Oregon'), ('pa', 'Pennsylvania'), ('pr', 'Puerto Rico'), ('ri', 'Rhode Island'), ('sc', 'South Carolina'), ('sd', 'South Dakota'), ('tn', 'Tennessee'), ('tx', 'Texas'), ('ut', 'Utah'), ('vt', 'Vermont'), ('va', 'Virginia'), ('wa', 'Washington State'), ('wv', 'West Virginia'), ('wi', 'Wisconsin'), ('wy', 'Wyoming'), ('other', 'Other')], default='tx', max_length=100, verbose_name='State of origin of the bus'),
        ),
        migrations.AlterField(
            model_name='medical',
            name='chronic_medical_problems',
            field=django_cryptography.fields.encrypt(models.CharField(blank=True, max_length=200, null=True, verbose_name='Chronic health issues')),
        ),
    ]