# Generated by Django 5.1 on 2024-09-03 00:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0008_alter_school_name_alter_school_province_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='school',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='board.school'),
        ),
    ]
