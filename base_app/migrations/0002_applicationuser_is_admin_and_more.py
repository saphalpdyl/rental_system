# Generated by Django 5.0 on 2023-12-30 05:14

import base_app.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="applicationuser",
            name="is_admin",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="applicationuser",
            name="user_id",
            field=models.CharField(
                default=base_app.models.generate_uuid,
                max_length=32,
                primary_key=True,
                serialize=False,
                unique=True,
            ),
        ),
        migrations.CreateModel(
            name="RenterUser",
            fields=[
                (
                    "renter_id",
                    models.CharField(
                        default=base_app.models.generate_uuid,
                        max_length=32,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                (
                    "application_user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
