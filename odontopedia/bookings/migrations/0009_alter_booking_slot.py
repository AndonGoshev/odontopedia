# Generated by Django 5.1.5 on 2025-02-19 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0008_booking_date_booking_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bookings.availableslot'),
        ),
    ]
