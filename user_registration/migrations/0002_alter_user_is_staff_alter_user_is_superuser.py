# Generated by Django 4.1.4 on 2023-12-03 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_staff',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=True),
        ),
    ]