# Generated by Django 3.0.3 on 2020-03-17 21:37

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0007_auto_20200302_2330"),
    ]

    operations = [
        migrations.CreateModel(
            name="Todo",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("body", models.CharField(max_length=500)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("completed_at", models.DateTimeField(default=None, null=True)),
            ],
        ),
    ]
