# Generated by Django 5.1.5 on 2025-02-12 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0015_customuser_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, default='Please add some information about you.', max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='university',
            field=models.CharField(blank=True, choices=[('plovdiv_med_uni', 'PLOVDIV_MED_UNI'), ('varna_med_uni', 'VARNA_MED_UNI')], default='', max_length=255, null=True),
        ),
    ]
