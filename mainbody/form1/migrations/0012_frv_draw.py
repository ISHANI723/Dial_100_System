# Generated by Django 4.1 on 2022-08-25 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form1', '0011_frv_assigned_waypoints_alter_frv_assigned_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Frv_Draw',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Cord', models.TextField()),
                ('Name', models.CharField(max_length=500)),
                ('Lat', models.TextField()),
                ('Lag', models.TextField()),
            ],
        ),
    ]
