# Generated by Django 2.2.1 on 2019-06-05 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0014_auto_20190605_0353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='states',
            name='abbreviation',
            field=models.CharField(max_length=5, unique=True, verbose_name='State abbreviation'),
        ),
    ]
