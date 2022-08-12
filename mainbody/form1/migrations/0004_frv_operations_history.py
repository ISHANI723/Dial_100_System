# Generated by Django 4.1 on 2022-08-11 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form1', '0003_form1detail_frv_req'),
    ]

    operations = [
        migrations.CreateModel(
            name='FRV',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FRV_Type', models.CharField(max_length=20)),
                ('FRV_Plate_No', models.CharField(max_length=10)),
                ('Driver_Name', models.CharField(max_length=100)),
                ('Driver_Number', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Operations',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('Dialer_Name', models.CharField(max_length=300)),
                ('Dialer_Address', models.TextField(max_length=500)),
                ('Describe_call', models.TextField(max_length=500)),
                ('Incident_Type', models.CharField(max_length=500)),
                ('Phone_Number', models.CharField(max_length=10)),
                ('Division', models.CharField(max_length=500)),
                ('District', models.CharField(max_length=500)),
                ('Incident_Address', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('frvs', models.ManyToManyField(blank=True, to='form1.frv')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('Dialer_Name', models.CharField(max_length=300)),
                ('Dialer_Address', models.TextField(max_length=500)),
                ('Describe_call', models.TextField(max_length=500)),
                ('Incident_Type', models.CharField(max_length=500)),
                ('Phone_Number', models.CharField(max_length=10)),
                ('Division', models.CharField(max_length=500)),
                ('District', models.CharField(max_length=500)),
                ('Incident_Address', models.TextField(max_length=500)),
                ('date', models.DateField()),
                ('frvs', models.ManyToManyField(blank=True, to='form1.frv')),
            ],
        ),
    ]
