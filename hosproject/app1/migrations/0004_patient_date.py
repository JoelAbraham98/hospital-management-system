# Generated by Django 5.0.6 on 2024-07-13 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_patient_slot'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='date',
            field=models.DateField(default='2024-07-13'),
        ),
    ]