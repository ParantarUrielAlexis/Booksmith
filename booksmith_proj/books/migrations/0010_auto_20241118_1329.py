from django.db import migrations, models

def normalize_data(apps, schema_editor):
    Book = apps.get_model('books', 'Book')
    Author = apps.get_model('books', 'Author')
    Category = apps.get_model('books', 'Category')

    # Cache to avoid duplicates
    author_cache = {}
    category_cache = {}

    for book in Book.objects.all():
        # Handle missing or NULL author/category values
        author_name = book.author if book.author else "Unknown Author"
        category_name = book.category if book.category else "Uncategorized"

        # Normalize authors
        if author_name not in author_cache:
            author, _ = Author.objects.get_or_create(name=author_name)
            author_cache[author_name] = author
        else:
            author = author_cache[author_name]

        # Normalize categories
        if category_name not in category_cache:
            category, _ = Category.objects.get_or_create(name=category_name)
            category_cache[category_name] = category
        else:
            category = category_cache[category_name]

        # Update book's foreign keys
        book.author = author
        book.category = category
        book.save()

class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_book_recommended'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.ForeignKey(to='books.Author', on_delete=models.CASCADE, null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(to='books.Category', on_delete=models.CASCADE, null=True),
        ),
        migrations.RunPython(normalize_data),
    ]
