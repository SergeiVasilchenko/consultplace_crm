# Generated by Django 4.2.3 on 2024-08-25 14:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0036_remove_answersstudent_answer_answersstudent_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taskstudent',
            name='task_rating',
        ),
    ]
