# Generated by Django 5.0.2 on 2024-05-12 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_user_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(default='admin', max_length=255),
            preserve_default=False,
        ),
    ]