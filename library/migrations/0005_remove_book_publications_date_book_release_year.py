# Generated by Django 5.2.3 on 2025-06-22 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0004_alter_author_deleted_alter_author_profile_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='publications_date',
        ),
        migrations.AddField(
            model_name='book',
            name='release_year',
            field=models.IntegerField(default=2025, verbose_name='release date'),
        ),
    ]
