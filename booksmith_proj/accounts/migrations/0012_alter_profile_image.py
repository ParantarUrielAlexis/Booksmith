# Generated by Django 4.2.16 on 2024-11-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_profile_bought_books'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default_avatar.png', null=True, upload_to='profile_pics'),
        ),
    ]