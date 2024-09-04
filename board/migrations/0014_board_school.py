# Generated by Django 5.1 on 2024-09-04 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0013_remove_board_school_delete_school'),
        ('member', '0009_remove_userprofile_class_number_1_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='school',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='member.school'),
        ),
    ]
