# Generated by Django 4.2.16 on 2024-11-04 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(blank=True, default='default_avatar.png', null=True, upload_to='profile_pics'),
        ),
    ]