# Generated by Django 2.2.1 on 2019-06-11 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0025_auto_20190611_1720'),
    ]

    operations = [
        migrations.AddField(
            model_name='families',
            name='days_detained',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='families',
            name='days_traveling',
            field=models.IntegerField(null=True),
        ),
    ]
