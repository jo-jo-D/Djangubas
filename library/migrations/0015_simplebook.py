# Generated by Django 5.2.3 on 2025-08-01 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0014_actor_director_user_book_owner_authordetail_borrow_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleBook',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('publication_date', models.DateField()),
            ],
        ),
    ]
