# Generated by Django 3.1.7 on 2021-04-04 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('intake', '0020_auto_20210401_2216'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lead',
            name='specialty',
            field=models.CharField(choices=[('clothes', 'Clothes'), ('concierge', 'Concierge'), ('departurebags', 'Departure Bags'), ('food', 'Food'), ('intake', 'Intake'), ('travel', 'Travel'), ('transportation', 'Transportation'), ('volunteercoordinator', 'Volunteer Coordinator'), ('other', 'Other')], default='other', max_length=100, verbose_name='Team lead area'),
        ),
    ]