# Generated by Django 4.1 on 2022-08-17 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sip_db', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_details',
            name='aadhar',
            field=models.CharField(max_length=12),
        ),
        migrations.AlterField(
            model_name='user_details',
            name='dob',
            field=models.CharField(max_length=10),
        ),
    ]