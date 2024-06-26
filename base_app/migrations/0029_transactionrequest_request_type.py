# Generated by Django 5.0 on 2024-04-18 14:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_app", "0028_vehicles_location_lat_vehicles_location_lng"),
    ]

    operations = [
        migrations.AddField(
            model_name="transactionrequest",
            name="request_type",
            field=models.TextField(
                choices=[("RENTAL", "Rental"), ("EXTENSION", "Extension")],
                default="RENTAL",
            ),
        ),
    ]
