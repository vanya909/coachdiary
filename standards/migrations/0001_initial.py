# Generated by Django 5.0.2 on 2024-04-20 13:16

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=255, verbose_name='Название норматива')),
                ('has_numeric_value', models.BooleanField(help_text='Если True, то это умение. Иначе - норматив', verbose_name='Является ли это умением или нормативом')),
                ('who_added', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Кто добавил норматив')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('number', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(11)], verbose_name='Номер учебного класса')),
                ('class_name', models.CharField(help_text='А, Б, В, ...', max_length=1, verbose_name='Буква учебного класса')),
                ('recruitment_year', models.IntegerField(validators=[django.core.validators.MinValueValidator(2000)], verbose_name='Год набора')),
                ('class_owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Куратор класса')),
            ],
            options={
                'unique_together': {('number', 'class_name')},
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('full_name', models.CharField(help_text='Петров Петр Петрович', max_length=1024, verbose_name='Полное имя ученика')),
                ('birthday', models.DateField(verbose_name='Дата рождения ученика')),
                ('gender', models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')], max_length=1, verbose_name='Пол ученика')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standards.studentclass', verbose_name='Класс ученика')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StandardValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('level', models.CharField(max_length=255, verbose_name='Уровень физподготовки')),
                ('value', models.FloatField(verbose_name='Значение')),
                ('gender', models.CharField(choices=[('m', 'Мужской'), ('f', 'Женский')], max_length=1, verbose_name='Пол ученика')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standards.standard', verbose_name='Норматив')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standards.studentclass', verbose_name='Класс')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudentStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('restored_at', models.DateTimeField(blank=True, null=True)),
                ('grade', models.CharField(max_length=255, verbose_name='Оценка')),
                ('value', models.FloatField(verbose_name='Значение')),
                ('standard', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standards.standard', verbose_name='Норматив')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='standards.student', verbose_name='Ученик')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]