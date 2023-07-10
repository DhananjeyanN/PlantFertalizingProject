# Generated by Django 4.2.2 on 2023-07-10 03:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('photo', models.ImageField(upload_to='photos/plants/%Y/%m/%d/')),
                ('ec', models.CharField(max_length=1000)),
                ('ph', models.CharField(max_length=1000)),
                ('npk', models.CharField(max_length=1000)),
                ('temperature', models.CharField(max_length=1000)),
                ('ideal_moisture', models.CharField(max_length=1000)),
                ('fertilizer', models.CharField(max_length=1000)),
                ('plant_coefficient', models.FloatField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='DataTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('m_temp', models.FloatField(null=True)),
                ('m_moist', models.FloatField(null=True)),
                ('m_ec', models.FloatField(null=True)),
                ('m_npk', models.FloatField(null=True)),
                ('m_ph', models.FloatField(null=True)),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Core.plant')),
            ],
        ),
    ]
