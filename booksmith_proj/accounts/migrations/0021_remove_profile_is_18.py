# Generated by Django 4.2.16 on 2024-11-26 03:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_profile_is_18'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_18',
        ),
    ]