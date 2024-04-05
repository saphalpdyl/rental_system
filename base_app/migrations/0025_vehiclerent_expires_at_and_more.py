# Generated by Django 5.0.1 on 2024-04-05 07:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0024_remove_vehiclerent_renting_period_remaining'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclerent',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 4, 5, 7, 43, 33, 582666, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='vehiclerentingrequests',
            name='renting_period',
            field=models.DurationField(),
        ),
    ]
