# Generated by Django 5.1.5 on 2025-02-19 08:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0003_rename_link_meetingroom_room_link'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='topic',
            field=models.CharField(default='some topic here', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='booking',
            name='video_link',
            field=models.URLField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
    ]
