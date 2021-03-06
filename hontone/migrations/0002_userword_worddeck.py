# Generated by Django 3.1.5 on 2022-03-11 10:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20220227_1920'),
        ('hontone', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('UNKNOWN', 'UNKNOWN'), ('LEARNING', 'LEARNING'), ('KNOWN', 'KNOWN')], default='UNKNOWN', max_length=20)),
                ('level', models.CharField(default=None, max_length=20, null=True)),
                ('last_updated', models.DateTimeField(default=None, null=True)),
                ('next_review', models.DateTimeField(default=None, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_words', to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_word', to='books.Word')),
            ],
        ),
        migrations.CreateModel(
            name='WordDeck',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('books', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='word_decks', to='books.Book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='word_decks', to=settings.AUTH_USER_MODEL)),
                ('user_words', models.ManyToManyField(related_name='word_decks', to='hontone.UserWord')),
            ],
        ),
    ]
