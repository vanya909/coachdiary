# Generated by Django 5.0.2 on 2024-05-23 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0003_alter_studentstandard_grade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentstandard',
            name='grade',
            field=models.FloatField(max_length=255, verbose_name='Оценка'),
        ),
    ]
