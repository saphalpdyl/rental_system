# Generated by Django 5.0 on 2024-01-15 14:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_app", "0011_delete_vehiclelistingresult"),
    ]

    operations = [
        migrations.AlterField(
            model_name="applicationuser",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="uploadsw/"),
        ),
    ]