# Generated by Django 5.0.6 on 2024-07-13 06:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0002_patient_gender'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='slot',
            field=models.CharField(blank=True, choices=[('9-10', '9-10'), ('10-11', '10-11'), ('11-12', '11-12'), ('1-2', '1-2'), ('2-3', '2-3'), ('3-4', '3-4'), ('4-5', '4-5')], max_length=5, null=True),
        ),
    ]