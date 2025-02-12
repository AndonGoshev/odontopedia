# Generated by Django 5.1.5 on 2025-02-12 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_alter_profile_age_alter_profile_bio_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='age',
        ),
        migrations.AddField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='university',
            field=models.CharField(blank=True, choices=[('Select University', 'Initial'), ('PLOVDIV MED UNI', 'Plovdiv Med Uni'), ('VARNA MED UNI', 'Varna Med Uni')], default='Select University', max_length=255, null=True),
        ),
    ]
