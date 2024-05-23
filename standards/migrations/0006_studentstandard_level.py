# Generated by Django 5.0.2 on 2024-05-23 13:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standards', '0005_alter_studentstandard_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentstandard',
            name='level',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='standards.level', verbose_name='Уровень'),
        ),
    ]
