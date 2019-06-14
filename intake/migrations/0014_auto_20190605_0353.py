# Generated by Django 2.2.1 on 2019-06-05 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0013_auto_20190605_0341'),
    ]

    operations = [
        migrations.CreateModel(
            name='States',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='State')),
                ('abbreviation', models.CharField(max_length=5, verbose_name='State abbreviation')),
            ],
        ),
        migrations.AlterField(
            model_name='organizations',
            name='location_state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='intake.States', verbose_name='State'),
        ),
    ]
