# Generated by Django 5.1.5 on 2025-02-04 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_customuser_profile_image_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='age',
            field=models.PositiveSmallIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='default_images/profile_image.jpg', upload_to='<django.db.models.fields.CharField>-<django.db.models.fields.CharField>/profile_images'),
        ),
    ]
