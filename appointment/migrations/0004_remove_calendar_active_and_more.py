# Generated by Django 5.0.1 on 2024-02-27 20:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0003_alter_availability_day_of_week'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendar',
            name='active',
        ),
        migrations.RemoveField(
            model_name='calendar',
            name='appointments_limit_per_day',
        ),
    ]
