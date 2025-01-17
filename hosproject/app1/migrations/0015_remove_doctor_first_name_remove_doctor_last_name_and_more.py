# Generated by Django 5.0.6 on 2024-07-18 13:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_userprofile_doctor_userprofile_is_doctor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='doctor',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='doctor',
            name='last_name',
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
