# Generated by Django 5.1.5 on 2025-02-19 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0006_rename_topic_booking_description_booking_focus_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='TuitionFocusArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
