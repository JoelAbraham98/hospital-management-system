# Generated by Django 5.0.6 on 2024-07-26 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0031_alter_medicalrecord_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='medicalrecord',
            unique_together=set(),
        ),
    ]
