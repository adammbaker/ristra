# Generated by Django 2.2.1 on 2019-06-01 02:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0003_auto_20190601_0226'),
    ]

    operations = [
        migrations.CreateModel(
            name='Families',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('family_name', models.CharField(max_length=500, verbose_name='name of family unit')),
                ('destination', models.CharField(max_length=300)),
                ('language_spoken', models.CharField(choices=[('Latin', (('portuguese', 'Brazilian/Portuguese'), ('spanish', 'Spanish'))), ('Maya', (('achi', 'Achi'), ('awakatek', 'Awakatek'), ('chorti', "Ch'orti'"), ('chuj', 'Chuj'), ('itza', "Itza'"), ('ixil', 'Ixil'), ('jakaltek', 'Jakaltek'), ('kiche', "K'iche'"), ('kaqchiquel', 'Kaqchiquel'), ('mam', 'Mam'), ('mopan', 'Mopan'), ('poqomam', 'Poqomam'), ('poqomchi', "Poqomchi'"), ('qanjobal', "Q'anjob'al"), ('qeqchi', "Q'eqchi'"), ('sakapultek', 'Sakapultek'), ('sipakapense', 'Sipakapense'), ('tektitek', 'Tektitek'), ('tzutujil', "Tz'utujil"), ('upsantek', 'Upsantek'), ('other', 'Other'))), ('other', 'Other')], default='spanish', max_length=2)),
                ('travel_permission_date', models.DateTimeField(blank=True, null=True, verbose_name='okayed to travel')),
                ('notes', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='asylees',
            name='family',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='intake.Families'),
        ),
        migrations.AlterField(
            model_name='asylees',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='intakebuses',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='locations',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='medical',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='sponsors',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='travelplans',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='volunteers',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Family',
        ),
        migrations.DeleteModel(
            name='Notes',
        ),
        migrations.AddField(
            model_name='families',
            name='intake_bus',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='intake.IntakeBuses'),
        ),
        migrations.AddField(
            model_name='families',
            name='lodging',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='intake.Lodging'),
        ),
        migrations.AddField(
            model_name='families',
            name='sponsor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='intake.Sponsors'),
        ),
        migrations.AddField(
            model_name='families',
            name='taken_in_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='intake.Volunteers', verbose_name='intake by (volunteer)'),
        ),
        migrations.AddField(
            model_name='families',
            name='travel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='intake.TravelPlans'),
        ),
    ]
