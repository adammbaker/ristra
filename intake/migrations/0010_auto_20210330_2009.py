# Generated by Django 3.1.7 on 2021-03-31 02:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0009_auto_20210302_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='asylee',
            name='had_covid_disease',
            field=models.BooleanField(default=False, verbose_name='Has had COVID disease in the past'),
        ),
        migrations.CreateModel(
            name='Donate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Name')),
                ('url', models.URLField(blank=True, max_length=1000, null=True, verbose_name='URL')),
                ('description', models.TextField(null=True)),
                ('organization', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='intake.organization', verbose_name='Organization')),
            ],
        ),
    ]
