# Generated by Django 3.0.3 on 2020-02-18 23:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0002_notification"),
    ]

    operations = [
        migrations.AddField(
            model_name="assignment",
            name="week_start",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
