# Generated by Django 5.0.6 on 2024-07-14 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0010_patient_appointment_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='reason_for_visit',
        ),
    ]