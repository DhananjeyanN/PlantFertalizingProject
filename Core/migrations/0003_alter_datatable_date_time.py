# Generated by Django 4.2.4 on 2024-02-09 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_remove_sensor_sensor_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datatable',
            name='date_time',
            field=models.DateTimeField(),
        ),
    ]
