# Generated by Django 4.2.3 on 2024-08-05 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0032_alter_answersstudent_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answersstudent',
            name='status',
            field=models.CharField(choices=[(0, 'Not specified'), (1, 'Suggest edits'), (2, 'Submit feedback')], default='Not specified', max_length=50, verbose_name='Статус проверки'),
        ),
    ]
