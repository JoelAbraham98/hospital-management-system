# Generated by Django 5.0.6 on 2024-07-13 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0007_remove_medicalrecord_diagnosis_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='slot',
        ),
        migrations.AddField(
            model_name='patient',
            name='slot_date_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
