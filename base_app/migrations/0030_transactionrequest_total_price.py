# Generated by Django 5.0 on 2024-04-18 14:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("base_app", "0029_transactionrequest_request_type"),
    ]

    operations = [
        migrations.AddField(
            model_name="transactionrequest",
            name="total_price",
            field=models.FloatField(blank=True, null=True),
        ),
    ]
