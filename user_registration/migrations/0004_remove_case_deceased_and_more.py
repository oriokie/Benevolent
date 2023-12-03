# Generated by Django 4.1.4 on 2023-12-02 23:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_registration', '0003_alter_case_relationship_with_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='case',
            name='deceased',
        ),
        migrations.RemoveField(
            model_name='case',
            name='relationship_with_user',
        ),
        migrations.AddField(
            model_name='case',
            name='case_number',
            field=models.CharField(default=0, max_length=20, unique=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='dependant',
            name='is_deceased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='spouse',
            name='is_deceased',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='is_deceased',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='spouse',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spouses', to='user_registration.user'),
        ),
    ]
