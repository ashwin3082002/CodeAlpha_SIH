# Generated by Django 4.1 on 2022-08-20 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sip_db', '0013_student_detail_i_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student_detail',
            name='dob',
            field=models.CharField(max_length=20),
        ),
    ]
