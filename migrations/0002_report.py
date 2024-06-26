# Generated by Django 4.0.6 on 2023-02-21 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('age', models.CharField(max_length=200, null=True)),
                ('systolicBP', models.CharField(max_length=200, null=True)),
                ('diastolicBP', models.CharField(max_length=200, null=True)),
                ('bs', models.CharField(max_length=200, null=True)),
                ('bodytemp', models.CharField(max_length=200, null=True)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]