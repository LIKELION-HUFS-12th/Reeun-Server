# Generated by Django 5.1 on 2024-09-02 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0007_school'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='school',
            name='province',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='school',
            name='school_type',
            field=models.CharField(max_length=50),
        ),
    ]
