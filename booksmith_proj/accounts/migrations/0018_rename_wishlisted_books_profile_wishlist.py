# Generated by Django 4.2.16 on 2024-11-08 04:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0017_profile_wishlisted_books_alter_profile_bought_books_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='wishlisted_books',
            new_name='wishlist',
        ),
    ]