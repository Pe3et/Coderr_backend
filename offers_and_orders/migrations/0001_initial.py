# Generated by Django 5.1.5 on 2025-01-29 13:19

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='OfferDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('revisions', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(-1)])),
                ('delivery_time_in_days', models.PositiveIntegerField(default=1)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('offer_type', models.CharField(choices=[('basic', 'BASIC'), ('standard', 'Standard'), ('premium', 'Premium')], max_length=20)),
                ('features', models.ManyToManyField(related_name='offers', to='offers_and_orders.feature')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='offers_and_orders.offer')),
            ],
            options={
                'unique_together': {('offer', 'offer_type')},
            },
        ),
    ]
