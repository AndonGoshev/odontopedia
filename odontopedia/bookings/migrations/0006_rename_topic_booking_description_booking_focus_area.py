# Generated by Django 5.1.5 on 2025-02-19 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0005_booking_session_completed'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='topic',
            new_name='description',
        ),
        migrations.AddField(
            model_name='booking',
            name='focus_area',
            field=models.CharField(default='some focus area title', max_length=100),
            preserve_default=False,
        ),
    ]
