# Generated by Django 5.1 on 2024-09-04 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classboard', '0006_classboard_class_number_classboard_grade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='classboard',
            name='admission_year',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='classboard',
            name='grade',
            field=models.IntegerField(default=0),
        ),
    ]
