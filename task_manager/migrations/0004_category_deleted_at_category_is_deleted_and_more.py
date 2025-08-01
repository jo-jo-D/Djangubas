# Generated by Django 5.2.3 on 2025-07-29 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_alter_subtask_deadline_alter_task_deadline'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='deleted_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='deleted at'),
        ),
        migrations.AddField(
            model_name='category',
            name='is_deleted',
            field=models.BooleanField(default=False, verbose_name='is deleted'),
        ),
        migrations.AddField(
            model_name='category',
            name='restored_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='restored at'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('work', 'Work'), ('personal', 'Personal'), ('home', 'Home'), ('health', 'Health'), ('finance', 'Finance'), ('study', 'Study / Education'), ('meetings', 'Meetings'), ('shopping', 'Shopping'), ('travel', 'Travel'), ('other', 'others')], max_length=50, verbose_name='category of the task'),
        ),
    ]
