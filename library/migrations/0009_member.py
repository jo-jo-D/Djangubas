# Generated by Django 5.2.3 on 2025-06-22 21:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_library_rename_publisher_book_publishers_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, verbose_name="Library member's name")),
                ('last_name', models.CharField(max_length=70, verbose_name="Library member's last name")),
                ('email', models.EmailField(max_length=70, unique=True, verbose_name="Library member's email")),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('Other', 'Other'), ('ns', 'not set')], default='ns', verbose_name='Gender')),
                ('date_of_birth', models.DateField(blank=True, null=True, verbose_name='Date of birth')),
                ('age', models.PositiveIntegerField(blank=True, null=True, verbose_name='Age')),
                ('role', models.CharField(choices=[('admin', 'Administrator'), ('editor', 'Editor'), ('employee', 'Employee'), ('staff', 'Staff'), ('reader', 'Reader')], max_length=30, verbose_name='Role')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('libraries', models.ManyToManyField(related_name='members', to='library.library', verbose_name='Library')),
            ],
        ),
    ]
