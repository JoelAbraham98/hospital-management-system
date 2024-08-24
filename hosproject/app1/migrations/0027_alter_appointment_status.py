# Generated by Django 5.0.6 on 2024-07-23 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0026_alter_appointment_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('missed', 'missed'), ('completed', 'Completed'), ('skipped', 'Skipped')], default='scheduled', max_length=20),
        ),
    ]
