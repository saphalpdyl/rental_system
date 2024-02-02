# Generated by Django 5.0.1 on 2024-01-29 13:31

import base_app.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0013_alter_applicationuser_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifications',
            fields=[
                ('reference_id', models.CharField(default=base_app.models.generate_uuid, max_length=32, primary_key=True, serialize=False, unique=True)),
                ('data_generated_on', models.DateTimeField(auto_now_add=True)),
                ('message', models.CharField(max_length=100)),
                ('desc', models.TextField(blank=True, null=True)),
                ('notification_for', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
