# Generated by Django 5.0.6 on 2024-07-23 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0022_appointment_description_appointment_document'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appointment',
            name='description',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='document',
        ),
    ]