# Generated by Django 5.0.3 on 2024-03-22 16:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_profile_picture_myuser_profile_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentpost',
            name='name',
        ),
    ]
