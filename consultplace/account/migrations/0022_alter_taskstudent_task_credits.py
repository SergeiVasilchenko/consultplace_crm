# Generated by Django 4.2.3 on 2024-05-13 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0021_alter_taskstudent_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taskstudent',
            name='task_credits',
            field=models.PositiveIntegerField(blank=True, max_length=30, null=True, verbose_name='Кредиты'),
        ),
    ]
