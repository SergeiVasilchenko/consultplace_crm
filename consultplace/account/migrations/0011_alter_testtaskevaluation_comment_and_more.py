# Generated by Django 4.2.3 on 2024-04-22 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0010_rename_assigned_tesstask_testtaskevaluation_assigned_testtask'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testtaskevaluation',
            name='comment',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='testtaskevaluation',
            name='is_completed',
            field=models.BooleanField(blank=True, choices=[('Да', 'Yes'), ('Нет', 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='testtaskevaluation',
            name='url',
            field=models.URLField(blank=True, null=True, verbose_name='Выполненное задание (ссылка)'),
        ),
    ]
