# Generated by Django 4.1.7 on 2024-04-22 06:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("home", "0004_patientspecial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Settings",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("ngroklink", models.CharField(max_length=200, null=True)),
            ],
        ),
    ]
