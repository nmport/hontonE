# Generated by Django 3.1.5 on 2022-03-10 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_bookline_bookword'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookword',
            name='words',
        ),
        migrations.AddField(
            model_name='bookword',
            name='word',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='book_words', to='books.Word'),
        ),
        migrations.AlterField(
            model_name='bookline',
            name='line_romaji',
            field=models.CharField(default=None, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='bookword',
            name='indices',
            field=models.CharField(default='', max_length=1000),
        ),
    ]