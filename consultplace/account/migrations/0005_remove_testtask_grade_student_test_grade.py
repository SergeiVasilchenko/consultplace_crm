# Generated by Django 4.2.3 on 2024-04-17 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_testtask_task_duration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testtask',
            name='grade',
        ),
        migrations.AddField(
            model_name='student',
            name='test_grade',
            field=models.IntegerField(blank=True, default=0, null=True, verbose_name='Тестовая оценка'),
        ),
    ]
