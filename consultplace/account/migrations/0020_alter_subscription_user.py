# Generated by Django 4.2.3 on 2024-05-07 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0019_remove_student_subscription_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.student', verbose_name='Пользователь'),
        ),
    ]
