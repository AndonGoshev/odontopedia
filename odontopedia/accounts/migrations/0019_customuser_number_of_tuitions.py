# Generated by Django 5.1.5 on 2025-02-19 09:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_rename_birth_date_profile_date_of_birth'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='number_of_tuitions',
            field=models.IntegerField(default=1),
        ),
    ]
