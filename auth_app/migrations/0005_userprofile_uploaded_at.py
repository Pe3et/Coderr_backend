# Generated by Django 5.1.5 on 2025-02-14 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0004_alter_userprofile_file_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='uploaded_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
