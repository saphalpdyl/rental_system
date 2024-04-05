# Generated by Django 5.0.1 on 2024-04-05 03:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_app', '0021_transactionrequest_transactions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notifications',
            name='notification_redirect_link',
        ),
        migrations.AddField(
            model_name='notifications',
            name='related_transaction_request',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base_app.transactionrequest'),
        ),
    ]