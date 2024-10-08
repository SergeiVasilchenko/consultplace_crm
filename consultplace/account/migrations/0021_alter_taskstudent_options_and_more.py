# Generated by Django 4.2.3 on 2024-05-13 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0020_alter_subscription_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='taskstudent',
            options={'verbose_name': 'Задача специалиста по проекту', 'verbose_name_plural': 'Задачи специалистов по проекту'},
        ),
        # migrations.RemoveField(
        #     model_name='taskstudent',
        #     name='task_rating',
        # ),
        migrations.AddField(
            model_name='taskstudent',
            name='intricacy_coefficient',
            field=models.FloatField(blank=True, max_length=2, null=True, verbose_name='Коэффициент сложности'),
        ),
        migrations.AddField(
            model_name='taskstudent',
            name='task_credits',
            field=models.PositiveSmallIntegerField(blank=True, max_length=30, null=True, verbose_name='Кредиты'),
        ),
        migrations.AlterField(
            model_name='taskstudent',
            name='deadline_compliance',
            field=models.FloatField(blank=True, max_length=2, null=True, verbose_name='Соблюдение дедлайнов'),
        ),
        migrations.AlterField(
            model_name='taskstudent',
            name='personal_grade',
            field=models.FloatField(blank=True, max_length=1, null=True, verbose_name='Оценка по проекту'),
        ),
    ]
