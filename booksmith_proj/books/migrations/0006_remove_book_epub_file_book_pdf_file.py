# Generated by Django 4.2.16 on 2024-10-21 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_book_epub_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='epub_file',
        ),
        migrations.AddField(
            model_name='book',
            name='pdf_file',
            field=models.FileField(blank=True, null=True, upload_to='pdf_files/'),
        ),
    ]
