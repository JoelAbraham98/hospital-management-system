# Generated by Django 5.0.6 on 2024-07-23 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0023_remove_appointment_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='description_file',
            field=models.FileField(blank=True, null=True, upload_to='appointment_descriptions/'),
        ),
    ]