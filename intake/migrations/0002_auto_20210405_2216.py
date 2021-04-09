# Generated by Django 3.1.7 on 2021-04-06 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoricalAge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.CharField(max_length=10)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_age_count',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_asylees_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_country_of_origin',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_days_at_border',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_days_in_detention',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_destinations',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_detention_type',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_families_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_languages_spoken',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_needs',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_sex_count',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_sick_covid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_sick_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='historicalorganization',
            name='historical_travel_duration',
            field=models.JSONField(default={'bus': [0, 0], 'plane': [0, 0], 'private_car': [0, 0], 'train': [0, 0]}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_age_count',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_asylees_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_country_of_origin',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_days_at_border',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_days_in_detention',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_destinations',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_detention_type',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_families_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_languages_spoken',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_needs',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_sex_count',
            field=models.JSONField(default={}),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_sick_covid',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_sick_other',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='organization',
            name='historical_travel_duration',
            field=models.JSONField(default={'bus': [0, 0], 'plane': [0, 0], 'private_car': [0, 0], 'train': [0, 0]}),
        ),
        migrations.AlterField(
            model_name='asylee',
            name='vaccine_received',
            field=models.CharField(blank=True, choices=[('pfizer', 'Pfizer'), ('moderna', 'Moderna'), ('j_and_j', 'Johnson & Johnson'), ('astra_zeneca', 'AstraZeneca'), ('sinovac', 'Sinovac'), ('unknown', 'Unknown'), ('other', 'Other')], max_length=100, null=True, verbose_name='Vaccine manufacturer'),
        ),
        migrations.AlterField(
            model_name='historicalasylee',
            name='vaccine_received',
            field=models.CharField(blank=True, choices=[('pfizer', 'Pfizer'), ('moderna', 'Moderna'), ('j_and_j', 'Johnson & Johnson'), ('astra_zeneca', 'AstraZeneca'), ('sinovac', 'Sinovac'), ('unknown', 'Unknown'), ('other', 'Other')], max_length=100, null=True, verbose_name='Vaccine manufacturer'),
        ),
        migrations.AlterField(
            model_name='historicalheadofhousehold',
            name='vaccine_received',
            field=models.CharField(blank=True, choices=[('pfizer', 'Pfizer'), ('moderna', 'Moderna'), ('j_and_j', 'Johnson & Johnson'), ('astra_zeneca', 'AstraZeneca'), ('sinovac', 'Sinovac'), ('unknown', 'Unknown'), ('other', 'Other')], max_length=100, null=True, verbose_name='Vaccine manufacturer'),
        ),
        migrations.CreateModel(
            name='HistoricalData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('families_count', models.IntegerField(default=0)),
                ('asylees_count', models.IntegerField(default=0)),
                ('organization', models.OneToOneField(on_delete=models.SET('deleted'), to='intake.organization')),
            ],
        ),
    ]