# Generated by Django 4.2.16 on 2024-10-21 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_book_discount_percent'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='epub_file',
            field=models.FileField(blank=True, null=True, upload_to='epub_files/'),
        ),
    ]
