# Generated by Django 5.1.5 on 2025-02-04 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='premium_status',
            field=models.BooleanField(default=False),
        ),
    ]
