# Generated by Django 4.2.16 on 2024-10-20 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_discount_percent'),
        ('accounts', '0008_alter_profile_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='bought_books',
            field=models.ManyToManyField(blank=True, to='books.book'),
        ),
    ]