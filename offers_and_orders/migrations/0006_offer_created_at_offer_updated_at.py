# Generated by Django 5.1.5 on 2025-02-05 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers_and_orders', '0005_offer_min_delivery_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='offer',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
