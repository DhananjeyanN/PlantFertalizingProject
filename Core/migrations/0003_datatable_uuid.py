# Generated by Django 4.2.4 on 2023-10-03 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Core', '0002_alter_plant_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='datatable',
            name='uuid',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
