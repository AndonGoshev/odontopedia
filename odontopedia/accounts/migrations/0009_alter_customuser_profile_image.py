# Generated by Django 5.1.5 on 2025-02-10 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(default='default_images/profile_image.jpg', upload_to='profile_images'),
        ),
    ]
