# Generated by Django 5.0 on 2024-04-22 15:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("base_app", "0032_review"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="review",
            name="is_rating_only",
        ),
    ]