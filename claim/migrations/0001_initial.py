# Generated by Django 5.1 on 2024-09-04 12:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Claim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('claimedUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='receivedClaim', to=settings.AUTH_USER_MODEL)),
                ('claimingUser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='myClaim', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
