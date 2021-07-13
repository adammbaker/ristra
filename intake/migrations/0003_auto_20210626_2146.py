# Generated by Django 3.2.4 on 2021-06-26 21:46

from django.db import migrations, models
import intake.models


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0002_auto_20210626_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicalorganization',
            name='historical_travel_duration',
            field=models.JSONField(default=intake.models.get_default_travel_duration),
        ),
        migrations.AlterField(
            model_name='organization',
            name='historical_travel_duration',
            field=models.JSONField(default=intake.models.get_default_travel_duration),
        ),
    ]