# Generated by Django 4.1 on 2022-08-25 00:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form1', '0012_remove_form1detail_dialer_address_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='form1detail',
            name='City',
        ),
        migrations.RemoveField(
            model_name='form1detail',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='form1detail',
            name='Pin_Code',
        ),
        migrations.RemoveField(
            model_name='form1detail',
            name='State',
        ),
        migrations.RemoveField(
            model_name='history',
            name='City',
        ),
        migrations.RemoveField(
            model_name='history',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='history',
            name='Pin_Code',
        ),
        migrations.RemoveField(
            model_name='history',
            name='State',
        ),
        migrations.RemoveField(
            model_name='operations',
            name='City',
        ),
        migrations.RemoveField(
            model_name='operations',
            name='Country',
        ),
        migrations.RemoveField(
            model_name='operations',
            name='Pin_Code',
        ),
        migrations.RemoveField(
            model_name='operations',
            name='State',
        ),
        migrations.AddField(
            model_name='form1detail',
            name='Dialer_Address',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='form1detail',
            name='Division',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='Dialer_Address',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='history',
            name='Division',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operations',
            name='Dialer_Address',
            field=models.TextField(default='', max_length=500),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='operations',
            name='Division',
            field=models.CharField(default='', max_length=500),
            preserve_default=False,
        ),
    ]
