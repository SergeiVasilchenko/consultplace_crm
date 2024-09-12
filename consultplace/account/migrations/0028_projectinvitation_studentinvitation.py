# Generated by Django 4.2.3 on 2024-06-22 09:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0027_testtaskevaluation_date_accepted'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('invitation_duration', models.IntegerField(default=2, verbose_name='Срок действия')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitations', to='account.project')),
            ],
        ),
        migrations.CreateModel(
            name='StudentInvitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction_status', models.IntegerField(default=0, verbose_name='Статус отклика')),
                ('invitation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_invitations', to='account.projectinvitation', verbose_name='Приглашение')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student_invitations', to='account.student', verbose_name='Приглашенный специалист')),
            ],
        ),
    ]
