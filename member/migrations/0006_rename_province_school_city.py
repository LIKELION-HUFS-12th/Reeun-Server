# Generated by Django 5.1 on 2024-09-02 01:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_school_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='school',
            old_name='province',
            new_name='city',
        ),
    ]
