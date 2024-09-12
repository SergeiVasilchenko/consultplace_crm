# Generated by Django 4.2.3 on 2024-06-22 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0028_projectinvitation_studentinvitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectinvitation',
            name='students',
            field=models.ManyToManyField(related_name='project_invitations', to='account.student'),
        ),
    ]
