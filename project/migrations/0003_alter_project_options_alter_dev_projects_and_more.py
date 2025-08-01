# Generated by Django 5.2.3 on 2025-06-23 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_task_assigned'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-name'], 'verbose_name': 'Project', 'verbose_name_plural': 'Projects'},
        ),
        migrations.AlterField(
            model_name='dev',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='devs', to='project.project'),
        ),
        migrations.AlterField(
            model_name='project',
            name='lang',
            field=models.CharField(choices=[('py', '🐍Python'), ('js', 'JavaScript'), ('c#', 'C#'), ('c++', '➕C++'), ('java', '☕️Java')], max_length=10),
        ),
        migrations.AlterUniqueTogether(
            name='project',
            unique_together={('name', 'description')},
        ),
    ]
