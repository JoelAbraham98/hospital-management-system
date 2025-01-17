# Generated by Django 5.0.6 on 2024-07-18 12:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0013_alter_patient_gender_alter_patient_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='doctor',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.doctor'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='is_doctor',
            field=models.BooleanField(default=False),
        ),
    ]
