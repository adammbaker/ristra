# Generated by Django 2.2.1 on 2019-06-06 01:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0023_auto_20190606_0142'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='capacities',
            options={'verbose_name': 'Capacity', 'verbose_name_plural': 'Capacities'},
        ),
        migrations.AlterModelOptions(
            name='languages',
            options={'verbose_name': 'Language', 'verbose_name_plural': 'Languages'},
        ),
        migrations.AlterModelOptions(
            name='lodgingtypes',
            options={'verbose_name': 'Lodging', 'verbose_name_plural': 'Lodging'},
        ),
        migrations.AlterModelOptions(
            name='organizations',
            options={'verbose_name': 'Organization', 'verbose_name_plural': 'Organizations'},
        ),
        migrations.AlterModelOptions(
            name='states',
            options={'verbose_name': 'State', 'verbose_name_plural': 'States'},
        ),
        migrations.AlterModelOptions(
            name='volunteers',
            options={'verbose_name': 'Volunteer', 'verbose_name_plural': 'Volunteers'},
        ),
    ]
